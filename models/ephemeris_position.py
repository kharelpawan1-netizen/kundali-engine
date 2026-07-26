"""
Swiss Ephemeris Position Model.

This module defines the immutable result returned by the Swiss
Ephemeris wrapper.

The model represents one astronomical body's computed position at
a specific Julian Day.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EphemerisPosition:
    """
    Astronomical position returned by Swiss Ephemeris.

    Attributes
    ----------
    longitude
        Sidereal longitude in degrees.

    latitude
        Ecliptic latitude in degrees.

    distance
        Distance from Earth (AU).

    longitude_speed
        Daily longitudinal speed.

    latitude_speed
        Daily latitudinal speed.

    distance_speed
        Daily distance change.

    retrograde
        True if longitude speed is negative.
    """

    longitude: float

    latitude: float

    distance: float

    longitude_speed: float

    latitude_speed: float

    distance_speed: float

    retrograde: bool
