"""
Tests for Vimsamsa (D20).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.vimsamsa import vimsamsa
from models.zodiac import ZodiacSign


def test_aries_first_vimsamsa():
    """
    Aries begins from Aries.
    """

    result = vimsamsa(1.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_vimsamsa():
    """
    Aries second division -> Taurus.
    """

    result = vimsamsa(2.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_vimsamsa():
    """
    Aries twentieth division.
    """

    result = vimsamsa(29.9)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 20


def test_taurus_first_vimsamsa():
    """
    Taurus begins from Sagittarius.
    """

    result = vimsamsa(31.0)

    assert result.sign == ZodiacSign.SAGITTARIUS
    assert result.division == 1


def test_taurus_second_vimsamsa():
    """
    Taurus second division.
    """

    result = vimsamsa(32.0)

    assert result.sign == ZodiacSign.CAPRICORN
    assert result.division == 2


def test_taurus_last_vimsamsa():
    """
    Taurus twentieth division.
    """

    result = vimsamsa(59.9)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 20


def test_gemini_first_vimsamsa():
    """
    Gemini begins from Leo.
    """

    result = vimsamsa(61.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_boundary_one_point_five():
    """
    Exactly 1.5° begins second division.
    """

    result = vimsamsa(1.5)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_zero_longitude():
    """
    Zero longitude.
    """

    result = vimsamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    """
    Longitude greater than 360.
    """

    result = vimsamsa(361.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = vimsamsa(-1.0)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 20


def test_last_possible_degree():
    """
    Final longitude.
    """

    result = vimsamsa(359.999)

    assert result.sign == ZodiacSign.PISCES
    assert result.division == 20
