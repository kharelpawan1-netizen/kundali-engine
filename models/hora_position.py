"""
Hora (D2) position model.

Represents a planet's position in the Hora chart
according to Brihat Parashara Hora Shastra.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class HoraPosition:
    """
    Position in Hora (D2).

    Attributes
    ----------
    sign
        Hora sign.

    division
        Hora division (1 or 2).
    """

    sign: ZodiacSign

    division: int
