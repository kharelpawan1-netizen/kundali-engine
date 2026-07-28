"""
Navamsa (D9).

According to the classical Parasara system.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.navamsa_position import NavamsaPosition
from models.zodiac import ZodiacSign, sign_from_number

MOVABLE_SIGNS = {
    ZodiacSign.ARIES,
    ZodiacSign.CANCER,
    ZodiacSign.LIBRA,
    ZodiacSign.CAPRICORN,
}

FIXED_SIGNS = {
    ZodiacSign.TAURUS,
    ZodiacSign.LEO,
    ZodiacSign.SCORPIO,
    ZodiacSign.AQUARIUS,
}

DUAL_SIGNS = {
    ZodiacSign.GEMINI,
    ZodiacSign.VIRGO,
    ZodiacSign.SAGITTARIUS,
    ZodiacSign.PISCES,
}


def navamsa(
    longitude: float,
) -> NavamsaPosition:
    """
    Compute Navamsa (D9).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    NavamsaPosition
    """

    sign_number = int(longitude // 30) + 1

    sign = sign_from_number(sign_number)

    degree = longitude % 30.0

    navamsa_index = int(degree // (30.0 / 9.0))

    if sign in MOVABLE_SIGNS:
        start = sign.number

    elif sign in FIXED_SIGNS:
        start = ((sign.number + 8 - 1) % 12) + 1

    else:
        start = ((sign.number + 4 - 1) % 12) + 1

    target = ((start + navamsa_index - 1) % 12) + 1

    return NavamsaPosition(
        sign=sign_from_number(target),
        degree_in_sign=(degree % (30.0 / 9.0)) * 9.0,
    )


__all__ = [
    "navamsa",
]
