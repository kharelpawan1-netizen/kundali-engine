"""
models/chart.py

Complete birth chart model for the Kundali Engine.

Stores every calculated value of a horoscope.

Version:
    2.0.0

Compatible with Python 3.9
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from models.birth_data import BirthData
from models.planet import Planet
from models.house import House


@dataclass
class BirthChart:
    """
    Complete horoscope.

    This class is the central object returned by
    HoroscopeEngine after all calculations are complete.
    """

    # ---------------------------------------------------------
    # Input Data
    # ---------------------------------------------------------

    birth_data: Optional[BirthData] = None

    # ---------------------------------------------------------
    # Astronomical Data
    # ---------------------------------------------------------

    julian_day: float = 0.0

    ayanamsa: float = 0.0

    # ---------------------------------------------------------
    # Ascendant
    # ---------------------------------------------------------

    ascendant: float = 0.0

    ascendant_sign: str = ""

    ascendant_degree: float = 0.0

    # ---------------------------------------------------------
    # Midheaven
    # ---------------------------------------------------------

    midheaven: float = 0.0

    # ---------------------------------------------------------
    # Horoscope Data
    # ---------------------------------------------------------

    planets: Dict[str, Planet] = field(default_factory=dict)

    houses: Dict[int, House] = field(default_factory=dict)

    # ---------------------------------------------------------
    # Future Modules
    # ---------------------------------------------------------

    yogas: list = field(default_factory=list)

    dashas: list = field(default_factory=list)

    divisional_charts: dict = field(default_factory=dict)

    # ---------------------------------------------------------

    def add_planet(self, planet: Planet):
        """
        Add a planet to the chart.
        """

        self.planets[planet.name] = planet

    def add_house(self, house: House):
        """
        Add a house to the chart.
        """

        self.houses[house.number] = house

    def get_planet(self, name: str):
        """
        Returns a planet by name.
        """

        return self.planets.get(name)

    def get_house(self, number: int):
        """
        Returns a house.
        """

        return self.houses.get(number)

    def __str__(self):
        """
        Human-readable representation.
        """

        return (
            f"BirthChart("
            f"{len(self.planets)} planets, "
            f"{len(self.houses)} houses)"
        )