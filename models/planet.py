"""
Planet model.
Compatible with Python 3.9
"""

from dataclasses import dataclass


@dataclass
class Planet:
    name: str

    longitude: float
    latitude: float
    distance: float
    speed: float

    retrograde: bool = False

    sign: str = ""
    sign_number: int = 0
    sign_degree: float = 0.0

    nakshatra: str = ""
    pada: int = 0
    nakshatra_lord: str = ""

    house: int = 0