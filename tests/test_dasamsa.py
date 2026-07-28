"""
Tests for Dasamsa (D10).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.dasamsa import dasamsa
from models.zodiac import ZodiacSign


def test_aries_first_dasamsa():
    """
    Aries 1° -> Aries.
    """

    result = dasamsa(1.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_dasamsa():
    """
    Aries 4° -> Taurus.
    """

    result = dasamsa(4.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_dasamsa():
    """
    Aries 29° -> Capricorn.
    """

    result = dasamsa(29.0)

    assert result.sign == ZodiacSign.CAPRICORN
    assert result.division == 10


def test_taurus_first_dasamsa():
    """
    Taurus starts from Capricorn.
    """

    result = dasamsa(31.0)

    assert result.sign == ZodiacSign.CAPRICORN
    assert result.division == 1


def test_taurus_second_dasamsa():
    """
    Taurus second division -> Aquarius.
    """

    result = dasamsa(34.0)

    assert result.sign == ZodiacSign.AQUARIUS
    assert result.division == 2


def test_taurus_last_dasamsa():
    """
    Taurus last division -> Libra.
    """

    result = dasamsa(59.0)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 10


def test_boundary_three_degrees():
    """
    Exactly 3° begins second Dasamsa.
    """

    result = dasamsa(3.0)

    assert result.division == 2
    assert result.sign == ZodiacSign.TAURUS


def test_boundary_twenty_seven_degrees():
    """
    Exactly 27° begins tenth Dasamsa.
    """

    result = dasamsa(27.0)

    assert result.division == 10
    assert result.sign == ZodiacSign.CAPRICORN


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = dasamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude >360.
    """

    result = dasamsa(361.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = dasamsa(-1.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 10


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = dasamsa(359.999)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 10
