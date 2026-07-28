"""
Bhamsa (D27) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class BhamsaPosition:
    """
    Position in the Bhamsa (D27) chart.

    Attributes
    ----------
    sign
        D27 sign.

    division
        Division number (1–27).
    """

    sign: ZodiacSign
    division: int
