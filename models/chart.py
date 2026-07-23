"""
models/chart.py

Birth chart model.
Compatible with Python 3.9
"""

from dataclasses import dataclass, field
from typing import Dict

from models.planet import Planet


@dataclass
class BirthChart:
    """
    Complete horoscope.
    """

    # Basic astronomical data
    julian_day: float
    ayanamsa: float

    # Ascendant
    ascendant: float = 0.0
    ascendant_sign: str = ""

    # Midheaven
    mc: float = 0.0

    # Planet data
    planets: Dict[str, Planet] = field(default_factory=dict)

    # House cusps
    house_cusps: Dict[int, float] = field(default_factory=dict)