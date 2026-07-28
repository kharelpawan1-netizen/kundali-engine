"""
Vimsamsa (D20) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class VimsamsaPosition:
    """
    Position in the Vimsamsa (D20) chart.

    Attributes
    ----------
    sign
        D20 sign.

    division
        Division number (1–20).
    """

    sign: ZodiacSign
    division: int
