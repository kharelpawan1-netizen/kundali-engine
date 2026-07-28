"""
Tests for Saptamsa (D7).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.saptamsa import saptamsa
from models.zodiac import ZodiacSign


def test_aries_first_saptamsa():
    """
    Aries 2° -> Aries.
    """

    result = saptamsa(2.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_saptamsa():
    """
    Aries 5° -> Taurus.
    """

    result = saptamsa(5.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_saptamsa():
    """
    Aries 29° -> Libra.
    """

    result = saptamsa(29.0)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 7


def test_taurus_first_saptamsa():
    """
    Taurus begins from Scorpio.
    """

    result = saptamsa(31.0)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 1


def test_taurus_second_saptamsa():
    """
    Taurus second division -> Sagittarius.
    """

    result = saptamsa(35.0)

    assert result.sign == ZodiacSign.SAGITTARIUS
    assert result.division == 2


def test_taurus_last_saptamsa():
    """
    Taurus last division -> Taurus.
    """

    result = saptamsa(59.5)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 7


def test_boundary_first():
    """
    Exactly one division boundary.
    """

    result = saptamsa(30.0 / 7.0)

    assert result.division == 2


def test_boundary_second():
    """
    Second boundary.
    """

    result = saptamsa((30.0 / 7.0) * 2)

    assert result.division == 3


def test_zero_degree():
    """
    Zero longitude.
    """

    result = saptamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude >360.
    """

    result = saptamsa(362.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.

    -1° is equivalent to 359°, which lies in Pisces
    in the 7th Saptamsa.
    """

    result = saptamsa(-1.0)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 7


def test_last_possible_degree():
    """
    Final degree of zodiac.
    """

    result = saptamsa(359.999)

    assert result.division == 7
