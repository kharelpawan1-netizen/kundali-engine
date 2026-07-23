"""
models/house.py

House model for the Kundali Engine.

Represents one astrological house.

Version:
    2.0.0

Compatible with Python 3.9
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class House:
    """
    Represents one astrological house.
    """

    # ---------------------------------------------------------
    # House Number
    # ---------------------------------------------------------

    number: int

    # ---------------------------------------------------------
    # House Beginning Longitude
    # ---------------------------------------------------------

    longitude: float

    # ---------------------------------------------------------
    # Zodiac Sign
    # ---------------------------------------------------------

    sign: str

    sign_number: int

    # ---------------------------------------------------------
    # Planets Occupying the House
    # ---------------------------------------------------------

    planets: List[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Future Calculations
    # ---------------------------------------------------------

    lord: str = ""

    strength: float = 0.0

    benefics: int = 0

    malefics: int = 0

    # ---------------------------------------------------------

    def add_planet(self, planet_name: str):
        """
        Add a planet to this house.
        """

        if planet_name not in self.planets:
            self.planets.append(planet_name)

    def __str__(self):
        """
        Human-readable representation.
        """

        return (
            f"House {self.number}: "
            f"{self.sign}"
        )