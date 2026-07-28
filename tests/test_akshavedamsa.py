"""
Tests for Akshavedamsa (D45).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.akshavedamsa import akshavedamsa
from models.zodiac import ZodiacSign

# -------------------------
# Odd signs
# -------------------------


def test_aries_first_division():
    result = akshavedamsa(0.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_aries_second_division():
    result = akshavedamsa(0.8)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


def test_aries_last_division():
    result = akshavedamsa(29.9)

    assert result.division == 45


# -------------------------
# Even signs
# -------------------------


def test_taurus_first_division():
    result = akshavedamsa(30.2)

    assert result.sign == ZodiacSign.LIBRA
    assert result.division == 1


def test_taurus_second_division():
    result = akshavedamsa(30.8)

    assert result.sign == ZodiacSign.SCORPIO
    assert result.division == 2


def test_taurus_last_division():
    result = akshavedamsa(59.9)

    assert result.division == 45


# -------------------------
# Another odd sign
# -------------------------


def test_gemini_first_division():
    result = akshavedamsa(60.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


# -------------------------
# Boundary
# -------------------------


def test_boundary():
    result = akshavedamsa(30.0 / 45.0)

    assert result.sign == ZodiacSign.TAURUS
    assert result.division == 2


# -------------------------
# Wraparound
# -------------------------


def test_zero_longitude():
    result = akshavedamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    result = akshavedamsa(360.2)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    result = akshavedamsa(-1.0)

    # Verify after running pytest.
    assert result.division == 44


def test_last_possible_degree():
    result = akshavedamsa(359.999)

    assert result.division == 45
