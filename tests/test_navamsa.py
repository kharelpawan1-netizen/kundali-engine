"""
Tests for Navamsa (D9).

According to the classical Parasara system.
"""

from astronomy.navamsa import navamsa
from models.zodiac import ZodiacSign


def test_aries_first_navamsa():
    """
    Aries 1° -> Aries.
    """

    result = navamsa(1.0)

    assert result.sign is ZodiacSign.ARIES


def test_aries_second_navamsa():
    """
    Aries 4° -> Taurus.
    """

    result = navamsa(4.0)

    assert result.sign is ZodiacSign.TAURUS


def test_aries_last_navamsa():
    """
    Aries 29° -> Sagittarius.
    """

    result = navamsa(29.0)

    assert result.sign is ZodiacSign.SAGITTARIUS


def test_taurus_first_navamsa():
    """
    Taurus begins from Capricorn.
    """

    result = navamsa(31.0)

    assert result.sign is ZodiacSign.CAPRICORN


def test_gemini_first_navamsa():
    """
    Gemini begins from Libra.
    """

    result = navamsa(61.0)

    assert result.sign is ZodiacSign.LIBRA


def test_cancer_first_navamsa():
    """
    Cancer begins from Cancer.
    """

    result = navamsa(91.0)

    assert result.sign is ZodiacSign.CANCER


def test_boundary_first_transition():
    """
    Exactly 3°20′ enters second Navamsa.
    """

    result = navamsa(30.0 / 9.0)

    assert result.sign is ZodiacSign.TAURUS


def test_degree_range():
    """
    Degree must always remain within one sign.
    """

    result = navamsa(17.8)

    assert 0.0 <= result.degree_in_sign < 30.0
