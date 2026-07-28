"""
Shodasamsa (D16) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class ShodasamsaPosition:
    """
    Position in the Shodasamsa (D16) chart.

    Attributes
    ----------
    sign
        D16 sign.

    division
        Division number (1–16).
    """

    sign: ZodiacSign
    division: int
