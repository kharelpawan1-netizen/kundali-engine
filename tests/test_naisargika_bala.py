"""
Tests for Naisargika Bala.

According to Brihat Parashara Hora Shastra (BPHS).
"""

from astronomy.naisargika_bala import naisargika_bala
from models.graha import Graha


def test_sun():
    assert naisargika_bala(Graha.SUN) == 60.0


def test_moon():
    assert naisargika_bala(Graha.MOON) == 51.43


def test_venus():
    assert naisargika_bala(Graha.VENUS) == 42.86


def test_jupiter():
    assert naisargika_bala(Graha.JUPITER) == 34.29


def test_mercury():
    assert naisargika_bala(Graha.MERCURY) == 25.71


def test_mars():
    assert naisargika_bala(Graha.MARS) == 17.14


def test_saturn():
    assert naisargika_bala(Graha.SATURN) == 8.57
