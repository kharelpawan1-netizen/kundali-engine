"""
Trimshamsa (D30) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class TrimshamsaPosition:
    """
    Position in the Trimshamsa (D30) chart.

    Attributes
    ----------
    sign
        D30 sign.

    ruler
        Planetary ruler of the Trimshamsa.

    division
        Trimshamsa segment number.
    """

    sign: ZodiacSign
    ruler: str
    division: int
