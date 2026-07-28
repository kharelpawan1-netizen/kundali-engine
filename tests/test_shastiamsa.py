"""
Tests for Shastiamsa (D60).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.shastiamsa import shastiamsa
from models.zodiac import ZodiacSign

# -------------------------
# Odd signs
# -------------------------


def test_aries_first_division():
    result = shastiamsa(0.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_division():
    result = shastiamsa(0.6)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_division():
    result = shastiamsa(29.9)

    assert result.division == 60


# -------------------------
# Even signs
# -------------------------


def test_taurus_first_division():
    result = shastiamsa(30.2)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 1


def test_taurus_second_division():
    result = shastiamsa(30.6)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 2


def test_taurus_last_division():
    result = shastiamsa(59.9)

    assert result.division == 60


# -------------------------
# Another odd sign
# -------------------------


def test_gemini_first_division():
    result = shastiamsa(60.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


# -------------------------
# Boundary
# -------------------------


def test_boundary():
    result = shastiamsa(30.0 / 60.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


# -------------------------
# Wraparound
# -------------------------


def test_zero_longitude():
    result = shastiamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    result = shastiamsa(360.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    result = shastiamsa(-1.0)

    assert result.division == 59


def test_last_possible_degree():
    result = shastiamsa(359.999)

    assert result.division == 60
