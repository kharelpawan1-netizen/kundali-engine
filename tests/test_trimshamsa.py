"""
Tests for Trimshamsa (D30).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.trimshamsa import trimshamsa
from models.zodiac import ZodiacSign

# -------------------------
# Odd signs
# -------------------------


def test_odd_first_segment():
    result = trimshamsa(1.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.ruler == "Mars"
    assert result.division == 1


def test_odd_second_segment():
    result = trimshamsa(6.0)

    assert result.sign == ZodiacSign.AQUARIUS
    assert result.ruler == "Saturn"
    assert result.division == 2


def test_odd_third_segment():
    result = trimshamsa(12.0)

    assert result.sign == ZodiacSign.SAGITTARIUS
    assert result.ruler == "Jupiter"
    assert result.division == 3


def test_odd_fourth_segment():
    result = trimshamsa(20.0)

    assert result.sign == ZodiacSign.GEMINI
    assert result.ruler == "Mercury"
    assert result.division == 4


def test_odd_fifth_segment():
    result = trimshamsa(27.0)

    assert result.sign == ZodiacSign.LIBRA
    assert result.ruler == "Venus"
    assert result.division == 5


# -------------------------
# Even signs
# -------------------------


def test_even_first_segment():
    result = trimshamsa(31.0)

    assert result.sign == ZodiacSign.LIBRA
    assert result.ruler == "Venus"
    assert result.division == 1


def test_even_second_segment():
    result = trimshamsa(36.0)

    assert result.sign == ZodiacSign.GEMINI
    assert result.ruler == "Mercury"
    assert result.division == 2


def test_even_third_segment():
    result = trimshamsa(43.0)

    assert result.sign == ZodiacSign.PISCES
    assert result.ruler == "Jupiter"
    assert result.division == 3


def test_even_fourth_segment():
    result = trimshamsa(51.0)

    assert result.sign == ZodiacSign.AQUARIUS
    assert result.ruler == "Saturn"
    assert result.division == 4


def test_even_fifth_segment():
    result = trimshamsa(56.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.ruler == "Mars"
    assert result.division == 5


# -------------------------
# Boundaries
# -------------------------


def test_boundary_5_degrees():
    result = trimshamsa(5.0)

    assert result.division == 2


def test_boundary_10_degrees():
    result = trimshamsa(10.0)

    assert result.division == 3


def test_boundary_18_degrees():
    result = trimshamsa(18.0)

    assert result.division == 4


def test_boundary_25_degrees():
    result = trimshamsa(25.0)

    assert result.division == 5


# -------------------------
# Wraparound
# -------------------------


def test_zero_longitude():
    result = trimshamsa(0.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_wraparound():
    result = trimshamsa(361.0)

    assert result.sign == ZodiacSign.ARIES
    assert result.division == 1


def test_negative_longitude():
    result = trimshamsa(-1.0)

    assert result.division == 5


def test_last_possible_degree():
    result = trimshamsa(359.999)

    assert result.division == 5
