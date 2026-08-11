"""
tests/test_astrology_signs.py

Unit tests for the classical Rashi knowledge layer.

Tests:
    - Rashi lords
    - Rashi elements
    - Movable / Fixed / Dual classification
    - Masculine / Feminine classification
    - Odd / Even classification
    - Rashi modality
    - Element convenience helpers

Python Version:
    3.9+
"""

from astrology.signs import (
    DUAL_SIGNS,
    FEMININE_SIGNS,
    FIXED_SIGNS,
    MASCULINE_SIGNS,
    MOVABLE_SIGNS,
    RASHI_ELEMENTS,
    RASHI_LORDS,
    is_air_sign,
    is_dual,
    is_earth_sign,
    is_even,
    is_fire_sign,
    is_fixed,
    is_feminine,
    is_masculine,
    is_movable,
    is_odd,
    is_water_sign,
    rashi_element,
    rashi_lord,
    rashi_modality,
)
from models.element import Element
from models.zodiac import ZodiacSign


# ---------------------------------------------------------------------
# Rashi Lord Tests
# ---------------------------------------------------------------------


def test_all_rashis_have_lords():
    """Every Rashi must have a defined classical lord."""

    assert len(RASHI_LORDS) == 12

    for sign in ZodiacSign:
        assert sign in RASHI_LORDS
        assert isinstance(RASHI_LORDS[sign], str)
        assert RASHI_LORDS[sign]


def test_rashi_lords():
    """Verify classical Rashi lordship."""

    expected = {
        ZodiacSign.ARIES: "Mars",
        ZodiacSign.TAURUS: "Venus",
        ZodiacSign.GEMINI: "Mercury",
        ZodiacSign.CANCER: "Moon",
        ZodiacSign.LEO: "Sun",
        ZodiacSign.VIRGO: "Mercury",
        ZodiacSign.LIBRA: "Venus",
        ZodiacSign.SCORPIO: "Mars",
        ZodiacSign.SAGITTARIUS: "Jupiter",
        ZodiacSign.CAPRICORN: "Saturn",
        ZodiacSign.AQUARIUS: "Saturn",
        ZodiacSign.PISCES: "Jupiter",
    }

    assert RASHI_LORDS == expected

    for sign, lord in expected.items():
        assert rashi_lord(sign) == lord


# ---------------------------------------------------------------------
# Element Tests
# ---------------------------------------------------------------------


def test_all_rashis_have_elements():
    """Every Rashi must have an element."""

    assert len(RASHI_ELEMENTS) == 12

    for sign in ZodiacSign:
        assert sign in RASHI_ELEMENTS
        assert isinstance(RASHI_ELEMENTS[sign], Element)


def test_rashi_elements():
    """Verify the classical four-element Rashi sequence."""

    expected = {
        ZodiacSign.ARIES: Element.FIRE,
        ZodiacSign.TAURUS: Element.EARTH,
        ZodiacSign.GEMINI: Element.AIR,
        ZodiacSign.CANCER: Element.WATER,
        ZodiacSign.LEO: Element.FIRE,
        ZodiacSign.VIRGO: Element.EARTH,
        ZodiacSign.LIBRA: Element.AIR,
        ZodiacSign.SCORPIO: Element.WATER,
        ZodiacSign.SAGITTARIUS: Element.FIRE,
        ZodiacSign.CAPRICORN: Element.EARTH,
        ZodiacSign.AQUARIUS: Element.AIR,
        ZodiacSign.PISCES: Element.WATER,
    }

    assert RASHI_ELEMENTS == expected

    for sign, expected_element in expected.items():
        assert rashi_element(sign) is expected_element


# ---------------------------------------------------------------------
# Movable / Fixed / Dual Tests
# ---------------------------------------------------------------------


def test_movable_signs():
    """Verify Chara (Movable) Rashis."""

    expected = {
        ZodiacSign.ARIES,
        ZodiacSign.CANCER,
        ZodiacSign.LIBRA,
        ZodiacSign.CAPRICORN,
    }

    assert MOVABLE_SIGNS == expected

    for sign in ZodiacSign:
        assert is_movable(sign) is (sign in expected)


def test_fixed_signs():
    """Verify Sthira (Fixed) Rashis."""

    expected = {
        ZodiacSign.TAURUS,
        ZodiacSign.LEO,
        ZodiacSign.SCORPIO,
        ZodiacSign.AQUARIUS,
    }

    assert FIXED_SIGNS == expected

    for sign in ZodiacSign:
        assert is_fixed(sign) is (sign in expected)


def test_dual_signs():
    """Verify Dvisvabhava (Dual) Rashis."""

    expected = {
        ZodiacSign.GEMINI,
        ZodiacSign.VIRGO,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.PISCES,
    }

    assert DUAL_SIGNS == expected

    for sign in ZodiacSign:
        assert is_dual(sign) is (sign in expected)


def test_each_sign_has_exactly_one_modality():
    """Every Rashi must belong to exactly one modality."""

    for sign in ZodiacSign:
        classifications = [
            is_movable(sign),
            is_fixed(sign),
            is_dual(sign),
        ]

        assert sum(classifications) == 1


