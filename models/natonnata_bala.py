"""
Natonnata Bala model.

Represents Natonnata Bala (diurnal/nocturnal strength)
according to Brihat Parashara Hora Shastra.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NatonnataBala:
    """
    Natonnata Bala expressed in Shastiamsas.

    Attributes
    ----------
    value
        Strength in Shastiamsas (0–60).
    """

    value: float
