"""
astronomy/ascendant.py

Ascendant (Lagna) calculations.

This module converts the raw Swiss Ephemeris house
calculation into the project's Ascendant model.

Version:
    1.0.0
"""

from __future__ import annotations

from astronomy.nakshatra import (
    longitude_to_nakshatra,
    nakshatra_pada,
)
from astronomy.signs import (
    sign_degree,
    sign_enum,
)
from astronomy.swiss import houses
from models.ascendant import Ascendant
from models.location import Location


def ascendant_longitude(
    julian_day: float,
    location: Location,
) -> float:
    """
    Return Ascendant longitude.
    """

    _, ascmc = houses(
        julian_day,
        location.latitude,
        location.longitude,
    )

    return float(ascmc[0])


def ascendant_sign(
    longitude: float,
):
    """
    Return zodiac sign.
    """

    return sign_enum(longitude)


def ascendant_degree(
    longitude: float,
):
    """
    Return degree inside the sign.
    """

    return sign_degree(longitude)


def calculate_ascendant(
    julian_day: float,
    location: Location,
) -> Ascendant:
    """
    Calculate complete Ascendant.
    """

    longitude = ascendant_longitude(
        julian_day,
        location,
    )

    return Ascendant(
        longitude=longitude,
        sign=ascendant_sign(longitude),
        degree_in_sign=ascendant_degree(longitude),
        nakshatra=longitude_to_nakshatra(longitude),
        pada=nakshatra_pada(longitude),
    )