def test_rashi_modality():
    """Verify modality names."""

    assert rashi_modality(ZodiacSign.ARIES) == "Movable"
    assert rashi_modality(ZodiacSign.CANCER) == "Movable"
    assert rashi_modality(ZodiacSign.LIBRA) == "Movable"
    assert rashi_modality(ZodiacSign.CAPRICORN) == "Movable"

    assert rashi_modality(ZodiacSign.TAURUS) == "Fixed"
    assert rashi_modality(ZodiacSign.LEO) == "Fixed"
    assert rashi_modality(ZodiacSign.SCORPIO) == "Fixed"
    assert rashi_modality(ZodiacSign.AQUARIUS) == "Fixed"

    assert rashi_modality(ZodiacSign.GEMINI) == "Dual"
    assert rashi_modality(ZodiacSign.VIRGO) == "Dual"
    assert rashi_modality(ZodiacSign.SAGITTARIUS) == "Dual"
    assert rashi_modality(ZodiacSign.PISCES) == "Dual"


# ---------------------------------------------------------------------
# Masculine / Feminine Tests
# ---------------------------------------------------------------------


def test_masculine_signs():
    """Verify traditionally masculine Rashis."""

    expected = {
        ZodiacSign.ARIES,
        ZodiacSign.GEMINI,
        ZodiacSign.LEO,
        ZodiacSign.LIBRA,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.AQUARIUS,
    }

    assert MASCULINE_SIGNS == expected

    for sign in ZodiacSign:
        assert is_masculine(sign) is (sign in expected)


def test_feminine_signs():
    """Verify traditionally feminine Rashis."""

    expected = {
        ZodiacSign.TAURUS,
        ZodiacSign.CANCER,
        ZodiacSign.VIRGO,
        ZodiacSign.SCORPIO,
        ZodiacSign.CAPRICORN,
        ZodiacSign.PISCES,
    }

    assert FEMININE_SIGNS == expected

    for sign in ZodiacSign:
        assert is_feminine(sign) is (sign in expected)


def test_each_sign_has_exactly_one_gender():
    """Every Rashi must be classified as masculine or feminine."""

    for sign in ZodiacSign:
        classifications = [
            is_masculine(sign),
            is_feminine(sign),
        ]

        assert sum(classifications) == 1


# ---------------------------------------------------------------------
# Odd / Even Tests
# ---------------------------------------------------------------------


def test_odd_signs_are_masculine():
    """Odd-numbered Rashis must be masculine."""

    for sign in ZodiacSign:
        if sign.number % 2 == 1:
            assert is_odd(sign)
            assert is_masculine(sign)


def test_even_signs_are_feminine():
    """Even-numbered Rashis must be feminine."""

    for sign in ZodiacSign:
        if sign.number % 2 == 0:
            assert is_even(sign)
            assert is_feminine(sign)


def test_odd_even_are_mutually_exclusive():
    """A Rashi cannot be both odd and even."""

    for sign in ZodiacSign:
        assert is_odd(sign) is not is_even(sign)


# ---------------------------------------------------------------------
# Element Convenience Helper Tests
# ---------------------------------------------------------------------


def test_fire_sign_helpers():
    """Verify Fire-sign helper."""

    fire_signs = {
        ZodiacSign.ARIES,
        ZodiacSign.LEO,
        ZodiacSign.SAGITTARIUS,
    }

    for sign in ZodiacSign:
        assert is_fire_sign(sign) is (sign in fire_signs)


def test_earth_sign_helpers():
    """Verify Earth-sign helper."""

    earth_signs = {
        ZodiacSign.TAURUS,
        ZodiacSign.VIRGO,
        ZodiacSign.CAPRICORN,
    }

    for sign in ZodiacSign:
        assert is_earth_sign(sign) is (sign in earth_signs)


def test_air_sign_helpers():
    """Verify Air-sign helper."""

    air_signs = {
        ZodiacSign.GEMINI,
        ZodiacSign.LIBRA,
        ZodiacSign.AQUARIUS,
    }

    for sign in ZodiacSign:
        assert is_air_sign(sign) is (sign in air_signs)


def test_water_sign_helpers():
    """Verify Water-sign helper."""

    water_signs = {
        ZodiacSign.CANCER,
        ZodiacSign.SCORPIO,
        ZodiacSign.PISCES,
    }

    for sign in ZodiacSign:
        assert is_water_sign(sign) is (sign in water_signs)


def test_element_helpers_are_mutually_exclusive():
    """Every Rashi must belong to exactly one element."""

    for sign in ZodiacSign:
        classifications = [
            is_fire_sign(sign),
            is_earth_sign(sign),
            is_air_sign(sign),
            is_water_sign(sign),
        ]

        assert sum(classifications) == 1


# ---------------------------------------------------------------------
# Structural Completeness
# ---------------------------------------------------------------------


def test_all_twelve_rashis_are_represented():
    """The knowledge layer must cover all twelve Rashis."""

    assert len(list(ZodiacSign)) == 12
    assert len(RASHI_LORDS) == 12
    assert len(RASHI_ELEMENTS) == 12


def test_modality_groups_cover_all_rashis():
    """Movable, Fixed, and Dual groups must cover all Rashis."""

    combined = (
        MOVABLE_SIGNS
        | FIXED_SIGNS
        | DUAL_SIGNS
    )

    assert len(combined) == 12
    assert combined == set(ZodiacSign)


def test_gender_groups_cover_all_rashis():
    """Masculine and feminine groups must cover all Rashis."""

    combined = (
        MASCULINE_SIGNS
        | FEMININE_SIGNS
    )

    assert len(combined) == 12
    assert combined == set(ZodiacSign)