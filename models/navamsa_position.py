"""
Navamsa (D9) position model.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from dataclasses import dataclass

from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class NavamsaPosition:
    """
    Represents a Navamsa (D9) position.
    """

    sign: ZodiacSign

    degree_in_sign: float
