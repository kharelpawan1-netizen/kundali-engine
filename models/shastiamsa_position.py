"""
Shastiamsa (D60) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class ShastiamsaPosition:
    """
    Position in the Shastiamsa (D60) chart.

    Attributes
    ----------
    sign
        D60 sign.

    division
        Division number (1–60).
    """

    sign: ZodiacSign
    division: int
