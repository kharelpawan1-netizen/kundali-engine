"""
models/dignity.py

Planetary dignity models.

Represents the classical BPHS dignity
of a planet.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from models.graha import Graha
from models.zodiac import ZodiacSign


class Dignity(Enum):
    """Planetary dignity."""

    EXALTED = "Exalted"

    DEBILITATED = "Debilitated"

    MOOLATRIKONA = "Moolatrikona"

    OWN = "Own Sign"

    FRIEND = "Friend"

    NEUTRAL = "Neutral"

    ENEMY = "Enemy"


@dataclass(frozen=True)
class PlanetaryDignity:
    """
    Complete dignity information.
    """

    graha: Graha

    sign: ZodiacSign

    dignity: Dignity

    exact_degree: float

    is_exalted: bool

    is_debilitated: bool

    is_own_sign: bool

    is_moolatrikona: bool
