"""
Tests for Shodasamsa (D16).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.shodasamsa import shodasamsa
from models.zodiac import ZodiacSign


def test_aries_first_shodasamsa():
    """
    Aries begins from Aries.
    """

    result = shodasamsa(1.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_shodasamsa():
    """
    Aries second division -> Taurus.
    """

    result = shodasamsa(2.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_shodasamsa():
    """
    Aries last division -> Cancer.
    """

    result = shodasamsa(29.5)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 16


def test_taurus_first_shodasamsa():
    """
    Taurus begins from Leo.
    """

    result = shodasamsa(31.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_taurus_second_shodasamsa():
    """
    Taurus second division -> Virgo.
    """

    result = shodasamsa(32.0)

    assert result.sign == ZodiacSign.VIRGO
    assert result.division == 2


def test_taurus_last_shodasamsa():
    """
    Taurus last division -> Scorpio.
    """

    result = shodasamsa(59.5)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 16


def test_gemini_first_shodasamsa():
    """
    Gemini begins from Sagittarius.
    """

    result = shodasamsa(61.0)

    assert result.sign == ZodiacSign.SAGITTARIUS
    assert result.division == 1


def test_boundary_first():
    """
    Exactly 1.875° begins second division.
    """

    result = shodasamsa(1.875)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = shodasamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude greater than 360.
    """

    result = shodasamsa(361.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = shodasamsa(-1.0)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 16


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = shodasamsa(359.999)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 16
