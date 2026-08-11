"""
Drekkana (D3).

According to the classical Parasara system.

Python Version:
3.9+

Author:
Kundali Engine
"""

from __future__ import annotations

from models.varga_position import VargaPosition
from models.zodiac import sign_from_number


def drekkana(
    longitude: float,
) -> VargaPosition:
    """
    Compute Drekkana (D3).

    Parameters
    ----------
    longitude
        Sidereal longitude in degrees.

    Returns
    -------
    VargaPosition
        Drekkana position.

    Notes
    -----
    Classical Parashari Drekkana divides every zodiac sign
    into three equal parts of 10 degrees.

    First Drekkana:
        Same sign as the birth sign.

    Second Drekkana:
        Fifth sign from the birth sign.

    Third Drekkana:
        Ninth sign from the birth sign.

    Longitudes are normalized modulo 360 degrees before
    calculating the zodiac sign.
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    part = int(degree // 10.0)

    if part == 0:
        target = sign_number

    elif part == 1:
        target = ((sign_number + 4 - 1) % 12) + 1

    else:
        target = ((sign_number + 8 - 1) % 12) + 1

    degree_in_sign = (degree % 10.0) * 3.0

    return VargaPosition(
        sign=sign_from_number(target),
        degree_in_sign=degree_in_sign,
    )


__all__ = [
    "drekkana",
]
