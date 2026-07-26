"""
astronomy/planets.py

Planet engine.

This module computes all grahas for a given
Julian Day using the Swiss Ephemeris wrapper.

Version:
    1.0.0
"""

from __future__ import annotations

from typing import Dict

from astronomy.swiss import planet_position
from models.ephemeris_position import EphemerisPosition
from models.graha import Graha


def calculate_planets(
    julian_day: float,
) -> Dict[Graha, EphemerisPosition]:
    """
    Calculate positions of all nine grahas.

    Parameters
    ----------
    julian_day
        Julian Day (UT).

    Returns
    -------
    dict
        Mapping of Graha → EphemerisPosition.
    """

    planets: Dict[Graha, EphemerisPosition] = {}

    for graha in Graha:
        planets[graha] = planet_position(
            julian_day,
            graha,
        )

    return planets
