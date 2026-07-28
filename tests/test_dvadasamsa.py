"""
Tests for Dvadasamsa (D12).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.dvadasamsa import dvadasamsa
from models.zodiac import ZodiacSign


def test_aries_first_dvadasamsa():
    """
    Aries 1° -> Aries.
    """

    result = dvadasamsa(1.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_dvadasamsa():
    """
    Aries 3° -> Taurus.
    """

    result = dvadasamsa(3.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_dvadasamsa():
    """
    Aries 29° -> Pisces.
    """

    result = dvadasamsa(29.0)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 12


def test_taurus_first_dvadasamsa():
    """
    Taurus begins from Taurus.
    """

    result = dvadasamsa(31.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 1


def test_taurus_second_dvadasamsa():
    """
    Taurus second division -> Gemini.
    """

    result = dvadasamsa(33.0)

    assert result.sign == ZodiacSign.GEMINI
    assert result.division == 2


def test_taurus_last_dvadasamsa():
    """
    Taurus last division -> Aries.
    """

    result = dvadasamsa(59.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 12


def test_boundary_two_point_five():
    """
    Exactly 2.5° begins second division.
    """

    result = dvadasamsa(2.5)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_boundary_twenty_seven_point_five():
    """
    Exactly 27.5° begins twelfth division.
    """

    result = dvadasamsa(27.5)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 12


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = dvadasamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude greater than 360.
    """

    result = dvadasamsa(361.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = dvadasamsa(-1.0)

    assert result.sign == ZodiacSign.AQUARIUS
    assert result.division == 12


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = dvadasamsa(359.999)

    assert result.sign == ZodiacSign.AQUARIUS
    assert result.division == 12
