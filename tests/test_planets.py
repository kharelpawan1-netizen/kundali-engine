"""
Tests for the planet calculation engine.
"""

from datetime import datetime

from astronomy.julian import datetime_to_julian
from astronomy.planets import calculate_planets
from astronomy.swiss import (
    Ayanamsha,
    set_ayanamsha,
    set_ephemeris_path,
)
from models.ephemeris_position import EphemerisPosition
from models.graha import Graha

set_ephemeris_path(r"D:\kundali\ephe")
set_ayanamsha(Ayanamsha.LAHIRI)


def test_calculate_planets_returns_dictionary():
    """Engine should return a dictionary."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    planets = calculate_planets(jd)

    assert isinstance(planets, dict)


def test_all_nine_grahas_exist():
    """Every graha should be calculated."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    planets = calculate_planets(jd)

    assert len(planets) == 9

    for graha in Graha:
        assert graha in planets


def test_every_value_is_ephemeris_position():
    """Each dictionary value must be EphemerisPosition."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    planets = calculate_planets(jd)

    for value in planets.values():
        assert isinstance(value, EphemerisPosition)


def test_longitudes_are_normalized():
    """Planet longitudes must lie inside 0–360°."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    planets = calculate_planets(jd)

    for position in planets.values():
        assert 0.0 <= position.longitude < 360.0


def test_rahu_ketu_are_opposite():
    """Rahu and Ketu must always differ by 180 degrees."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    planets = calculate_planets(jd)

    rahu = planets[Graha.RAHU].longitude
    ketu = planets[Graha.KETU].longitude

    difference = (ketu - rahu) % 360.0

    assert abs(difference - 180.0) < 1e-8
