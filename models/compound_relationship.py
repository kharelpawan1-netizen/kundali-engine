"""
Compound (Panchadha) planetary relationships.

According to Brihat Parashara Hora Shastra.
"""

from __future__ import annotations

from enum import Enum


class CompoundRelationship(Enum):
    """
    Compound (Panchadha) relationship between two planets.
    """

    GREAT_FRIEND = "Great Friend"

    FRIEND = "Friend"

    NEUTRAL = "Neutral"

    ENEMY = "Enemy"

    GREAT_ENEMY = "Great Enemy"

    def __str__(self) -> str:
        return self.value
