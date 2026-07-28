"""
Shodasamsa (D16) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into sixteen equal parts.

Movable signs:
    Counting begins from Aries.

Fixed signs:
    Counting begins from Leo.

Dual signs:
    Counting begins from Sagittarius.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.shodasamsa_position import ShodasamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 16.0

MOVABLE_SIGNS = {
    1,  # Aries
    4,  # Cancer
    7,  # Libra
    10,  # Capricorn
}

FIXED_SIGNS = {
    2,  # Taurus
    5,  # Leo
    8,  # Scorpio
    11,  # Aquarius
}

DUAL_SIGNS = {
    3,  # Gemini
    6,  # Virgo
    9,  # Sagittarius
    12,  # Pisces
}


def shodasamsa(
    longitude: float,
) -> ShodasamsaPosition:
    """
    Compute Shodasamsa (D16).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    ShodasamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 16:
        division = 16

    if sign_number in MOVABLE_SIGNS:
        start = 1  # Aries
    elif sign_number in FIXED_SIGNS:
        start = 5  # Leo
    else:
        start = 9  # Sagittarius

    target = ((start + division - 2) % 12) + 1

    return ShodasamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "shodasamsa",
]
