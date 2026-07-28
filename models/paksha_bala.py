"""
Paksha Bala model.

Represents the Paksha Bala (lunar phase strength)
according to Brihat Parashara Hora Shastra.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PakshaBala:
    """
    Paksha Bala expressed in Shastiamsas.

    Attributes
    ----------
    value
        Strength in Shastiamsas (0–60).
    """

    value: float
