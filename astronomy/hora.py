"""
Hora (D2) calculation.

According to Brihat Parashara Hora Shastra.

Each sign is divided into two equal parts of 15°.

Odd signs:
    First Hora  -> Leo
    Second Hora -> Cancer

Even signs:
    First Hora  -> Cancer
    Second Hora -> Leo

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.hora_position import HoraPosition
from models.zodiac import sign_from_number

ODD_SIGNS = {
    1,
    3,
    5,
    7,
    9,
    11,
}


def hora(
    longitude: float,
) -> HoraPosition:
    """
    Compute Hora (D2).

    Parameters
    ----------
    longitude
        Sidereal longitude (0°–360°).

    Returns
    -------
    HoraPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30) + 1

    degree = longitude % 30.0

    first_half = degree < 15.0

    if sign_number in ODD_SIGNS:
        target = 5 if first_half else 4
    else:
        target = 4 if first_half else 5

    return HoraPosition(
        sign=sign_from_number(target),
        division=1 if first_half else 2,
    )


__all__ = [
    "hora",
]
