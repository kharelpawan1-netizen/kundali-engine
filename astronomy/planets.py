"""
Planet calculation engine.

This module calculates all nine grahas
using the Swiss Ephemeris wrapper.
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
    Calculate all grahas.

    Parameters
    ----------
    julian_day
        Julian Day.

    Returns
    -------
    dict
        Mapping:
            Graha -> EphemerisPosition
    """

    positions = {}

    for graha in Graha:
        positions[graha] = planet_position(
            julian_day,
            graha,
        )

    return positions
