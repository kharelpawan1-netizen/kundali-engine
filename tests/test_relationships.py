"""
Tests for natural planetary relationships.
"""

from astronomy.relationships import relationship
from models.graha import Graha
from models.relationship import Relationship


def test_sun_friends():
    assert relationship(Graha.SUN, Graha.MOON) == Relationship.FRIEND
    assert relationship(Graha.SUN, Graha.MARS) == Relationship.FRIEND
    assert relationship(Graha.SUN, Graha.JUPITER) == Relationship.FRIEND


def test_sun_enemies():
    assert relationship(Graha.SUN, Graha.VENUS) == Relationship.ENEMY
    assert relationship(Graha.SUN, Graha.SATURN) == Relationship.ENEMY


def test_sun_neutral():
    assert relationship(Graha.SUN, Graha.MERCURY) == Relationship.NEUTRAL


def test_moon_relationships():
    assert relationship(Graha.MOON, Graha.SUN) == Relationship.FRIEND
    assert relationship(Graha.MOON, Graha.MERCURY) == Relationship.FRIEND
    assert relationship(Graha.MOON, Graha.MARS) == Relationship.NEUTRAL


def test_mars_relationships():
    assert relationship(Graha.MARS, Graha.JUPITER) == Relationship.FRIEND
    assert relationship(Graha.MARS, Graha.MERCURY) == Relationship.ENEMY
    assert relationship(Graha.MARS, Graha.VENUS) == Relationship.NEUTRAL


def test_mercury_relationships():
    assert relationship(Graha.MERCURY, Graha.SUN) == Relationship.FRIEND
    assert relationship(Graha.MERCURY, Graha.MOON) == Relationship.ENEMY
    assert relationship(Graha.MERCURY, Graha.JUPITER) == Relationship.NEUTRAL


def test_jupiter_relationships():
    assert relationship(Graha.JUPITER, Graha.SUN) == Relationship.FRIEND
    assert relationship(Graha.JUPITER, Graha.VENUS) == Relationship.ENEMY
    assert relationship(Graha.JUPITER, Graha.SATURN) == Relationship.NEUTRAL


def test_venus_relationships():
    assert relationship(Graha.VENUS, Graha.MERCURY) == Relationship.FRIEND
    assert relationship(Graha.VENUS, Graha.SUN) == Relationship.ENEMY
    assert relationship(Graha.VENUS, Graha.JUPITER) == Relationship.NEUTRAL


def test_saturn_relationships():
    assert relationship(Graha.SATURN, Graha.VENUS) == Relationship.FRIEND
    assert relationship(Graha.SATURN, Graha.SUN) == Relationship.ENEMY
    assert relationship(Graha.SATURN, Graha.JUPITER) == Relationship.NEUTRAL
