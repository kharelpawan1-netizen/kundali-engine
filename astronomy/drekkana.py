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
        Sidereal longitude.

    Returns
    -------
    VargaPosition
        Drekkana position.
    """

    sign_number = int(longitude // 30) + 1

    degree = longitude % 30

    part = int(degree // 10)

    if part == 0:
        target = sign_number

    elif part == 1:
        target = ((sign_number + 4 - 1) % 12) + 1

    else:
        target = ((sign_number + 8 - 1) % 12) + 1

    return VargaPosition(
        sign=sign_from_number(target),
        degree_in_sign=(degree % 10.0) * 3.0,
    )


__all__ = [
    "drekkana",
]
