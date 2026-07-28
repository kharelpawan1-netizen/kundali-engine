"""
Akshavedamsa (D45) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class AkshavedamsaPosition:
    """
    Position in the Akshavedamsa (D45) chart.

    Attributes
    ----------
    sign
        D45 sign.

    division
        Division number (1–45).
    """

    sign: ZodiacSign
    division: int
