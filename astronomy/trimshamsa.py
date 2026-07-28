"""
Trimshamsa (D30) calculation.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from models.trimshamsa_position import TrimshamsaPosition
from models.zodiac import ZodiacSign


def trimshamsa(
    longitude: float,
) -> TrimshamsaPosition:
    """
    Compute Trimshamsa (D30).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    TrimshamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    odd = sign_number % 2 == 1

    if odd:

        if degree < 5:
            return TrimshamsaPosition(
                sign=ZodiacSign.ARIES,
                ruler="Mars",
                division=1,
            )

        if degree < 10:
            return TrimshamsaPosition(
                sign=ZodiacSign.AQUARIUS,
                ruler="Saturn",
                division=2,
            )

        if degree < 18:
            return TrimshamsaPosition(
                sign=ZodiacSign.SAGITTARIUS,
                ruler="Jupiter",
                division=3,
            )

        if degree < 25:
            return TrimshamsaPosition(
                sign=ZodiacSign.GEMINI,
                ruler="Mercury",
                division=4,
            )

        return TrimshamsaPosition(
            sign=ZodiacSign.LIBRA,
            ruler="Venus",
            division=5,
        )

    if degree < 5:
        return TrimshamsaPosition(
            sign=ZodiacSign.LIBRA,
            ruler="Venus",
            division=1,
        )

    if degree < 12:
        return TrimshamsaPosition(
            sign=ZodiacSign.GEMINI,
            ruler="Mercury",
            division=2,
        )

    if degree < 20:
        return TrimshamsaPosition(
            sign=ZodiacSign.PISCES,
            ruler="Jupiter",
            division=3,
        )

    if degree < 25:
        return TrimshamsaPosition(
            sign=ZodiacSign.AQUARIUS,
            ruler="Saturn",
            division=4,
        )

    return TrimshamsaPosition(
        sign=ZodiacSign.ARIES,
        ruler="Mars",
        division=5,
    )


__all__ = [
    "trimshamsa",
]
