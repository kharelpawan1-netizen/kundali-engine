"""
Tests for Khavedamsa (D40).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.khavedamsa import khavedamsa
from models.zodiac import ZodiacSign

# -------------------------
# Odd signs
# -------------------------


def test_aries_first_division():
    result = khavedamsa(0.3)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_division():
    result = khavedamsa(0.8)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_division():
    result = khavedamsa(29.9)

    assert result.division == 40


# -------------------------
# Even signs
# -------------------------


def test_taurus_first_division():
    result = khavedamsa(30.3)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 1


def test_taurus_second_division():
    result = khavedamsa(30.8)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 2


def test_taurus_last_division():
    result = khavedamsa(59.9)

    assert result.division == 40


# -------------------------
# Another odd sign
# -------------------------


def test_gemini_first_division():
    result = khavedamsa(60.3)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


# -------------------------
# Boundary
# -------------------------


def test_boundary():
    result = khavedamsa(30.0 / 40.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


# -------------------------
# Wraparound
# -------------------------


def test_zero_longitude():
    result = khavedamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    result = khavedamsa(360.3)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    result = khavedamsa(-1.0)

    assert result.division == 39


def test_last_possible_degree():
    result = khavedamsa(359.999)

    assert result.division == 40
