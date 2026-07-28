"""
astronomy/dignity.py

Planetary dignity calculations
according to BPHS.
"""

from __future__ import annotations

from models.graha import Graha
from models.zodiac import ZodiacSign

EXALTATION = {
    Graha.SUN: (ZodiacSign.ARIES, 10.0),
    Graha.MOON: (ZodiacSign.TAURUS, 3.0),
    Graha.MARS: (ZodiacSign.CAPRICORN, 28.0),
    Graha.MERCURY: (ZodiacSign.VIRGO, 15.0),
    Graha.JUPITER: (ZodiacSign.CANCER, 5.0),
    Graha.VENUS: (ZodiacSign.PISCES, 27.0),
    Graha.SATURN: (ZodiacSign.LIBRA, 20.0),
}
DEBILITATION = {
    Graha.SUN: (ZodiacSign.LIBRA, 10.0),
    Graha.MOON: (ZodiacSign.SCORPIO, 3.0),
    Graha.MARS: (ZodiacSign.CANCER, 28.0),
    Graha.MERCURY: (ZodiacSign.PISCES, 15.0),
    Graha.JUPITER: (ZodiacSign.CAPRICORN, 5.0),
    Graha.VENUS: (ZodiacSign.VIRGO, 27.0),
    Graha.SATURN: (ZodiacSign.ARIES, 20.0),
}
OWN_SIGNS = {
    Graha.SUN: (ZodiacSign.LEO,),
    Graha.MOON: (ZodiacSign.CANCER,),
    Graha.MARS: (
        ZodiacSign.ARIES,
        ZodiacSign.SCORPIO,
    ),
    Graha.MERCURY: (
        ZodiacSign.GEMINI,
        ZodiacSign.VIRGO,
    ),
    Graha.JUPITER: (
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.PISCES,
    ),
    Graha.VENUS: (
        ZodiacSign.TAURUS,
        ZodiacSign.LIBRA,
    ),
    Graha.SATURN: (
        ZodiacSign.CAPRICORN,
        ZodiacSign.AQUARIUS,
    ),
}
MOOLATRIKONA = {
    Graha.SUN: ZodiacSign.LEO,
    Graha.MOON: ZodiacSign.TAURUS,
    Graha.MARS: ZodiacSign.ARIES,
    Graha.MERCURY: ZodiacSign.VIRGO,
    Graha.JUPITER: ZodiacSign.SAGITTARIUS,
    Graha.VENUS: ZodiacSign.LIBRA,
    Graha.SATURN: ZodiacSign.AQUARIUS,
}


def is_exalted(
    graha: Graha,
    sign: ZodiacSign,
) -> bool:
    """
    Return True if the planet is exalted.
    """

    exaltation_sign, _ = EXALTATION[graha]

    return sign == exaltation_sign


def is_debilitated(
    graha: Graha,
    sign: ZodiacSign,
) -> bool:
    """
    Return True if the planet is debilitated.
    """

    debilitation_sign, _ = DEBILITATION[graha]

    return sign == debilitation_sign


def is_own_sign(
    graha: Graha,
    sign: ZodiacSign,
) -> bool:
    """
    Return True if the planet occupies one of its own signs.
    """

    return sign in OWN_SIGNS[graha]


def is_moolatrikona(
    graha: Graha,
    sign: ZodiacSign,
) -> bool:
    """
    Return True if the planet occupies its
    Moolatrikona sign.
    """

    return MOOLATRIKONA[graha] == sign


__all__ = [
    "EXALTATION",
    "DEBILITATION",
    "OWN_SIGNS",
    "MOOLATRIKONA",
    "is_exalted",
    "is_debilitated",
    "is_own_sign",
    "is_moolatrikona",
]
