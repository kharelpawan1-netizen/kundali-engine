"""
Dig Bala model.

Directional strength according to
Brihat Parashara Hora Shastra (BPHS).

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from enum import Enum


class Direction(Enum):
    """
    Cardinal chart directions.
    """

    EAST = "East"

    SOUTH = "South"

    WEST = "West"

    NORTH = "North"

    def __str__(self) -> str:
        return self.value
