"""
Tests for Drekkana (D3).

According to the classical Parasara system.
"""

from astronomy.drekkana import drekkana
from models.zodiac import ZodiacSign


def test_aries_first_drekkana():
    """
    Aries 5° -> Aries.
    """

    result = drekkana(5.0)

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == 15.0


def test_aries_second_drekkana():
    """
    Aries 15° -> Leo.
    """

    result = drekkana(15.0)

    assert result.sign is ZodiacSign.LEO
    assert result.degree_in_sign == 15.0


def test_aries_third_drekkana():
    """
    Aries 25° -> Sagittarius.
    """

    result = drekkana(25.0)

    assert result.sign is ZodiacSign.SAGITTARIUS
    assert result.degree_in_sign == 15.0


def test_taurus_first_drekkana():
    """
    Taurus 5° -> Taurus.
    """

    result = drekkana(35.0)

    assert result.sign is ZodiacSign.TAURUS
    assert result.degree_in_sign == 15.0


def test_taurus_second_drekkana():
    """
    Taurus 15° -> Virgo.
    """

    result = drekkana(45.0)

    assert result.sign is ZodiacSign.VIRGO
    assert result.degree_in_sign == 15.0


def test_taurus_third_drekkana():
    """
    Taurus 25° -> Capricorn.
    """

    result = drekkana(55.0)

    assert result.sign is ZodiacSign.CAPRICORN
    assert result.degree_in_sign == 15.0


def test_boundary_10_degrees():
    """
    Exactly 10° begins second Drekkana.
    """

    result = drekkana(10.0)

    assert result.sign is ZodiacSign.LEO


def test_boundary_20_degrees():
    """
    Exactly 20° begins third Drekkana.
    """

    result = drekkana(20.0)

    assert result.sign is ZodiacSign.SAGITTARIUS
