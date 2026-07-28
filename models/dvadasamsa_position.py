"""
Dvadasamsa (D12) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class DvadasamsaPosition:
    """
    Position in the Dvadasamsa (D12) chart.

    Attributes
    ----------
    sign
        D12 sign.

    division
        Division number (1–12).
    """

    sign: ZodiacSign
    division: int
