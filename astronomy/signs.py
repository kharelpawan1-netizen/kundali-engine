"""
astronomy/signs.py

Zodiac sign calculations for the Kundali Engine.

This module provides utilities for converting a sidereal
longitude into zodiac sign information.

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
from models.sign_info import SignInfo
from models.zodiac import ZodiacSign

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

TOTAL_SIGNS = 12

DEGREES_PER_SIGN = 30.0

FULL_CIRCLE = 360.0


# ---------------------------------------------------------------------
# Lookup Tables
# ---------------------------------------------------------------------

SIGNS = (
    ZodiacSign.ARIES,
    ZodiacSign.TAURUS,
    ZodiacSign.GEMINI,
    ZodiacSign.CANCER,
    ZodiacSign.LEO,
    ZodiacSign.VIRGO,
    ZodiacSign.LIBRA,
    ZodiacSign.SCORPIO,
    ZodiacSign.SAGITTARIUS,
    ZodiacSign.CAPRICORN,
    ZodiacSign.AQUARIUS,
    ZodiacSign.PISCES,
)


SIGN_TO_ELEMENT: Dict[ZodiacSign, Element] = {
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
# Validation
# ---------------------------------------------------------------------


def mod360(angle: float) -> float:
    """
    Normalize any angle to the range:

        0° <= angle < 360°

    Examples
    --------
    361° -> 1°

    -20° -> 340°

    720° -> 0°
    """

    angle %= FULL_CIRCLE

    if angle < 0:
        angle += FULL_CIRCLE

    return angle


def validate_longitude(longitude: float) -> float:
    """
    Validate and normalize longitude.

    Parameters
    ----------
    longitude : float

    Returns
    -------
    float
        Longitude normalized to
        0 <= longitude < 360
    """

    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be numeric.")

    return mod360(float(longitude))


# ---------------------------------------------------------------------
# Basic Sign Calculations
# ---------------------------------------------------------------------


def sign_number(longitude: float) -> int:
    """
    Return zodiac sign number.

    Aries = 1

    Taurus = 2

    ...

    Pisces = 12
    """

    longitude = validate_longitude(longitude)

    return int(longitude // DEGREES_PER_SIGN) + 1


def sign_enum(longitude: float) -> ZodiacSign:
    """
    Return ZodiacSign enum.
    """

    number = sign_number(longitude)

    return SIGNS[number - 1]


# ---------------------------------------------------------------------
# Sign Properties
# ---------------------------------------------------------------------


def sign_name(longitude: float) -> str:
    """
    Return the zodiac sign name.

    Parameters
    ----------
    longitude : float

    Returns
    -------
    str
    """

    return sign_enum(longitude).display_name


def sign_degree(longitude: float) -> float:
    """
    Return the longitude within a sign.

    Examples
    --------
    145.62° -> 25.62°

    359.90° -> 29.90°
    """

    longitude = validate_longitude(longitude)

    return longitude % DEGREES_PER_SIGN


def sign_start(longitude: float) -> float:
    """
    Return the starting longitude of the sign.

    Examples
    --------
    145° -> 120°

    25° -> 0°
    """

    number = sign_number(longitude)

    return (number - 1) * DEGREES_PER_SIGN


def sign_end(longitude: float) -> float:
    """
    Return the ending longitude of the sign.

    Examples
    --------
    145° -> 150°

    5° -> 30°
    """

    return sign_start(longitude) + DEGREES_PER_SIGN


# ---------------------------------------------------------------------
# Element Helpers
# ---------------------------------------------------------------------


def element(longitude: float) -> Element:
    """
    Return the zodiac element.

    Returns
    -------
    Element
    """

    return sign_enum(longitude).element


def is_fire(longitude: float) -> bool:
    """
    True if longitude lies in a Fire sign.
    """

    return element(longitude) is Element.FIRE


def is_earth(longitude: float) -> bool:
    """
    True if longitude lies in an Earth sign.
    """

    return element(longitude) is Element.EARTH


def is_air(longitude: float) -> bool:
    """
    True if longitude lies in an Air sign.
    """

    return element(longitude) is Element.AIR


def is_water(longitude: float) -> bool:
    """
    True if longitude lies in a Water sign.
    """

    return element(longitude) is Element.WATER


# ---------------------------------------------------------------------
# Main API
# ---------------------------------------------------------------------


def longitude_to_sign(longitude: float) -> SignInfo:
    """
    Convert a zodiac longitude into a SignInfo object.

    Parameters
    ----------
    longitude : float
        Sidereal longitude in degrees.

    Returns
    -------
    SignInfo
        Complete zodiac sign information.
    """

    longitude = validate_longitude(longitude)

    sign = sign_enum(longitude)

    return SignInfo(
        number=sign.number,
        sign=sign,
        degree=sign_degree(longitude),
        start_degree=sign_start(longitude),
        end_degree=sign_end(longitude),
        element=sign.element,
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

__all__ = [
    "TOTAL_SIGNS",
    "DEGREES_PER_SIGN",
    "FULL_CIRCLE",
    "mod360",
    "validate_longitude",
    "sign_number",
    "sign_enum",
    "sign_name",
    "sign_degree",
    "sign_start",
    "sign_end",
    "element",
    "is_fire",
    "is_earth",
    "is_air",
    "is_water",
    "longitude_to_sign",
]
