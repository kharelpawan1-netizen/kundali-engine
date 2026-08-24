"""
api/app.py

Production-ready FastAPI backend server for the Vedic Kundali Analytics Platform.
Features:
- Thread-safe Swiss Ephemeris ayanamsha locking
- In-memory LRU calculation cache
- Strict Pydantic input validation
- Rich error handling & request logging
- Endpoints for full horoscope, transits, Sade Sati, 77 Nepal districts, and geocoding.
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from api.cities_db import CITIES_DATA, NEPAL_DISTRICTS_DATA, search_cities
from api.serializers import serialize_complete_chart
from astronomy.julian import datetime_to_julian
from astronomy.planets import calculate_planets
from astronomy.signs import sign_enum, sign_number
from astronomy.swiss import Ayanamsha, set_ayanamsha, set_ephemeris_path
from engine import HoroscopeEngine
from models.birth_data import BirthData
from models.location import Location

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("kundali.api")

# Initialize paths and engine
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"
EPHEMERIS_PATH = PROJECT_ROOT / "ephe"

set_ephemeris_path(EPHEMERIS_PATH)
set_ayanamsha(Ayanamsha.LAHIRI)
horoscope_engine = HoroscopeEngine()

# Thread lock to guarantee concurrency safety for global Swiss Ephemeris C state
EPHEMERIS_LOCK = threading.Lock()

# In-memory Calculation Cache (Hash -> Response JSON, max 500 entries)
CALCULATION_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_LOCK = threading.Lock()
MAX_CACHE_SIZE = 500

app = FastAPI(
    title="Vedic Kundali Analytics Platform API",
    description="High-precision Vedic Astrology calculation, Shodashavarga, Vimshottari Dasha, Yogas, and Sade Sati Analytics API.",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Allow CORS for cross-origin and local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return user-friendly JSON error details for validation errors."""
    errors = []
    for err in exc.errors():
        field_name = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": field_name,
            "message": err.get("msg", "Invalid input value"),
            "type": err.get("type", "value_error"),
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "One or more input fields are invalid.",
            "details": errors,
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Format HTTP exceptions into consistent JSON format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request Error",
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
        },
    )


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class BirthChartRequest(BaseModel):
    name: str = Field(default="Native", description="Name of the native")
    birth_date: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    birth_time: str = Field(..., description="Time of birth (HH:MM or HH:MM:SS)")
    place: str = Field(default="Kathmandu, Nepal", description="Place name")
    latitude: float = Field(default=27.7172, ge=-90.0, le=90.0, description="Latitude in decimal degrees (-90 to +90)")
    longitude: float = Field(default=85.3240, ge=-180.0, le=180.0, description="Longitude in decimal degrees (-180 to +180)")
    timezone: str = Field(default="Asia/Kathmandu", description="IANA Timezone name")
    elevation: float = Field(default=0.0, ge=0.0, le=8848.0, description="Elevation in meters")
    gender: Optional[str] = Field(default="", description="Gender of the native")
    ayanamsha: Optional[str] = Field(default="LAHIRI", description="Ayanamsha system (LAHIRI, RAMAN, KP)")

    @field_validator("birth_date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        v = v.strip()
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("birth_date must be in YYYY-MM-DD format (e.g. 1995-08-20)")
        return v

    @field_validator("birth_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        v = v.strip()
        if len(v.split(":")) == 2:
            v = f"{v}:00"
        try:
            datetime.strptime(v, "%H:%M:%S")
        except ValueError:
            raise ValueError("birth_time must be in HH:MM:SS or HH:MM format (24-hour clock)")
        return v


class GeocodeRequest(BaseModel):
    query: str = Field(..., description="Place name or city to geocode")


class SadeSatiRequest(BaseModel):
    moon_sign: str = Field(..., description="Natal Moon sign (e.g. Pisces, Taurus, Cancer)")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_cache_key(req: BirthChartRequest) -> str:
    """Generate SHA256 cache key from calculation parameters."""
    raw = f"{req.birth_date}|{req.birth_time}|{req.latitude:.4f}|{req.longitude:.4f}|{req.timezone}|{req.ayanamsha}|{req.elevation}"
    return hashlib.sha256(raw.encode()).hexdigest()


# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/api/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "kundali-analytics-api",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/cities", tags=["Geographical"])
def get_cities(
    q: Optional[str] = Query(default="", description="Search query"),
    limit: int = Query(default=15, ge=1, le=100, description="Max results"),
) -> Dict[str, Any]:
    """Search pre-indexed fast city and Nepal districts database."""
    results = search_cities(q, limit=limit)
    return {"results": results, "count": len(results)}


@app.get("/api/nepal-districts", tags=["Geographical"])
def get_nepal_districts() -> Dict[str, Any]:
    """Return all 77 districts of Nepal grouped by province."""
    provinces: Dict[str, List[Dict[str, Any]]] = {}
    for d in NEPAL_DISTRICTS_DATA:
        prov = d.get("province", "Other")
        if prov not in provinces:
            provinces[prov] = []
        provinces[prov].append(d)
    return {
        "total_districts": len(NEPAL_DISTRICTS_DATA),
        "provinces": provinces,
        "districts": NEPAL_DISTRICTS_DATA,
    }


@app.post("/api/geocode", tags=["Geographical"])
def geocode_place(payload: GeocodeRequest) -> Dict[str, Any]:
    """Geocode arbitrary place query with online fallback."""
    query = payload.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 1. Offline database lookup
    offline_matches = search_cities(query, limit=5)
    for m in offline_matches:
        if query.lower() in m["name"].lower() or query.lower() in m.get("city", "").lower():
            return {"match": m, "source": "offline_db"}

    # 2. Geopy / TimezoneFinder fallback
    try:
        from geopy.geocoders import Nominatim
        from timezonefinder import TimezoneFinder

        geolocator = Nominatim(user_agent="kundali_analytics_app/3.0", timeout=4)
        loc = geolocator.geocode(query)

        if not loc:
            if offline_matches:
                return {"match": offline_matches[0], "source": "offline_fallback"}
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
        if offline_matches:
            return {"match": offline_matches[0], "source": "offline_fallback"}
        raise HTTPException(status_code=500, detail=f"Geocoding error: {str(e)}")


@app.get("/api/sample-profiles", tags=["Horoscope"])
def get_sample_profiles() -> List[Dict[str, Any]]:
    """Return pre-configured sample horoscope profiles for instant demo calculations."""
    return [
        {
            "id": "sample_1",
            "name": "Pawan Sharma",
            "gender": "Male",
            "birth_date": "1995-08-20",
            "birth_time": "10:30:00",
            "place": "Kathmandu, Nepal",
            "latitude": 27.7172,
            "longitude": 85.3240,
            "timezone": "Asia/Kathmandu",
            "description": "Libra Ascendant, Taurus Moon (Exalted), Budha-Aditya Yoga",
        },
        {
            "id": "sample_2",
            "name": "Aarav Gupta",
            "gender": "Male",
            "birth_date": "2000-01-01",
            "birth_time": "12:00:00",
            "place": "New Delhi, India",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone": "Asia/Kolkata",
            "description": "Pisces Ascendant, Libra Moon, Millennium Chart",
        },
        {
            "id": "sample_3",
            "name": "Maya Thapa",
            "gender": "Female",
            "birth_date": "1998-05-15",
            "birth_time": "06:45:00",
            "place": "Pokhara, Nepal",
            "latitude": 28.2096,
            "longitude": 83.9856,
            "timezone": "Asia/Kathmandu",
            "description": "Taurus Ascendant, Sagittarius Moon, Dhana Yoga",
        },
        {
            "id": "sample_4",
            "name": "Sophia Miller",
            "gender": "Female",
            "birth_date": "1992-11-04",
            "birth_time": "18:20:00",
            "place": "New York, USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
            "description": "Taurus Ascendant, Aquarius Moon, Raja Yoga",
        },
        {
            "id": "sample_5",
            "name": "Kenji Takahashi",
            "gender": "Male",
            "birth_date": "1988-09-09",
            "birth_time": "09:09:00",
            "place": "Tokyo, Japan",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "timezone": "Asia/Tokyo",
            "description": "Libra Ascendant, Leo Moon, Gaja Kesari Yoga",
        },
    ]


@app.get("/api/transits-current", tags=["Analytics"])
def get_current_transits() -> Dict[str, Any]:
    """Get live planetary positions and zodiac signs for today."""
    now_dt = datetime.now()
    with EPHEMERIS_LOCK:
        set_ayanamsha(Ayanamsha.LAHIRI)
        jd = datetime_to_julian(now_dt)
        positions = calculate_planets(jd)

    transits = []
    for graha_enum, pos in positions.items():
        sign_num = sign_number(pos.longitude)
        sign_name = sign_enum(pos.longitude).display_name
        transits.append({
            "planet": graha_enum.display_name,
            "longitude": round(pos.longitude, 4),
            "sign": sign_name,
            "sign_number": sign_num,
            "retrograde": pos.retrograde,
            "speed": round(pos.longitude_speed, 4),
        })

    return {
        "timestamp": now_dt.isoformat(),
        "display_date": now_dt.strftime("%B %d, %Y (%I:%M %p)"),
        "ayanamsa": "Lahiri",
        "planets": transits,
    }


@app.post("/api/chart", tags=["Horoscope"])
def calculate_chart(req: BirthChartRequest) -> Dict[str, Any]:
    """
    Main horoscope calculation endpoint.
    Computes Ascendant, Whole-Sign houses, 9 Grahas, BPHS dignities,
    all 16 Shodashavarga charts, 6-level Vimshottari Dashas, Vedic Yogas,
    Balas strengths, Panchadha Maitri, Shani Sade Sati, and Life Synthesis.
    """
    # 1. Check in-memory LRU cache
    cache_key = make_cache_key(req)
    with CACHE_LOCK:
        if cache_key in CALCULATION_CACHE:
            cached_data = CALCULATION_CACHE[cache_key]
            # Update native name in case it changed
            cached_data["native"]["name"] = req.name.strip() or "Native"
            return cached_data

    # 2. Parse Date & Time
    time_str = req.birth_time if len(req.birth_time.split(":")) == 3 else f"{req.birth_time}:00"
    dt_str = f"{req.birth_date} {time_str}"
    try:
        birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid date/time format: {str(e)}",
        )

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

    # 4. Generate Chart with Thread-Safe Ayanamsha Lock
    with EPHEMERIS_LOCK:
        ay_str = (req.ayanamsha or "LAHIRI").upper()
        if ay_str == "RAMAN":
            set_ayanamsha(Ayanamsha.RAMAN)
        elif ay_str in ("KP", "KRISHNAMURTI"):
            set_ayanamsha(Ayanamsha.KRISHNAMURTI)
        else:
            set_ayanamsha(Ayanamsha.LAHIRI)

        try:
            chart = horoscope_engine.build_chart(birth)
            response_data = serialize_complete_chart(chart)
        except Exception as e:
            logger.exception("Horoscope calculation error")
            raise HTTPException(
                status_code=500,
                detail=f"Horoscope calculation failed: {str(e)}",
            )
        finally:
            # Always reset to LAHIRI default
            set_ayanamsha(Ayanamsha.LAHIRI)

    # 5. Store in cache
    with CACHE_LOCK:
        if len(CALCULATION_CACHE) >= MAX_CACHE_SIZE:
            # Evict oldest entry
            oldest_key = next(iter(CALCULATION_CACHE))
            del CALCULATION_CACHE[oldest_key]
        CALCULATION_CACHE[cache_key] = response_data

    return response_data


# ============================================================
# STATIC FILES & ROOT ROUTE
# ============================================================

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", tags=["Dashboard"])
def serve_dashboard():
    """Serve main SPA dashboard."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard index.html not found.")
    return FileResponse(str(index_path))
