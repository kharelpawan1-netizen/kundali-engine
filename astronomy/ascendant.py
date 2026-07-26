"""
astronomy/ascendant.py

Ascendant (Lagna) calculations.

This module converts the raw Swiss Ephemeris house
calculation into the project's Ascendant model.

Version:
    1.0.0
"""

from __future__ import annotations

from models.ascendant import Ascendant
from models.location import Location


def ascendant_longitude(
    julian_day: float,
    location: Location,
) -> float:
    """
    Return Ascendant longitude.
    """

    raise NotImplementedError


def ascendant_sign(
    longitude: float,
):
    """
    Return zodiac sign.
    """

    raise NotImplementedError


def ascendant_degree(
    longitude: float,
):
    """
    Return degree inside the sign.
    """

    raise NotImplementedError


def calculate_ascendant(
    julian_day: float,
    location: Location,
) -> Ascendant:
    """
    Calculate complete Ascendant.
    """

    raise NotImplementedError