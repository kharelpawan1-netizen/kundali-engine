"""
tests/test_signs.py

Unit tests for astronomy.signs
"""

import pytest

from astronomy.signs import (
    element,
    longitude_to_sign,
    mod360,
    sign_degree,
    sign_end,
    sign_enum,
    sign_name,
    sign_number,
    sign_start,
    validate_longitude,
)
from models.element import Element
from models.zodiac import ZodiacSign

# -------------------------------------------------------
# mod360
# -------------------------------------------------------


def test_mod360_zero():
    assert mod360(0) == 0


def test_mod360_positive():
    assert mod360(361) == 1


def test_mod360_negative():
    assert mod360(-1) == 359


def test_mod360_large():
    assert mod360(721) == 1


# -------------------------------------------------------
# validate_longitude
# -------------------------------------------------------


def test_validate():
    assert validate_longitude(400) == 40


def test_validate_negative():
    assert validate_longitude(-20) == 340


def test_validate_invalid():
    with pytest.raises(TypeError):
        validate_longitude("abc")


# -------------------------------------------------------
# sign_number
# -------------------------------------------------------


def test_sign_number():
    assert sign_number(0) == 1
    assert sign_number(29.999) == 1
    assert sign_number(30) == 2
    assert sign_number(359.999) == 12


# -------------------------------------------------------
# sign_enum
# -------------------------------------------------------


def test_sign_enum():
    assert sign_enum(0) == ZodiacSign.ARIES
    assert sign_enum(30) == ZodiacSign.TAURUS
    assert sign_enum(150) == ZodiacSign.VIRGO


# -------------------------------------------------------
# sign_name
# -------------------------------------------------------


def test_sign_name():
    assert sign_name(0) == "Aries"
    assert sign_name(330) == "Pisces"


# -------------------------------------------------------
# sign_degree
# -------------------------------------------------------


def test_sign_degree():
    assert sign_degree(35) == 5
    assert sign_degree(359.5) == pytest.approx(29.5)


# -------------------------------------------------------
# boundaries
# -------------------------------------------------------


def test_boundaries():
    assert sign_start(35) == 30
    assert sign_end(35) == 60


# -------------------------------------------------------
# elements
# -------------------------------------------------------


def test_element():
    assert element(0) == Element.FIRE
    assert element(30) == Element.EARTH
    assert element(60) == Element.AIR
    assert element(90) == Element.WATER


# -------------------------------------------------------
# SignInfo
# -------------------------------------------------------


def test_sign_info():
    info = longitude_to_sign(145.62)

    assert info.number == 5
    assert info.sign == ZodiacSign.LEO
    assert info.element == Element.FIRE
    assert info.degree == pytest.approx(25.62)
