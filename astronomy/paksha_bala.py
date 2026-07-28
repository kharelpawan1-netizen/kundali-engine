"""
Paksha Bala.

According to Brihat Parashara Hora Shastra.

Paksha Bala is computed from the angular separation
between the Sun and Moon.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.paksha_bala import PakshaBala


def moon_phase_angle(
    sun_longitude: float,
    moon_longitude: float,
) -> float:
    """
    Return the Moon's elongation from the Sun.

    Parameters
    ----------
    sun_longitude
        Sidereal longitude of the Sun.

    moon_longitude
        Sidereal longitude of the Moon.

    Returns
    -------
    float
        Phase angle in degrees (0–360).
    """

    return (moon_longitude - sun_longitude) % 360.0


def paksha_bala(
    sun_longitude: float,
    moon_longitude: float,
) -> PakshaBala:
    """
    Compute Paksha Bala of the Moon.

    According to BPHS:
        New Moon  = 0
        Full Moon = 60

    Parameters
    ----------
    sun_longitude
        Sidereal longitude of Sun.

    moon_longitude
        Sidereal longitude of Moon.

    Returns
    -------
    PakshaBala
    """

    phase = moon_phase_angle(
        sun_longitude,
        moon_longitude,
    )

    if phase <= 180.0:
        value = phase / 3.0
    else:
        value = (360.0 - phase) / 3.0

    return PakshaBala(value=value)


__all__ = [
    "moon_phase_angle",
    "paksha_bala",
]
