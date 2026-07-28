"""
Panchadha (Compound) planetary relationships.

Combines natural (Naisargika) and temporary (Tatkalika)
relationships according to BPHS.
"""

from __future__ import annotations

from astronomy.relationships import natural_relationship
from astronomy.tatkalika import temporary_relationship
from models.compound_relationship import CompoundRelationship
from models.relationship import Relationship
from models.zodiac import ZodiacSign


def compound_relationship(
    source_sign: ZodiacSign,
    target_sign: ZodiacSign,
    source_planet,
    target_planet,
) -> CompoundRelationship:
    """
    Return the Panchadha (compound) relationship
    according to BPHS.
    """

    natural = natural_relationship(
        source_planet,
        target_planet,
    )

    temporary = temporary_relationship(
        source_sign,
        target_sign,
    )

    if natural == Relationship.FRIEND and temporary == Relationship.FRIEND:
        return CompoundRelationship.GREAT_FRIEND

    if natural == Relationship.ENEMY and temporary == Relationship.ENEMY:
        return CompoundRelationship.GREAT_ENEMY

    if natural == Relationship.FRIEND and temporary == Relationship.ENEMY:
        return CompoundRelationship.NEUTRAL

    if natural == Relationship.ENEMY and temporary == Relationship.FRIEND:
        return CompoundRelationship.NEUTRAL

    if natural == Relationship.NEUTRAL and temporary == Relationship.FRIEND:
        return CompoundRelationship.FRIEND

    if natural == Relationship.NEUTRAL and temporary == Relationship.ENEMY:
        return CompoundRelationship.ENEMY

    return CompoundRelationship.NEUTRAL
