"""
Tests for Chaturvimshamsa (D24).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.chaturvimshamsa import chaturvimshamsa
from models.zodiac import ZodiacSign


def test_aries_first_division():
    """
    Aries starts from Leo.
    """

    result = chaturvimshamsa(0.5)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_aries_second_division():
    """
    Aries second division -> Virgo.
    """

    result = chaturvimshamsa(1.5)

    assert result.sign == ZodiacSign.VIRGO
    assert result.division == 2


def test_aries_last_division():
    """
    Aries 24th division.
    """

    result = chaturvimshamsa(29.9)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 24


def test_taurus_first_division():
    """
    Taurus starts from Cancer.
    """

    result = chaturvimshamsa(30.5)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 1


def test_taurus_second_division():
    """
    Taurus second division -> Leo.
    """

    result = chaturvimshamsa(31.5)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2


def test_taurus_last_division():
    """
    Taurus 24th division.
    """

    result = chaturvimshamsa(59.9)

    assert result.sign == ZodiacSign.GEMINI
    assert result.division == 24


def test_gemini_first_division():
    """
    Gemini starts from Leo.
    """

    result = chaturvimshamsa(60.5)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_boundary():
    """
    Exactly 1.25° begins second division.
    """

    result = chaturvimshamsa(1.25)

    assert result.sign == ZodiacSign.VIRGO
    assert result.division == 2


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = chaturvimshamsa(0.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_wraparound():
    """
    Longitude greater than 360.
    """

    result = chaturvimshamsa(360.5)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = chaturvimshamsa(-1.0)

    # We'll verify this after running pytest.
    assert result.division == 24


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = chaturvimshamsa(359.999)

    # We'll verify this after running pytest.
    assert result.division == 24
