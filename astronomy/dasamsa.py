"""
Dasamsa (D10) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into ten equal parts.

Odd signs:
    Counting begins from the same sign.

Even signs:
    Counting begins from the ninth sign.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.dasamsa_position import DasamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 3.0

ODD_SIGNS = {
    1,
    3,
    5,
    7,
    9,
    11,
}


def dasamsa(
    longitude: float,
) -> DasamsaPosition:
    """
    Compute Dasamsa (D10).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    DasamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 10:
        division = 10

    if sign_number in ODD_SIGNS:
        start = sign_number
    else:
        # 9th sign from the sign itself
        start = ((sign_number + 8 - 1) % 12) + 1

    target = ((start + division - 2) % 12) + 1

    return DasamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "dasamsa",
]
