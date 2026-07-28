"""
Uccha Bala.

Exaltation strength according to BPHS.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from astronomy.dignity import DEBILITATION
from models.graha import Graha


def uccha_bala(
    graha: Graha,
    longitude: float,
) -> float:
    """
    Compute simplified Uccha Bala.

    Parameters
    ----------
    graha
        Planet.

    longitude
        Sidereal longitude in degrees.

    Returns
    -------
    float
        Strength from 0 to 60 Shastiamsas.
    """

    deb_sign, deb_degree = DEBILITATION[graha]

    deb_longitude = (deb_sign.number - 1) * 30.0 + deb_degree

    distance = (longitude - deb_longitude) % 360.0

    if distance > 180.0:
        distance = 360.0 - distance

    return round(distance / 3.0, 2)


__all__ = [
    "uccha_bala",
]
