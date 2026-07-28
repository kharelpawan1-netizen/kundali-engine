"""
Dasamsa (D10) position model.

According to Brihat Parashara Hora Shastra.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class DasamsaPosition:
    """
    Position in the Dasamsa (D10) chart.

    Attributes
    ----------
    sign
        D10 sign.

    division
        Dasamsa division (1–10).
    """

    sign: ZodiacSign
    division: int
