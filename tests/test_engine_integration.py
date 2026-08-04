
"""
tests/test_engine_integration.py

Full integration tests for the Kundali Horoscope Engine.

Tests the complete flow:

    BirthData
        ↓
    Local time -> UTC
        ↓
    Julian Day
        ↓
    Swiss Ephemeris
        ↓
    Lahiri Ayanamsha
        ↓
    Ascendant
        ↓
    Whole-sign houses
        ↓
    Planetary positions
        ↓
    Nakshatra / Pada
        ↓
    Planet-to-house assignment
        ↓
    Planetary dignity
        ↓
    Parashari aspects
        ↓
    Vimshottari Dasha hierarchy
        ↓
    Complete BirthChart

The test automatically discovers the Swiss Ephemeris data directory
inside the project and initializes the Swiss wrapper before running
the integration tests.

Compatible with:
    Python 3.9+
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from engine import HoroscopeEngine

from astronomy.swiss import (
    Ayanamsha,
    get_ephemeris_path,
    set_ayanamsha,
    set_ephemeris_path,
)

from models.birth_data import BirthData
from models.location import Location


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# SWISS EPHEMERIS DISCOVERY
# ============================================================


def find_ephemeris_directory() -> Path:
    """
    Find a directory containing Swiss Ephemeris data files.

    The project may store ephemeris files in different directories,
    so the test does not hard-code one particular path.

    Returns
    -------
    Path
        Directory containing Swiss Ephemeris files.

    Raises
    ------
    FileNotFoundError
        If no Swiss Ephemeris data directory can be found.
    """

    candidate_directories = [
        PROJECT_ROOT / "ephemeris",
        PROJECT_ROOT / "ephe",
        PROJECT_ROOT / "data" / "ephemeris",
        PROJECT_ROOT / "data" / "ephe",
        PROJECT_ROOT / "astronomy" / "ephemeris",
        PROJECT_ROOT / "astronomy" / "ephe",
    ]

    # --------------------------------------------------------
    # First: check known locations
    # --------------------------------------------------------

    for directory in candidate_directories:

        if not directory.is_dir():
            continue

        if any(directory.glob("*.se1")):
            return directory

        if any(directory.glob("*.se2")):
            return directory

        if any(directory.glob("*.se3")):
            return directory

    # --------------------------------------------------------
    # Second: search the project recursively
    # --------------------------------------------------------

    for file_path in PROJECT_ROOT.rglob("*.se1"):

        if file_path.is_file():
            return file_path.parent

    for file_path in PROJECT_ROOT.rglob("*.se2"):

        if file_path.is_file():
            return file_path.parent

    for file_path in PROJECT_ROOT.rglob("*.se3"):

        if file_path.is_file():
            return file_path.parent

    raise FileNotFoundError(
        "Swiss Ephemeris data files were not found.\n\n"
        "Expected files such as *.se1, *.se2, or *.se3.\n"
        f"Project root searched: {PROJECT_ROOT}\n\n"
        "Please verify that the Swiss Ephemeris data files "
        "have been downloaded into the project."
    )


# ============================================================
# TEST SESSION INITIALIZATION
# ============================================================


@pytest.fixture(scope="session", autouse=True)
def initialize_swiss_ephemeris():
    """
    Initialize Swiss Ephemeris once for the entire integration
    test session.

    This fixture intentionally initializes the dependency at the
    test boundary rather than hiding initialization inside every
    individual test.
    """

    ephemeris_directory = find_ephemeris_directory()

    set_ephemeris_path(
        ephemeris_directory
    )

    set_ayanamsha(
        Ayanamsha.LAHIRI
    )

    assert (
        get_ephemeris_path()
        == ephemeris_directory.resolve()
    )


# ============================================================
# TEST BIRTH DATA
# ============================================================


def make_birth_data() -> BirthData:
    """
    Create a deterministic test birth record.

    Location:
        Kathmandu, Nepal

    Latitude:
        27.7172 N

    Longitude:
        85.3240 E

    Timezone:
        Asia/Kathmandu
    """

    location = Location(
        name="Kathmandu",
        latitude=27.7172,
        longitude=85.3240,
        elevation=0.0,
        timezone="Asia/Kathmandu",
        city="Kathmandu",
        country="Nepal",
    )

    birth_datetime = datetime(
        2000,
        1,
        1,
        12,
        0,
        0,
    )

    return BirthData(
    name="Test Birth",
    birth_datetime=birth_datetime,
    location=location,
)


# ============================================================
# ENGINE BUILDER
# ============================================================


def build_test_chart():

    birth = make_birth_data()

    engine = HoroscopeEngine()

    chart = engine.build_chart(
        birth
    )

    return birth, chart


# ============================================================
# BASIC ENGINE TESTS
# ============================================================


def test_engine_builds_birth_chart():

    birth, chart = build_test_chart()

    assert chart is not None
    assert chart.birth_data is birth


def test_engine_calculates_julian_day():

    _, chart = build_test_chart()

    assert chart.julian_day > 0.0


def test_engine_calculates_ayanamsa():

    _, chart = build_test_chart()

    assert 20.0 < chart.ayanamsa < 30.0


# ============================================================
# ASCENDANT
# ============================================================


def test_engine_calculates_ascendant():

    _, chart = build_test_chart()

    assert 0.0 <= chart.ascendant < 360.0


def test_engine_calculates_ascendant_sign():

    _, chart = build_test_chart()

    assert chart.ascendant_sign != ""

    valid_signs = {
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    }

    assert chart.ascendant_sign in valid_signs


def test_engine_calculates_ascendant_degree():

    _, chart = build_test_chart()

    assert (
        0.0
        <= chart.ascendant_degree
        < 30.0
    )


# ============================================================
# PLANETS
# ============================================================


def test_engine_populates_planets():

    _, chart = build_test_chart()

    assert len(chart.planets) >= 9


def test_engine_contains_core_planets():

    _, chart = build_test_chart()

    required_planets = {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
    }

    assert required_planets.issubset(
        set(chart.planets.keys())
    )


def test_engine_contains_rahu_and_ketu():

    _, chart = build_test_chart()

    assert "Rahu" in chart.planets
    assert "Ketu" in chart.planets


def test_planets_have_valid_longitudes():

    _, chart = build_test_chart()

    for planet in chart.planets.values():

        assert (
            0.0
            <= planet.longitude
            < 360.0
        )


# ============================================================
# HOUSES
# ============================================================


def test_engine_populates_twelve_houses():

    _, chart = build_test_chart()

    assert len(chart.houses) == 12


def test_engine_houses_are_numbered_one_to_twelve():

    _, chart = build_test_chart()

    assert set(chart.houses.keys()) == set(
        range(1, 13)
    )


# ============================================================
# COMPLETE CHART
# ============================================================


def test_engine_produces_complete_chart():

    _, chart = build_test_chart()

    assert chart.is_complete()


def test_birth_data_is_preserved():

    birth, chart = build_test_chart()

    assert chart.birth_data is birth

    assert (
        chart.birth_data.birth_datetime
        == birth.birth_datetime
    )

    assert (
        chart.birth_data.location.latitude
        == birth.location.latitude
    )

    assert (
        chart.birth_data.location.longitude
        == birth.location.longitude
    )


# ============================================================
# PLANET / HOUSE RELATIONSHIP
# ============================================================


def test_planets_have_house_information_when_available():

    _, chart = build_test_chart()

    for planet in chart.planets.values():

        # The engine's house assignment should provide
        # house information when supported by the Planet model.
        if hasattr(planet, "house"):

            assert (
                planet.house is None
                or 1 <= planet.house <= 12
            )


def test_houses_have_valid_sign_information():

    _, chart = build_test_chart()

    valid_signs = {
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    }

    for house in chart.houses.values():

        assert house.sign in valid_signs

        assert (
            1
            <= house.sign_number
            <= 12
        )

        assert (
            1
            <= house.number
            <= 12
        )


# ============================================================
# REPEATABILITY
# ============================================================


def test_engine_build_is_repeatable():

    birth = make_birth_data()

    engine = HoroscopeEngine()

    chart_one = engine.build_chart(
        birth
    )

    chart_two = engine.build_chart(
        birth
    )

    assert (
        chart_one.julian_day
        == chart_two.julian_day
    )

    assert (
        chart_one.ayanamsa
        == pytest.approx(
            chart_two.ayanamsa,
            abs=1e-10,
        )
    )

    assert (
        chart_one.ascendant
        == pytest.approx(
            chart_two.ascendant,
            abs=1e-10,
        )
    )

    assert (
        chart_one.ascendant_sign
        == chart_two.ascendant_sign
    )

    assert (
        chart_one.ascendant_degree
        == pytest.approx(
            chart_two.ascendant_degree,
            abs=1e-10,
        )
    )

    assert set(
        chart_one.planets.keys()
    ) == set(
        chart_two.planets.keys()
    )

    for planet_name in chart_one.planets:

        planet_one = chart_one.planets[
            planet_name
        ]

        planet_two = chart_two.planets[
            planet_name
        ]

        assert (
            planet_one.longitude
            == pytest.approx(
                planet_two.longitude,
                abs=1e-10,
            )
        )

        assert (
            planet_one.latitude
            == pytest.approx(
                planet_two.latitude,
                abs=1e-10,
            )
        )

        assert (
            planet_one.speed
            == pytest.approx(
                planet_two.speed,
                abs=1e-10,
            )
        )
