"""
api/app.py

FastAPI backend server for the Vedic Kundali Dashboard.
Serves calculation endpoints, city lookups, geocoding, and static dashboard assets.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.cities_db import search_cities, CITIES_DATA
from api.serializers import serialize_complete_chart
from astronomy.swiss import Ayanamsha, set_ayanamsha, set_ephemeris_path
from engine import HoroscopeEngine
from models.birth_data import BirthData
from models.location import Location


# Initialize paths and engine
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EPHEMERIS_PATH = PROJECT_ROOT / "ephe"

set_ephemeris_path(EPHEMERIS_PATH)
set_ayanamsha(Ayanamsha.LAHIRI)
horoscope_engine = HoroscopeEngine()

app = FastAPI(
    title="Vedic Kundali Engine Dashboard API",
    description="High-precision Vedic Astrology calculation and visualization API.",
    version="2.5.0",
)

# Allow CORS for local dev flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class BirthChartRequest(BaseModel):
    name: str = Field(default="Native", description="Name of the native")
    birth_date: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Time of birth (HH:MM or HH:MM:SS)")
    place: str = Field(default="Kathmandu, Nepal", description="Place name")
    latitude: float = Field(default=27.7172, description="Latitude in decimal degrees")
    longitude: float = Field(default=85.3240, description="Longitude in decimal degrees")
    timezone: str = Field(default="Asia/Kathmandu", description="IANA Timezone name")
    elevation: float = Field(default=0.0, description="Elevation in meters")
    gender: Optional[str] = Field(default="", description="Gender of the native")
    ayanamsha: Optional[str] = Field(default="LAHIRI", description="Ayanamsha system (LAHIRI, RAMAN, KP)")


class GeocodeRequest(BaseModel):
    query: str = Field(..., description="Place name or city to geocode")


# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/api/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "kundali-dashboard-api",
        "version": "2.5.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/cities")
def get_cities(
    q: Optional[str] = Query(default="", description="Search query"),
    limit: int = Query(default=12, ge=1, le=50, description="Max results"),
) -> Dict[str, Any]:
    """Search pre-indexed fast city database."""
    results = search_cities(q, limit=limit)
    return {"results": results, "count": len(results)}


@app.post("/api/geocode")
def geocode_place(payload: GeocodeRequest) -> Dict[str, Any]:
    """Geocode arbitrary query and return coordinates and IANA timezone."""
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # First check offline database
    offline_matches = search_cities(query, limit=5)
    for m in offline_matches:
        if query.lower() in m["name"].lower() or query.lower() in m["city"].lower():
            return {"match": m, "source": "offline_db"}

    # Online lookup fallback using geopy + timezonefinder
    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder

        geolocator = Nominatim(user_agent="kundali_dashboard_app/1.0", timeout=4)
        loc = geolocator.geocode(query)

        if not loc:
            raise HTTPException(status_code=404, detail=f"Location not found for '{query}'")

        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=loc.longitude, lat=loc.latitude) or "UTC"

        result = {
            "name": loc.address,
            "city": query,
            "country": "",
            "latitude": round(loc.latitude, 5),
            "longitude": round(loc.longitude, 5),
            "timezone": tz_name,
            "elevation": 0.0,
        }
        return {"match": result, "source": "nominatim"}
    except HTTPException:
        raise
    except Exception as e:
        # If network/geopy fails, return first best offline match if any
        if offline_matches:
            return {"match": offline_matches[0], "source": "offline_fallback"}
        raise HTTPException(status_code=500, detail=f"Geocoding error: {str(e)}")


@app.get("/api/sample-profiles")
def get_sample_profiles() -> List[Dict[str, Any]]:
    """Return instant 1-click sample profiles."""
    return [
        {
            "id": "sample-ktm",
            "name": "Pawan Sharma",
            "gender": "Male",
            "birth_date": "1995-08-20",
            "birth_time": "10:30:00",
            "place": "Kathmandu, Nepal",
            "latitude": 27.7172,
            "longitude": 85.3240,
            "timezone": "Asia/Kathmandu",
            "description": "Born in Kathmandu, Nepal - Leo Ascendant with strong Kendra placements",
        },
        {
            "id": "sample-delhi",
            "name": "Aarav Gupta",
            "gender": "Male",
            "birth_date": "2000-01-01",
            "birth_time": "12:00:00",
            "place": "New Delhi, India",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "description": "Millennium birth in New Delhi - Pisces Lagna with Saturn Mahadasha",
        },
        {
            "id": "sample-ny",
            "name": "Sophia Reynolds",
            "gender": "Female",
            "birth_date": "1992-11-14",
            "birth_time": "06:45:00",
            "place": "New York, USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
            "description": "Scorpio native born in New York with Gaja Kesari Yoga",
        },
        {
            "id": "sample-london",
            "name": "Oliver Davies",
            "gender": "Male",
            "birth_date": "1988-06-21",
            "birth_time": "15:15:00",
            "place": "London, United Kingdom",
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
            "description": "Summer Solstice London native with powerful Budha-Aditya Yoga",
        },
        {
            "id": "sample-tokyo",
            "name": "Kenji Takahashi",
            "gender": "Male",
            "birth_date": "1999-09-09",
            "birth_time": "09:09:00",
            "place": "Tokyo, Japan",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "timezone": "Asia/Tokyo",
            "description": "Libra Lagna Tokyo birth with auspicious Dhana Yogas",
        },
    ]


@app.post("/api/chart")
def calculate_chart(req: BirthChartRequest) -> Dict[str, Any]:
    """
    Calculate the full Vedic horoscope, all 16 divisional charts,
    Vimshottari dashas, detected yogas, and life interpretations.
    """
    # 1. Parse Date and Time
    try:
        time_parts = req.birth_time.strip().split(":")
        hh = int(time_parts[0])
        mm = int(time_parts[1]) if len(time_parts) > 1 else 0
        ss = int(float(time_parts[2])) if len(time_parts) > 2 else 0

        date_parts = req.birth_date.strip().split("-")
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])

        birth_dt = datetime(year, month, day, hh, mm, ss)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date or time format. Expected YYYY-MM-DD and HH:MM:SS. Error: {str(e)}",
        )

    # 2. Configure Ayanamsha
    if req.ayanamsha:
        ay_str = req.ayanamsha.upper()
        if ay_str == "RAMAN":
            set_ayanamsha(Ayanamsha.RAMAN)
        elif ay_str in ("KP", "KRISHNAMURTI"):
            set_ayanamsha(Ayanamsha.KRISHNAMURTI)
        else:
            set_ayanamsha(Ayanamsha.LAHIRI)
    else:
        set_ayanamsha(Ayanamsha.LAHIRI)

    # 3. Build Location and BirthData models
    loc = Location(
        name=req.place,
        latitude=req.latitude,
        longitude=req.longitude,
        timezone=req.timezone,
        elevation=req.elevation,
        country="",
        city=req.place.split(",")[0].strip(),
    )

    birth = BirthData(
        name=req.name.strip() or "Native",
        birth_datetime=birth_dt,
        location=loc,
        notes=req.gender or "",
    )

    # 4. Generate Chart via HoroscopeEngine
    try:
        chart = horoscope_engine.build_chart(birth)
        response_data = serialize_complete_chart(chart)
        return response_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Horoscope calculation failed: {str(e)}",
        )


# ============================================================
# STATIC FILES & ROOT ROUTE
# ============================================================

STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def index() -> FileResponse:
    """Serve main SPA dashboard."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard index.html not found.")
    return FileResponse(str(index_path))
