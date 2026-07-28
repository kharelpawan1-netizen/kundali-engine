"""
Temporary (Tatkalika) planetary relationships.

According to BPHS.
"""

from __future__ import annotations

from models.relationship import Relationship
from models.zodiac import ZodiacSign

# ---------------------------------------------------------------------
# Temporary Friendship Houses (BPHS)
# ---------------------------------------------------------------------

TEMPORARY_FRIEND_HOUSES = {
    2,
    3,
    4,
    10,
    11,
    12,
}

TEMPORARY_ENEMY_HOUSES = {
    1,
    5,
    6,
    7,
    8,
    9,
}


def relative_house(
    source_sign: int,
    target_sign: int,
) -> int:
    """
    Return the relative house from one sign to another.
    """

    return ((target_sign - source_sign) % 12) + 1


def temporary_relationship(
    source_sign: ZodiacSign,
    target_sign: ZodiacSign,
) -> Relationship:
    """
    Return the temporary (Tatkalika) relationship
    according to BPHS.
    """

    house = relative_house(
        source_sign.number,
        target_sign.number,
    )

    if house in TEMPORARY_FRIEND_HOUSES:
        return Relationship.FRIEND

    return Relationship.ENEMY
