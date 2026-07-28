"""
Chaturvimshamsa (D24) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into twenty-four equal parts.

Odd signs:
    Counting begins from Leo.

Even signs:
    Counting begins from Cancer.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.chaturvimshamsa_position import ChaturvimshamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 24.0

ODD_SIGNS = {
    1,  # Aries
    3,  # Gemini
    5,  # Leo
    7,  # Libra
    9,  # Sagittarius
    11,  # Aquarius
}

EVEN_SIGNS = {
    2,  # Taurus
    4,  # Cancer
    6,  # Virgo
    8,  # Scorpio
    10,  # Capricorn
    12,  # Pisces
}


def chaturvimshamsa(
    longitude: float,
) -> ChaturvimshamsaPosition:
    """
    Compute Chaturvimshamsa (D24).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    ChaturvimshamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 24:
        division = 24

    if sign_number in ODD_SIGNS:
        start = 5  # Leo
    else:
        start = 4  # Cancer

    target = ((start + division - 2) % 12) + 1

    return ChaturvimshamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "chaturvimshamsa",
]
