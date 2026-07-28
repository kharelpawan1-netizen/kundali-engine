"""
Dvadasamsa (D12) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into twelve equal parts.

Every sign begins counting from itself.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.dvadasamsa_position import DvadasamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 2.5


def dvadasamsa(
    longitude: float,
) -> DvadasamsaPosition:
    """
    Compute Dvadasamsa (D12).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    DvadasamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 12:
        division = 12

    target = ((sign_number + division - 2) % 12) + 1

    return DvadasamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "dvadasamsa",
]
