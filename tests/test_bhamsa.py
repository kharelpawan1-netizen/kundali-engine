"""
Tests for Bhamsa (D27).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.bhamsa import bhamsa
from models.zodiac import ZodiacSign


def test_aries_first_division():
    """
    Aries starts from Aries.
    """

    result = bhamsa(0.5)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_division():
    """
    Aries second division -> Taurus.
    """

    result = bhamsa(1.2)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_division():
    """
    Aries twenty-seventh division.
    """

    result = bhamsa(29.9)

    assert result.division == 27


def test_taurus_first_division():
    """
    Taurus starts from Libra.
    """

    result = bhamsa(30.5)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 1


def test_taurus_second_division():
    """
    Taurus second division -> Scorpio.
    """

    result = bhamsa(31.2)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 2


def test_taurus_last_division():
    """
    Taurus twenty-seventh division.
    """

    result = bhamsa(59.9)

    assert result.division == 27


def test_gemini_first_division():
    """
    Gemini starts from Aries.
    """

    result = bhamsa(60.5)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_boundary():
    """
    Exactly one division begins division two.
    """

    result = bhamsa(30.0 / 27.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = bhamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude greater than 360.
    """

    result = bhamsa(360.5)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = bhamsa(-1.0)

    assert result.division == 27


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = bhamsa(359.999)

    assert result.division == 27
