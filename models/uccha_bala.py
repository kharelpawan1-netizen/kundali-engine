"""
Uccha Bala model.

Exaltation strength according to
Brihat Parashara Hora Shastra (BPHS).

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UcchaBala:
    """
    Exaltation strength.

    Attributes
    ----------
    value
        Strength in Shastiamsas (0–60).
    """

    value: float
