"""
Tests for Uccha Bala.

According to Brihat Parashara Hora Shastra (BPHS).
"""

from astronomy.uccha_bala import uccha_bala
from models.graha import Graha


def test_sun_debilitation():
    """
    Sun at exact debilitation.
    """

    assert uccha_bala(Graha.SUN, 190.0) == 0.0


def test_sun_exaltation():
    """
    Sun at exact exaltation.
    """

    assert uccha_bala(Graha.SUN, 10.0) == 60.0


def test_moon_debilitation():
    assert uccha_bala(Graha.MOON, 213.0) == 0.0


def test_moon_exaltation():
    assert uccha_bala(Graha.MOON, 33.0) == 60.0


def test_range():
    """
    Every result should lie between 0 and 60.
    """

    value = uccha_bala(
        Graha.MARS,
        125.0,
    )

    assert 0.0 <= value <= 60.0


def test_midpoint():
    """
    Ninety degrees from debilitation should
    produce 30 Shastiamsas.
    """

    assert (
        uccha_bala(
            Graha.SUN,
            280.0,
        )
        == 30.0
    )
