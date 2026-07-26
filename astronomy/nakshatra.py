"""
astronomy/nakshatra.py

Nakshatra calculations for the Kundali Engine.

This module converts a sidereal longitude into Nakshatra
information according to the classical 27-Nakshatra system.

Python Version:
    3.9+

Author:
    Kundali Engine

License:
    MIT
"""

from __future__ import annotations

from astronomy.signs import mod360
from models.nakshatra import NakshatraInfo

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

TOTAL_NAKSHATRAS = 27

PADA_PER_NAKSHATRA = 4

NAKSHATRA_SIZE = 360.0 / TOTAL_NAKSHATRAS

PADA_SIZE = NAKSHATRA_SIZE / PADA_PER_NAKSHATRA


# ---------------------------------------------------------------------
# Nakshatra Names
# ---------------------------------------------------------------------

NAKSHATRA_NAMES = (
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
)


# ---------------------------------------------------------------------
# Nakshatra Lords
# ---------------------------------------------------------------------

NAKSHATRA_LORDS = (
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",
)


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------


def validate_longitude(longitude: float) -> float:
    """
    Validate and normalize longitude.

    Returns
    -------
    float
        Longitude normalized to:

            0 <= longitude < 360
    """

    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be numeric.")

    return mod360(float(longitude))


# ---------------------------------------------------------------------
# Basic Calculations
# ---------------------------------------------------------------------


def nakshatra_number(longitude: float) -> int:
    """
    Return Nakshatra number.

    Ashwini = 1

    Revati = 27
    """

    longitude = validate_longitude(longitude)

    return int(longitude // NAKSHATRA_SIZE) + 1


def nakshatra_name(longitude: float) -> str:
    """
    Return Nakshatra name.
    """

    return NAKSHATRA_NAMES[nakshatra_number(longitude) - 1]


def nakshatra_lord(longitude: float) -> str:
    """
    Return Nakshatra lord.
    """

    index = (nakshatra_number(longitude) - 1) % 9

    return NAKSHATRA_LORDS[index]


# ---------------------------------------------------------------------
# Degree Calculations
# ---------------------------------------------------------------------


def nakshatra_degree(longitude: float) -> float:
    """
    Return the degree within the Nakshatra.

    Examples
    --------
    Ashwini:
        5°00' Aries -> 5.0

    Bharani:
        15° Aries -> 1.666...
    """

    longitude = validate_longitude(longitude)

    return longitude % NAKSHATRA_SIZE


def nakshatra_start(longitude: float) -> float:
    """
    Return the starting longitude of the Nakshatra.
    """

    number = nakshatra_number(longitude)

    return (number - 1) * NAKSHATRA_SIZE


def nakshatra_end(longitude: float) -> float:
    """
    Return the ending longitude of the Nakshatra.
    """

    return nakshatra_start(longitude) + NAKSHATRA_SIZE


# ---------------------------------------------------------------------
# Pada Calculations
# ---------------------------------------------------------------------


def nakshatra_pada(longitude: float) -> int:
    """
    Return the Nakshatra Pada.

    Returns
    -------
    int
        Value from 1 to 4.
    """

    degree = nakshatra_degree(longitude)

    pada = int(degree // PADA_SIZE) + 1

    # Guard against floating-point rounding near boundaries.
    return min(pada, PADA_PER_NAKSHATRA)


# ---------------------------------------------------------------------
# Convenience Helpers
# ---------------------------------------------------------------------


def is_first_pada(longitude: float) -> bool:
    """
    True if the longitude lies in Pada 1.
    """

    return nakshatra_pada(longitude) == 1


def is_second_pada(longitude: float) -> bool:
    """
    True if the longitude lies in Pada 2.
    """

    return nakshatra_pada(longitude) == 2


def is_third_pada(longitude: float) -> bool:
    """
    True if the longitude lies in Pada 3.
    """

    return nakshatra_pada(longitude) == 3


def is_fourth_pada(longitude: float) -> bool:
    """
    True if the longitude lies in Pada 4.
    """

    return nakshatra_pada(longitude) == 4


# ---------------------------------------------------------------------
# Main API
# ---------------------------------------------------------------------


def longitude_to_nakshatra(longitude: float) -> NakshatraInfo:
    """
    Convert a sidereal longitude into a NakshatraInfo object.

    Parameters
    ----------
    longitude : float
        Sidereal longitude in degrees.

    Returns
    -------
    NakshatraInfo
        Complete Nakshatra information.
    """

    longitude = validate_longitude(longitude)

    return NakshatraInfo(
        number=nakshatra_number(longitude),
        name=nakshatra_name(longitude),
        lord=nakshatra_lord(longitude),
        pada=nakshatra_pada(longitude),
        degree=nakshatra_degree(longitude),
        start_degree=nakshatra_start(longitude),
        end_degree=nakshatra_end(longitude),
    )


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

__all__ = [
    "TOTAL_NAKSHATRAS",
    "PADA_PER_NAKSHATRA",
    "NAKSHATRA_SIZE",
    "PADA_SIZE",
    "validate_longitude",
    "nakshatra_number",
    "nakshatra_name",
    "nakshatra_lord",
    "nakshatra_degree",
    "nakshatra_start",
    "nakshatra_end",
    "nakshatra_pada",
    "is_first_pada",
    "is_second_pada",
    "is_third_pada",
    "is_fourth_pada",
    "longitude_to_nakshatra",
]
