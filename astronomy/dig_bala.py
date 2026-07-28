"""
Dig Bala.

Directional strength according to BPHS.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.graha import Graha

DIG_BALA_HOUSE = {
    Graha.SUN: 10,
    Graha.MARS: 10,
    Graha.MOON: 4,
    Graha.VENUS: 4,
    Graha.JUPITER: 1,
    Graha.MERCURY: 1,
    Graha.SATURN: 7,
}


def strongest_house(
    graha: Graha,
) -> int:
    """
    Return the house where a planet
    attains maximum Dig Bala.
    """

    return DIG_BALA_HOUSE[graha]


def dig_bala(
    graha: Graha,
    house: int,
) -> float:
    """
    Simplified Dig Bala.

    Returns

    60 if the planet occupies its
    strongest house,

    otherwise 0.
    """

    if house == strongest_house(graha):
        return 60.0

    return 0.0


__all__ = [
    "DIG_BALA_HOUSE",
    "strongest_house",
    "dig_bala",
]
