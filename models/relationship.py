"""
Planetary relationship types.

According to BPHS.
"""

from enum import Enum


class Relationship(Enum):
    FRIEND = "Friend"
    NEUTRAL = "Neutral"
    ENEMY = "Enemy"
