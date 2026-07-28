"""
Chaturvimshamsa (D24) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class ChaturvimshamsaPosition:
    """
    Position in the Chaturvimshamsa (D24) chart.

    Attributes
    ----------
    sign
        D24 sign.

    division
        Division number (1–24).
    """

    sign: ZodiacSign
    division: int
