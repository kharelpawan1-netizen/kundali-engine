"""
Integration tests for the Swiss Ephemeris wrapper.

These tests require a local Swiss Ephemeris installation.
"""

from pathlib import Path

import pytest

from astronomy.julian import julian_day
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

EPHE_PATH = Path("D:/kundali/ephe")  # <-- CHANGE THIS


@pytest.fixture(scope="module", autouse=True)
def configure_swiss():
    """
    Configure Swiss Ephemeris once.
    """

    set_ephemeris_path(EPHE_PATH)
    set_ayanamsha(Ayanamsha.LAHIRI)