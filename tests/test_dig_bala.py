"""
Tests for Dig Bala.
"""

from astronomy.dig_bala import (
    DIG_BALA_HOUSE,
    dig_bala,
    strongest_house,
)
from models.graha import Graha


def test_strongest_house_sun():
    assert strongest_house(Graha.SUN) == 10


def test_strongest_house_moon():
    assert strongest_house(Graha.MOON) == 4


def test_strongest_house_mercury():
    assert strongest_house(Graha.MERCURY) == 1


def test_strongest_house_saturn():
    assert strongest_house(Graha.SATURN) == 7


def test_dictionary_matches_function():
    for graha, house in DIG_BALA_HOUSE.items():
        assert strongest_house(graha) == house


def test_maximum_dig_bala():
    assert dig_bala(Graha.SUN, 10) == 60.0
    assert dig_bala(Graha.MOON, 4) == 60.0
    assert dig_bala(Graha.MERCURY, 1) == 60.0
    assert dig_bala(Graha.SATURN, 7) == 60.0


def test_zero_dig_bala():
    assert dig_bala(Graha.SUN, 1) == 0.0
    assert dig_bala(Graha.MOON, 10) == 0.0
    assert dig_bala(Graha.JUPITER, 5) == 0.0
