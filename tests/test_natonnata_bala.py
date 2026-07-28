"""
Tests for Natonnata Bala.
"""

from astronomy.natonnata_bala import natonnata_bala
from models.graha import Graha


def test_day_sun():
    assert natonnata_bala(Graha.SUN, True).value == 60.0


def test_day_moon():
    assert natonnata_bala(Graha.MOON, True).value == 0.0


def test_night_moon():
    assert natonnata_bala(Graha.MOON, False).value == 60.0


def test_night_sun():
    assert natonnata_bala(Graha.SUN, False).value == 0.0


def test_day_jupiter():
    assert natonnata_bala(Graha.JUPITER, True).value == 60.0


def test_night_venus():
    assert natonnata_bala(Graha.VENUS, False).value == 60.0


def test_mercury_day():
    assert natonnata_bala(Graha.MERCURY, True).value == 60.0


def test_mercury_night():
    assert natonnata_bala(Graha.MERCURY, False).value == 60.0
