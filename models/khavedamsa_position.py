"""
Khavedamsa (D40) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class KhavedamsaPosition:
    """
    Position in the Khavedamsa (D40) chart.

    Attributes
    ----------
    sign
        D40 sign.

    division
        Division number (1–40).
    """

    sign: ZodiacSign
    division: int
