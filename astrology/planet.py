"""
astrology/planet.py

Planet domain construction for the Kundali Engine.

This module converts low-level astronomical ephemeris results
into the project's Planet domain model.

Responsibilities
----------------
- Convert Graha enum values into Planet objects.
- Attach sidereal Rashi information.
- Attach Nakshatra and Pada information.
- Preserve astronomical speed and retrograde information.
- Keep house calculation outside this module.
- Keep planetary dignity and other interpretive classifications
  outside this module.

This module does not perform Swiss Ephemeris calculations.

Compatible with Python 3.9+.
"""

from __future__ import annotations

from typing import Dict

from astronomy.nakshatra import longitude_to_nakshatra
from astronomy.signs import longitude_to_sign
from models.ephemeris_position import EphemerisPosition
from models.graha import Graha
from models.planet import Planet


def build_planet(
    graha: Graha,
    position: EphemerisPosition,
) -> Planet:
    """
    Build a Planet domain object from an astronomical position.

    Parameters
    ----------
    graha
        Vedic Graha represented by the astronomical position.

    position
        Astronomical position returned by the Swiss Ephemeris
        wrapper.

    Returns
    -------
    Planet
        Fully populated astronomical, Rashi, and Nakshatra
        information.

    Notes
    -----
    House placement is intentionally not calculated here because
    it depends on the chart's house system and Ascendant.

    Planetary dignity, combustion, exaltation, debilitation,
    own-sign status, and Moolatrikona are also intentionally
    left for their dedicated calculation layers.
    """

    longitude = position.longitude

    sign_info = longitude_to_sign(longitude)
    nakshatra_info = longitude_to_nakshatra(longitude)

    return Planet(
        name=graha.display_name,
        longitude=longitude,
        latitude=position.latitude,
        distance=position.distance,
        speed=position.longitude_speed,
        retrograde=position.retrograde,
        sign=sign_info.sign.display_name,
        sign_number=sign_info.number,
        sign_degree=sign_info.degree,
        house=0,
        nakshatra=nakshatra_info.name,
        pada=nakshatra_info.pada,
        nakshatra_lord=nakshatra_info.lord,
    )


def build_planets(
    positions: Dict[Graha, EphemerisPosition],
) -> Dict[Graha, Planet]:
    """
    Convert astronomical positions for all Grahas into Planet
    domain objects.

    Parameters
    ----------
    positions
        Mapping from Graha to EphemerisPosition.

    Returns
    -------
    dict
        Mapping from Graha to Planet.

    Raises
    ------
    TypeError
        If a supplied value is not an EphemerisPosition.
    """

    planets: Dict[Graha, Planet] = {}

    for graha, position in positions.items():
        if not isinstance(position, EphemerisPosition):
            raise TypeError(
                "Each planetary position must be an "
                "EphemerisPosition."
            )

        planets[graha] = build_planet(
            graha,
            position,
        )

    return planets


__all__ = [
    "build_planet",
    "build_planets",
]