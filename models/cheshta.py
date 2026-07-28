"""
Cheshta (motion) state.

According to Brihat Parashara Hora Shastra (BPHS).

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from enum import Enum


class CheshtaState(Enum):
    """
    Planetary motion state.
    """

    RETROGRADE = "Retrograde"

    DIRECT = "Direct"

    STATIONARY = "Stationary"

    def __str__(self) -> str:
        return self.value
