"""
Saptamsa (D7) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class SaptamsaPosition:
    """
    Position in the Saptamsa (D7) chart.

    Attributes
    ----------
    sign
        D7 sign.

    division
        Saptamsa division (1–7).
    """

    sign: ZodiacSign
    division: int
