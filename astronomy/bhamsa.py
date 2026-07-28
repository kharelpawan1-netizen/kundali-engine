"""
Bhamsa (D27) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into twenty-seven equal parts.

Odd signs:
    Counting begins from Aries.

Even signs:
    Counting begins from Libra.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.bhamsa_position import BhamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 27.0

ODD_SIGNS = {
    1,  # Aries
    3,  # Gemini
    5,  # Leo
    7,  # Libra
    9,  # Sagittarius
    11,  # Aquarius
}


def bhamsa(
    longitude: float,
) -> BhamsaPosition:
    """
    Compute Bhamsa (D27).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    BhamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 27:
        division = 27

    if sign_number in ODD_SIGNS:
        start = 1  # Aries
    else:
        start = 7  # Libra

    target = ((start + division - 2) % 12) + 1

    return BhamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "bhamsa",
]
