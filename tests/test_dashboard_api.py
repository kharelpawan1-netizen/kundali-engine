"""
tests/test_dashboard_api.py

Automated integration test suite for the Vedic Kundali Analytics API.
Tests all endpoints, validations, chart calculations, Balas, Panchadha,
Sade Sati, Transits, Vargas, Dashas, and Yogas.
"""

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "kundali-analytics-api"


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


def test_nepal_districts_endpoint():
    res = client.get("/api/nepal-districts")
    assert res.status_code == 200
    data = res.json()
    assert data["total_districts"] == 77
    assert len(data["districts"]) == 77
    provinces = data["provinces"]
    expected_provinces = ["Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"]
    for prov in expected_provinces:
        assert prov in provinces
        assert len(provinces[prov]) > 0


def test_district_queries():
    # Test searching various districts across different provinces
    for q in ["Jhapa", "Mustang", "Humla", "Dang", "Ilam", "Chitwan", "Kailali", "Rupandehi"]:
        res = client.get(f"/api/cities?q={q}")
        assert res.status_code == 200
        results = res.json()["results"]
        assert len(results) >= 1
        assert results[0]["timezone"] == "Asia/Kathmandu"


def test_sample_profiles_endpoint():
    res = client.get("/api/sample-profiles")
    assert res.status_code == 200
    profiles = res.json()
    assert len(profiles) >= 5
    names = [p["name"] for p in profiles]
    assert "Pawan Sharma" in names
    assert "Aarav Gupta" in names


def test_current_transits_endpoint():
    res = client.get("/api/transits-current")
    assert res.status_code == 200
    data = res.json()
    assert "planets" in data
    assert len(data["planets"]) == 9
    p_names = [p["planet"] for p in data["planets"]]
    assert "Sun" in p_names
    assert "Jupiter" in p_names
    assert "Saturn" in p_names


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

    # 3. Planets list (Sun to Ketu) with combustion checks
    assert len(data["planets"]) == 9
    for p in data["planets"]:
        assert "is_combust" in p
        assert "dignity" in p
        assert "speed" in p

    # 4. Houses 1 to 12
    assert len(data["houses"]) == 12
    for idx, h in enumerate(data["houses"], 1):
        assert h["house"] == idx
        assert "sign" in h
        assert "sign_lord" in h
        assert "occupants" in h

    # 5. Divisional Charts (Vargas D1 to D60)
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

    # 7. Vedic Yogas (including Guru Chandal Yoga)
    assert "yogas" in data
    assert "all" in data["yogas"]
    assert "detected" in data["yogas"]
    yoga_names = [y["name"] for y in data["yogas"]["all"]]
    assert "Guru Chandal Yoga" in yoga_names
    assert "Raja Yoga" in yoga_names

    # 8. Planetary Strengths (Balas)
    assert "balas" in data
    assert len(data["balas"]["planets"]) == 7
    for bp in data["balas"]["planets"]:
        assert "total_virupas" in bp
        assert "relative_percentage" in bp
        assert "status" in bp

    # 9. Panchadha Maitri Matrix (5-fold relationship)
    assert "panchadha" in data
    assert "matrix" in data["panchadha"]
    assert "Sun" in data["panchadha"]["matrix"]
    assert "Mars" in data["panchadha"]["matrix"]["Sun"]

    # 10. Shani Sade Sati
    assert "sade_sati" in data
    assert "is_active" in data["sade_sati"]
    assert "current_phase" in data["sade_sati"]
    assert "estimated_periods" in data["sade_sati"]

    # 11. Live Transits (Gochara)
    assert "transits" in data
    assert "transits" in data["transits"]
    assert len(data["transits"]["transits"]) == 9

    # 12. Synthesis
    assert "synthesis" in data
    assert "themes" in data["synthesis"]


def test_validation_errors():
    # Invalid date
    res_bad_date = client.post("/api/chart", json={
        "name": "Test",
        "birth_date": "invalid-date",
        "birth_time": "12:00:00",
        "place": "Kathmandu",
    })
    assert res_bad_date.status_code == 422

    # Invalid latitude (> 90)
    res_bad_lat = client.post("/api/chart", json={
        "name": "Test",
        "birth_date": "1995-08-20",
        "birth_time": "12:00:00",
        "place": "Kathmandu",
        "latitude": 150.0,
    })
    assert res_bad_lat.status_code == 422
