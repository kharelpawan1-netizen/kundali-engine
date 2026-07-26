"""
Integration tests for the Swiss Ephemeris wrapper.

These tests require a local Swiss Ephemeris installation.
"""

from datetime import datetime
from pathlib import Path

import pytest

from astronomy.julian import datetime_to_julian
from astronomy.swiss import (
    Ayanamsha,
    get_ayanamsha,
    get_ephemeris_path,
    planet_longitude,
    planet_position,
    set_ayanamsha,
    set_ephemeris_path,
)
from models.graha import Graha

# ------------------------------------------------------------
# Configure your ephemeris folder here
# ------------------------------------------------------------

EPHE_PATH = Path(r"D:\kundali\ephe")


@pytest.fixture(scope="module", autouse=True)
def configure_swiss():
    """
    Configure Swiss Ephemeris once.
    """
    set_ephemeris_path(EPHE_PATH)
    set_ayanamsha(Ayanamsha.LAHIRI)


def test_ephemeris_path():
    """Ephemeris path should be configured."""
    assert get_ephemeris_path() == EPHE_PATH.resolve()


def test_ayanamsha():
    """Lahiri ayanamsha should be active."""
    assert get_ayanamsha() == Ayanamsha.LAHIRI


def test_planet_position():
    """Planet position should return a valid object."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    sun = planet_position(jd, Graha.SUN)

    assert 0.0 <= sun.longitude < 360.0
    assert isinstance(sun.longitude, float)
    assert isinstance(sun.latitude, float)


def test_planet_longitude():
    """planet_longitude() should return a float."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    lon = planet_longitude(jd, Graha.MOON)

    assert isinstance(lon, float)
    assert 0.0 <= lon < 360.0


def test_rahu_ketu_difference():
    """Rahu and Ketu must be opposite."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    rahu = planet_position(jd, Graha.RAHU)
    ketu = planet_position(jd, Graha.KETU)

    difference = (ketu.longitude - rahu.longitude) % 360.0

    assert abs(difference - 180.0) < 1e-8
