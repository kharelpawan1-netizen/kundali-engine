"""
astrology/signs.py

Classical Rashi (zodiac sign) knowledge for the Kundali Engine.

This module provides structural astrological properties of the
twelve Rashis used in Parashari/Vedic astrology.

It does not perform longitude calculations. Astronomical sign
calculation belongs to astronomy.signs.

Python Version:
    3.9+

Author:
    Kundali Engine

License:
    MIT
"""

from __future__ import annotations

from typing import Dict

from models.element import Element
from models.zodiac import ZodiacSign


# ---------------------------------------------------------------------
# Rashi Lords
# ---------------------------------------------------------------------

RASHI_LORDS: Dict[ZodiacSign, str] = {
    ZodiacSign.ARIES: "Mars",
    ZodiacSign.TAURUS: "Venus",
    ZodiacSign.GEMINI: "Mercury",
    ZodiacSign.CANCER: "Moon",
    ZodiacSign.LEO: "Sun",
    ZodiacSign.VIRGO: "Mercury",
    ZodiacSign.LIBRA: "Venus",
    ZodiacSign.SCORPIO: "Mars",
    ZodiacSign.SAGITTARIUS: "Jupiter",
    ZodiacSign.CAPRICORN: "Saturn",
    ZodiacSign.AQUARIUS: "Saturn",
    ZodiacSign.PISCES: "Jupiter",
}


# ---------------------------------------------------------------------
# Rashi Elements
# ---------------------------------------------------------------------

RASHI_ELEMENTS: Dict[ZodiacSign, Element] = {
    ZodiacSign.ARIES: Element.FIRE,
    ZodiacSign.TAURUS: Element.EARTH,
    ZodiacSign.GEMINI: Element.AIR,
    ZodiacSign.CANCER: Element.WATER,
    ZodiacSign.LEO: Element.FIRE,
    ZodiacSign.VIRGO: Element.EARTH,
    ZodiacSign.LIBRA: Element.AIR,
    ZodiacSign.SCORPIO: Element.WATER,
    ZodiacSign.SAGITTARIUS: Element.FIRE,
    ZodiacSign.CAPRICORN: Element.EARTH,
    ZodiacSign.AQUARIUS: Element.AIR,
    ZodiacSign.PISCES: Element.WATER,
}


# ---------------------------------------------------------------------
# Rashi Modality
# ---------------------------------------------------------------------
#
# Movable (Chara):
#     Aries, Cancer, Libra, Capricorn
#
# Fixed (Sthira):
#     Taurus, Leo, Scorpio, Aquarius
#
# Dual (Dvisvabhava):
#     Gemini, Virgo, Sagittarius, Pisces
# ---------------------------------------------------------------------

MOVABLE_SIGNS = frozenset(
    {
        ZodiacSign.ARIES,
        ZodiacSign.CANCER,
        ZodiacSign.LIBRA,
        ZodiacSign.CAPRICORN,
    }
)

FIXED_SIGNS = frozenset(
    {
        ZodiacSign.TAURUS,
        ZodiacSign.LEO,
        ZodiacSign.SCORPIO,
        ZodiacSign.AQUARIUS,
    }
)

DUAL_SIGNS = frozenset(
    {
        ZodiacSign.GEMINI,
        ZodiacSign.VIRGO,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.PISCES,
    }
)


# ---------------------------------------------------------------------
# Rashi Gender
# ---------------------------------------------------------------------
#
# Odd signs are traditionally masculine.
# Even signs are traditionally feminine.
# ---------------------------------------------------------------------

MASCULINE_SIGNS = frozenset(
    {
        ZodiacSign.ARIES,
        ZodiacSign.GEMINI,
        ZodiacSign.LEO,
        ZodiacSign.LIBRA,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.AQUARIUS,
    }
)

FEMININE_SIGNS = frozenset(
    {
        ZodiacSign.TAURUS,
        ZodiacSign.CANCER,
        ZodiacSign.VIRGO,
        ZodiacSign.SCORPIO,
        ZodiacSign.CAPRICORN,
        ZodiacSign.PISCES,
    }
)


# ---------------------------------------------------------------------
# Rashi Classification Helpers
# ---------------------------------------------------------------------


def rashi_lord(sign: ZodiacSign) -> str:
    """
    Return the classical lord of a Rashi.

    Parameters
    ----------
    sign
        Zodiac sign.

    Returns
    -------
    str
        Planetary lord.
    """

    try:
        return RASHI_LORDS[sign]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported zodiac sign: {sign}"
        ) from exc


def rashi_element(sign: ZodiacSign) -> Element:
    """
    Return the element associated with a Rashi.
    """

    try:
        return RASHI_ELEMENTS[sign]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported zodiac sign: {sign}"
        ) from exc


def is_movable(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi is Chara (Movable).
    """

    return sign in MOVABLE_SIGNS


def is_fixed(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi is Sthira (Fixed).
    """

    return sign in FIXED_SIGNS


def is_dual(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi is Dvisvabhava (Dual).
    """

    return sign in DUAL_SIGNS


def is_masculine(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi is traditionally masculine.
    """

    return sign in MASCULINE_SIGNS


def is_feminine(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi is traditionally feminine.
    """

    return sign in FEMININE_SIGNS


def is_odd(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi number is odd.
    """

    return sign.number % 2 == 1


def is_even(sign: ZodiacSign) -> bool:
    """
    Return True if the Rashi number is even.
    """

    return sign.number % 2 == 0


# ---------------------------------------------------------------------
# Modality
# ---------------------------------------------------------------------


def rashi_modality(sign: ZodiacSign) -> str:
    """
    Return the classical modality of the Rashi.

    Returns
    -------
    str
        One of:

        - "Movable"
        - "Fixed"
        - "Dual"
    """

    if is_movable(sign):
        return "Movable"

    if is_fixed(sign):
        return "Fixed"

    if is_dual(sign):
        return "Dual"

    raise ValueError(
        f"Unsupported zodiac sign: {sign}"
    )


# ---------------------------------------------------------------------
# Element Convenience Helpers
# ---------------------------------------------------------------------


def is_fire_sign(sign: ZodiacSign) -> bool:
    """Return True if the Rashi is a Fire sign."""

    return rashi_element(sign) is Element.FIRE


def is_earth_sign(sign: ZodiacSign) -> bool:
    """Return True if the Rashi is an Earth sign."""

    return rashi_element(sign) is Element.EARTH


def is_air_sign(sign: ZodiacSign) -> bool:
    """Return True if the Rashi is an Air sign."""

    return rashi_element(sign) is Element.AIR


def is_water_sign(sign: ZodiacSign) -> bool:
    """Return True if the Rashi is a Water sign."""

    return rashi_element(sign) is Element.WATER


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

__all__ = [
    "RASHI_LORDS",
    "RASHI_ELEMENTS",
    "MOVABLE_SIGNS",
    "FIXED_SIGNS",
    "DUAL_SIGNS",
    "MASCULINE_SIGNS",
    "FEMININE_SIGNS",
    "rashi_lord",
    "rashi_element",
    "is_movable",
    "is_fixed",
    "is_dual",
    "is_masculine",
    "is_feminine",
    "is_odd",
    "is_even",
    "rashi_modality",
    "is_fire_sign",
    "is_earth_sign",
    "is_air_sign",
    "is_water_sign",
]