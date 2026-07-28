"""
Natonnata Bala.

According to Brihat Parashara Hora Shastra.

Natonnata Bala is based on whether the birth is
during the day or night.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.graha import Graha
from models.natonnata_bala import NatonnataBala

DAY_PLANETS = {
    Graha.SUN,
    Graha.JUPITER,
    Graha.SATURN,
}

NIGHT_PLANETS = {
    Graha.MOON,
    Graha.MARS,
    Graha.VENUS,
}

DUAL_PLANET = Graha.MERCURY


def natonnata_bala(
    graha: Graha,
    is_day_birth: bool,
) -> NatonnataBala:
    """
    Compute Natonnata Bala.

    Parameters
    ----------
    graha
        Planet.

    is_day_birth
        True for day birth.
        False for night birth.

    Returns
    -------
    NatonnataBala
    """

    if graha == DUAL_PLANET:
        return NatonnataBala(60.0)

    if is_day_birth:
        if graha in DAY_PLANETS:
            return NatonnataBala(60.0)

        return NatonnataBala(0.0)

    if graha in NIGHT_PLANETS:
        return NatonnataBala(60.0)

    return NatonnataBala(0.0)


__all__ = [
    "natonnata_bala",
]
