"""
Tests for temporary (Tatkalika) planetary relationships.
"""

from astronomy.tatkalika import (
    relative_house,
    temporary_relationship,
)
from models.relationship import Relationship
from models.zodiac import ZodiacSign


def test_relative_house_same():
    """
    Same sign should be the 1st house.
    """

    assert relative_house(1, 1) == 1


def test_relative_house_second():
    """
    Taurus is the 2nd house from Aries.
    """

    assert relative_house(1, 2) == 2


def test_relative_house_twelfth():
    """
    Aries is the 12th house from Taurus.
    """

    assert relative_house(2, 1) == 12


def test_relative_house_eighth():
    """
    Aquarius is the 8th house from Cancer.
    """

    assert relative_house(4, 11) == 8


def test_temporary_friend():
    """
    Aries -> Taurus = 2nd house = Friend.
    """

    assert (
        temporary_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.TAURUS,
        )
        == Relationship.FRIEND
    )


def test_temporary_enemy():
    """
    Aries -> Leo = 5th house = Enemy.
    """

    assert (
        temporary_relationship(
            ZodiacSign.ARIES,
            ZodiacSign.LEO,
        )
        == Relationship.ENEMY
    )
