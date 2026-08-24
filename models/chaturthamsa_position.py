"""
Chaturthamsa (D4) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class ChaturthamsaPosition:
    """
    Position in the Chaturthamsa (D4) chart.

    Attributes
    ----------
    sign
        D4 sign.

    division
        Chaturthamsa division (1–4).
    """

    sign: ZodiacSign
    division: int
