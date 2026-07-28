"""
Varga Position model.

Represents the result of a divisional-chart calculation.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class VargaPosition:
    """
    Position of a planet in a divisional chart.
    """

    sign: ZodiacSign

    degree_in_sign: float
