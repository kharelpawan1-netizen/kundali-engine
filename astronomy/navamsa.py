"""
Navamsa (D9).

According to the classical Parasara system.

Python Version:
3.9+

Author:
Kundali Engine
"""

from __future__ import annotations

import math

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

NAVAMSA_SIZE = 30.0 / 9.0


def navamsa(longitude: float) -> NavamsaPosition:
    """
    Compute the classical Parasari Navamsa (D9) position.

    Parameters
    ----------
    longitude
        Sidereal ecliptic longitude in degrees.

        Longitudes are normalized modulo 360 degrees, so both
        positive and negative angular positions are supported.

    Returns
    -------
    NavamsaPosition
        The Navamsa sign and the degree within that Navamsa sign.

    Notes
    -----
    The zodiac is divided into twelve Rashis of 30 degrees each.
    Every Rashi is divided into nine equal Navamsas of 3°20'
    (10/3 degrees).

    Classical Parasari Navamsa starting-sign rules:

    - Movable signs begin from the same sign.
    - Fixed signs begin from the 9th sign from themselves.
    - Dual signs begin from the 5th sign from themselves.

    The nine Navamsas within each Rashi then proceed sequentially
    through the zodiac.

    Longitude normalization is performed before all other
    calculations:

        normalized_longitude = longitude % 360

    Therefore:

        navamsa(-5.0) == navamsa(355.0)

    and the same equivalence applies to every negative longitude.
    """

    if not math.isfinite(longitude):
        raise ValueError("Longitude must be a finite number.")

    # Normalize every longitude into the standard zodiacal range
    # [0°, 360°). This provides identical behavior for positive
    # wraparound and negative wraparound.
    normalized_longitude = longitude % 360.0

    # Determine the natal Rashi.
    sign_number = int(normalized_longitude // 30.0) + 1
    sign = sign_from_number(sign_number)

    # Degree within the natal Rashi.
    degree = normalized_longitude - (
        (sign_number - 1) * 30.0
    )

    # Determine which of the nine Navamsas contains the degree.
    #
    # Multiplication by 9/30 converts the Rashi degree into
    # a zero-based Navamsa position.
    #
    # The small tolerance protects exact boundaries from harmless
    # floating-point representation errors.
    scaled_degree = (degree * 9.0) / 30.0

    navamsa_index = min(
        8,
        int(math.floor(scaled_degree + 1e-12)),
    )

    # Determine the first Navamsa sign according to the
    # classical Parasari sign classification.
    if sign in MOVABLE_SIGNS:
        start = sign.number

    elif sign in FIXED_SIGNS:
        # 9th sign from the sign itself.
        start = ((sign.number + 8 - 1) % 12) + 1

    elif sign in DUAL_SIGNS:
        # 5th sign from the sign itself.
        start = ((sign.number + 4 - 1) % 12) + 1

    else:
        raise ValueError(
            f"Unsupported zodiac sign: {sign}"
        )

    # Advance sequentially through the zodiac according to the
    # Navamsa index.
    target = (
        (start + navamsa_index - 1) % 12
    ) + 1

    # Convert the position within the natal Navamsa division
    # into degrees within the resulting Navamsa sign.
    degree_in_navamsa = (
        degree - (navamsa_index * NAVAMSA_SIZE)
    ) * 9.0

    # Eliminate harmless floating-point artifacts at boundaries.
    if abs(degree_in_navamsa) < 1e-12:
        degree_in_navamsa = 0.0

    elif abs(degree_in_navamsa - 30.0) < 1e-12:
        degree_in_navamsa = 0.0

    return NavamsaPosition(
        sign=sign_from_number(target),
        degree_in_sign=degree_in_navamsa,
    )
