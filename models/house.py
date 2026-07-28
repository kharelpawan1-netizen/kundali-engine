from dataclasses import dataclass, field
from typing import List


@dataclass
class House:
    number: int
    longitude: float
    sign: str
    sign_number: int
    planets: List[str] = field(default_factory=list)
    lord: str = ""
    strength: float = 0.0
    benefics: int = 0
    malefics: int = 0

    def add_planet(self, planet_name: str):
        if planet_name not in self.planets:
            self.planets.append(planet_name)

    def __str__(self):
        return f"House {self.number}: {self.sign}"
