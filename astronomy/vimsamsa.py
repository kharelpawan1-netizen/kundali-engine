"""
Vimsamsa (D20) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into twenty equal parts.

Movable signs:
    Counting begins from Aries.

Fixed signs:
    Counting begins from Sagittarius.

Dual signs:
    Counting begins from Leo.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.vimsamsa_position import VimsamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 20.0

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


def vimsamsa(
    longitude: float,
) -> VimsamsaPosition:
    """
    Compute Vimsamsa (D20).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    VimsamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 20:
        division = 20

    if sign_number in MOVABLE_SIGNS:
        start = 1  # Aries

    elif sign_number in FIXED_SIGNS:
        start = 9  # Sagittarius

    else:
        start = 5  # Leo

    target = ((start + division - 2) % 12) + 1

    return VimsamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "vimsamsa",
]
