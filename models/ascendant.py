"""
models/ascendant.py

Ascendant (Lagna) model.

Version:
    1.0.0
"""

from __future__ import annotations

from dataclasses import dataclass

from models.nakshatra import Nakshatra
from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class Ascendant:
    """
    Represents the astronomical Ascendant (Lagna).
    """

    longitude: float

    sign: ZodiacSign

    degree_in_sign: float

    nakshatra: Nakshatra

    pada: int
