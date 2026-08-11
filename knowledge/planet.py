"""
knowledge/planet.py

Immutable planetary knowledge model used by the
interpretation engine.

This module stores permanent BPHS knowledge about a
planet. It intentionally contains no calculation logic.

Compatible with Python 3.9.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PlanetFacts:
    """
    Immutable knowledge describing one planet.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    name: str
    sanskrit_name: str

    # ---------------------------------------------------------
    # Natural nature
    # ---------------------------------------------------------

    is_benefic: bool

    gender: str
    element: str
    guna: str
    caste: str
    temperament: str
    dosha: str

    # ---------------------------------------------------------
    # Traditional correspondences
    # ---------------------------------------------------------

    direction: str
    color: str
    metal: str
    gemstone: str
    deity: str
    weekday: str

    # ---------------------------------------------------------
    # Sign ownership
    # ---------------------------------------------------------

    own_signs: Tuple[str, ...]

    exaltation_sign: str
    exaltation_degree: float

    debilitation_sign: str
    debilitation_degree: float

    moolatrikona_sign: str

    # ---------------------------------------------------------
    # Planetary friendships
    # ---------------------------------------------------------

    friends: Tuple[str, ...]
    enemies: Tuple[str, ...]
    neutrals: Tuple[str, ...]

    # ---------------------------------------------------------
    # Natural significations
    # ---------------------------------------------------------

    karakatwas: Tuple[str, ...]
    natural_houses: Tuple[int, ...]

    body_parts: Tuple[str, ...]
    diseases: Tuple[str, ...]
    professions: Tuple[str, ...]

    keywords: Tuple[str, ...]

    @property
    def is_malefic(self) -> bool:
        """
        Convenience property.
        """

        return not self.is_benefic

    def __str__(self) -> str:
        return self.name