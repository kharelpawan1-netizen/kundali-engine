"""
Tests for Hora (D2).

According to Brihat Parashara Hora Shastra.
"""

from astronomy.hora import hora
from models.zodiac import ZodiacSign


def test_aries_first_hora():
    """
    Aries 5° -> Leo.
    """

    result = hora(5.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_aries_second_hora():
    """
    Aries 20° -> Cancer.
    """

    result = hora(20.0)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 2


def test_taurus_first_hora():
    """
    Taurus 5° -> Cancer.
    """

    result = hora(35.0)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 1


def test_taurus_second_hora():
    """
    Taurus 20° -> Leo.
    """

    result = hora(50.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2


def test_boundary_15_degrees_odd():
    """
    Aries exactly 15° starts second Hora.
    """

    result = hora(15.0)

    assert result.sign == ZodiacSign.CANCER
    assert result.division == 2


def test_boundary_15_degrees_even():
    """
    Taurus exactly 15° starts second Hora.
    """

    result = hora(45.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2


def test_last_degree():
    """
    Pisces 29°59' remains second Hora.
    """

    result = hora(359.999)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2


def test_zero_degree():
    """
    0° Aries.
    """

    result = hora(0.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_wraparound():
    """
    Longitude above 360° wraps correctly.
    """

    result = hora(365.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


def test_negative_longitude():
    """
    Negative longitude wraps correctly.
    """

    result = hora(-5.0)

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2
