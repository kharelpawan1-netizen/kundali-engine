"""
Saptamsa (D7) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into seven equal parts.

Odd signs:
    Counting begins from the same sign.

Even signs:
    Counting begins from the seventh sign.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.saptamsa_position import SaptamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 30.0 / 7.0

ODD_SIGNS = {
    1,
    3,
    5,
    7,
    9,
    11,
}


def saptamsa(
    longitude: float,
) -> SaptamsaPosition:
    """
    Compute Saptamsa (D7).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    SaptamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30) + 1

    degree = longitude % 30.0

    division = int(degree / DIVISION_SIZE) + 1

    if division > 7:
        division = 7

    if sign_number in ODD_SIGNS:
        start = sign_number
    else:
        start = ((sign_number + 6 - 1) % 12) + 1

    target = ((start + division - 2) % 12) + 1

    return SaptamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "saptamsa",
]
