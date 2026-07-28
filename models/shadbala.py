"""
Shadbala model.

Stores the six classical strengths according to
Brihat Parashara Hora Shastra (BPHS).

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Shadbala:
    """
    Complete Shadbala result for one planet.
    """

    sthana_bala: float

    dig_bala: float

    kala_bala: float

    cheshta_bala: float

    naisargika_bala: float

    drik_bala: float

    @property
    def total_bala(self) -> float:
        """
        Return the total Shadbala.
        """

        return (
            self.sthana_bala
            + self.dig_bala
            + self.kala_bala
            + self.cheshta_bala
            + self.naisargika_bala
            + self.drik_bala
        )
