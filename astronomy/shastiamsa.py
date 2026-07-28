"""
Shastiamsa (D60) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into sixty equal parts.

Odd signs:
    Counting begins from Aries.

Even signs:
    Counting begins from Libra.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.shastiamsa_position import ShastiamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 60.0

ODD_SIGNS = {
    1,  # Aries
    3,  # Gemini
    5,  # Leo
    7,  # Libra
    9,  # Sagittarius
    11,  # Aquarius
}


def shastiamsa(
    longitude: float,
) -> ShastiamsaPosition:
    """
    Compute Shastiamsa (D60).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    ShastiamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 60:
        division = 60

    if sign_number in ODD_SIGNS:
        start = 1  # Aries
    else:
        start = 7  # Libra

    target = ((start + division - 2) % 12) + 1

    return ShastiamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "shastiamsa",
]
