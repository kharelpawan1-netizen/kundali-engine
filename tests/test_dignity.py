"""
Tests for planetary dignity calculations.
"""

from astronomy.dignity import (
    is_debilitated,
    is_exalted,
    is_moolatrikona,
    is_own_sign,
)
from models.graha import Graha
from models.zodiac import ZodiacSign


def test_sun_exaltation():
    assert is_exalted(
        Graha.SUN,
        ZodiacSign.ARIES,
    )


def test_sun_not_exalted():
    assert not is_exalted(
        Graha.SUN,
        ZodiacSign.LEO,
    )


def test_saturn_debilitation():
    assert is_debilitated(
        Graha.SATURN,
        ZodiacSign.ARIES,
    )


def test_saturn_not_debilitated():
    assert not is_debilitated(
        Graha.SATURN,
        ZodiacSign.AQUARIUS,
    )


def test_mars_own_sign():
    assert is_own_sign(
        Graha.MARS,
        ZodiacSign.ARIES,
    )


def test_mercury_own_sign():
    assert is_own_sign(
        Graha.MERCURY,
        ZodiacSign.VIRGO,
    )


def test_jupiter_not_own_sign():
    assert not is_own_sign(
        Graha.JUPITER,
        ZodiacSign.LEO,
    )


def test_sun_moolatrikona():
    assert is_moolatrikona(
        Graha.SUN,
        ZodiacSign.LEO,
    )


def test_jupiter_moolatrikona():
    assert is_moolatrikona(
        Graha.JUPITER,
        ZodiacSign.SAGITTARIUS,
    )


def test_saturn_not_moolatrikona():
    assert not is_moolatrikona(
        Graha.SATURN,
        ZodiacSign.CAPRICORN,
    )
