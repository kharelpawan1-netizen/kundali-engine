"""
models/element.py

Element enumeration for the Kundali Engine.

Python Version:
    3.9+

Author:
    Kundali Engine

License:
    MIT
"""

from enum import Enum


class Element(Enum):
    """
    Zodiac element.
    """

    FIRE = "Fire"
    EARTH = "Earth"
    AIR = "Air"
    WATER = "Water"

    def __str__(self) -> str:
        return self.value
