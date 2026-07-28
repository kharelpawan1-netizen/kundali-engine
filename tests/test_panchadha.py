"""
Tests for Panchadha (compound) planetary relationships.
"""

from astronomy.panchadha import compound_relationship
from models.compound_relationship import CompoundRelationship
from models.graha import Graha
from models.zodiac import ZodiacSign


def test_great_friend():
    """
    Natural Friend + Temporary Friend = Great Friend.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.TAURUS,
            Graha.SUN,
            Graha.MOON,
        )
        == CompoundRelationship.GREAT_FRIEND
    )


def test_great_enemy():
    """
    Natural Enemy + Temporary Enemy = Great Enemy.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.LEO,
            Graha.SUN,
            Graha.SATURN,
        )
        == CompoundRelationship.GREAT_ENEMY
    )


def test_friend():
    """
    Natural Neutral + Temporary Friend = Friend.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.TAURUS,
            Graha.MARS,
            Graha.VENUS,
        )
        == CompoundRelationship.FRIEND
    )


def test_enemy():
    """
    Natural Neutral + Temporary Enemy = Enemy.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.LEO,
            Graha.MARS,
            Graha.VENUS,
        )
        == CompoundRelationship.ENEMY
    )


def test_neutral_friend_enemy():
    """
    Natural Friend + Temporary Enemy = Neutral.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.LEO,
            Graha.SUN,
            Graha.MOON,
        )
        == CompoundRelationship.NEUTRAL
    )


def test_neutral_enemy_friend():
    """
    Natural Enemy + Temporary Friend = Neutral.
    """

    assert (
        compound_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.TAURUS,
            Graha.SUN,
            Graha.SATURN,
        )
        == CompoundRelationship.NEUTRAL
    )
