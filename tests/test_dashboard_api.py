"""
tests/test_dashboard_api.py

Automated integration test suite for the Kundali Dashboard API.
Tests all endpoints, chart calculations, vargas, dashas, and yogas.
"""

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "kundali-dashboard-api"


def test_static_files():
    # Index HTML
    res_index = client.get("/")
    assert res_index.status_code == 200
    assert "KUNDALI" in res_index.text
    assert "DASHBOARD" in res_index.text

    # Stylesheet
    res_css = client.get("/static/styles.css")
    assert res_css.status_code == 200
    assert "--gold-primary" in res_css.text

    # Chart Renderer JS
    res_chart = client.get("/static/chart_renderer.js")
    assert res_chart.status_code == 200
    assert "renderNorthIndianSvg" in res_chart.text
    assert "renderSouthIndianSvg" in res_chart.text

    # Main App JS
    res_app = client.get("/static/app.js")
    assert res_app.status_code == 200
    assert "renderCompleteDashboard" in res_app.text


def test_cities_endpoint():
    # Empty query returns top results
    res = client.get("/api/cities")
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) > 0

    # Query for Kathmandu
    res_ktm = client.get("/api/cities?q=kathmandu")
    assert res_ktm.status_code == 200
    ktm_data = res_ktm.json()
    assert len(ktm_data["results"]) >= 1
    assert "Kathmandu" in ktm_data["results"][0]["name"]
    assert ktm_data["results"][0]["timezone"] == "Asia/Kathmandu"


def test_sample_profiles_endpoint():
    res = client.get("/api/sample-profiles")
    assert res.status_code == 200
    profiles = res.json()
    assert len(profiles) >= 5
    names = [p["name"] for p in profiles]
    assert "Pawan Sharma" in names
    assert "Aarav Gupta" in names


def test_chart_calculation_complete():
    payload = {
        "name": "Pawan Sharma",
        "birth_date": "1995-08-20",
        "birth_time": "10:30:00",
        "place": "Kathmandu, Nepal",
        "latitude": 27.7172,
        "longitude": 85.3240,
        "timezone": "Asia/Kathmandu",
        "ayanamsha": "LAHIRI",
    }

    res = client.post("/api/chart", json=payload)
    assert res.status_code == 200
    data = res.json()

    # 1. Native metadata
    assert data["native"]["name"] == "Pawan Sharma"
    assert data["native"]["place"] == "Kathmandu, Nepal"
    assert "janma_rasi" in data["native"]

    # 2. Ascendant
    assert "sign" in data["ascendant"]
    assert "sign_degree_dms" in data["ascendant"]
    assert "nakshatra" in data["ascendant"]

    # 3. Planets list (Sun to Ketu)
    assert len(data["planets"]) == 9
    planet_names = [p["name"] for p in data["planets"]]
    for expected in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        assert expected in planet_names

    # 4. Houses 1 to 12
    assert len(data["houses"]) == 12
    for idx, h in enumerate(data["houses"], 1):
        assert h["house"] == idx
        assert "sign" in h
        assert "sign_lord" in h
        assert "occupants" in h

    # 5. Divisional Charts (Vargas)
    vargas = data["vargas"]
    assert "D1" in vargas
    assert "D9" in vargas
    assert "D10" in vargas
    assert "D60" in vargas
    assert len(vargas) >= 15

    # 6. Vimshottari Dashas
    dashas = data["dashas"]
    assert "active_chain" in dashas
    assert dashas["active_chain"]["mahadasha"] is not None
    assert len(dashas["mahadashas"]) == 9

    # 7. Vedic Yogas
    assert "yogas" in data
    assert "all" in data["yogas"]
    assert "detected" in data["yogas"]

    # 8. Synthesis
    assert "synthesis" in data
    assert "themes" in data["synthesis"]


def test_chart_calculation_different_locations():
    # Profile: New Delhi
    res_delhi = client.post("/api/chart", json={
        "name": "Aarav",
        "birth_date": "2000-01-01",
        "birth_time": "12:00:00",
        "place": "New Delhi, India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata",
    })
    assert res_delhi.status_code == 200
    assert res_delhi.json()["ascendant"]["sign"] == "Pisces"

    # Profile: Tokyo
    res_tokyo = client.post("/api/chart", json={
        "name": "Kenji",
        "birth_date": "1999-09-09",
        "birth_time": "09:09:00",
        "place": "Tokyo, Japan",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "timezone": "Asia/Tokyo",
    })
    assert res_tokyo.status_code == 200
    assert len(res_tokyo.json()["planets"]) == 9
