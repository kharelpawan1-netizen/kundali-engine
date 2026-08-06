"""
tests/test_chandra_mangala.py

Tests for structural Chandra-Mangala Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult
from yogas.chandra_mangala import (
    CHANDRA_MANGALA_YOGA_NAME,
    MARS,
    MOON,
    ChandraMangalaYogaRule,
    chandra_mangala_evidence,
    detect_chandra_mangala,
    get_planet_house,
    moon_mars_conjunct,
)


# ============================================================
# TEST HELPERS
# ============================================================

def make_context(
    moon_house=None,
    mars_house=None,
):
    """
    Build a minimal test context.

    The structure follows the project's current context
    convention:

        context.planets[planet_name].house
    """

    planets = {}

    if moon_house is not None:
        planets[MOON] = SimpleNamespace(
            name=MOON,
            house=moon_house,
        )

    if mars_house is not None:
        planets[MARS] = SimpleNamespace(
            name=MARS,
            house=mars_house,
        )

    return SimpleNamespace(
        planets=planets,
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_chandra_mangala_name():
    assert CHANDRA_MANGALA_YOGA_NAME == (
        "Chandra-Mangala Yoga"
    )


def test_moon_constant():
    assert MOON == "Moon"


def test_mars_constant():
    assert MARS == "Mars"


# ============================================================
# PLANET HOUSE HELPER
# ============================================================

def test_get_planet_house_returns_valid_house():
    context = make_context(
        moon_house=5,
        mars_house=5,
    )

    assert get_planet_house(
        context,
        MOON,
    ) == 5

    assert get_planet_house(
        context,
        MARS,
    ) == 5


def test_get_planet_house_missing_planet():
    context = make_context(
        moon_house=5,
    )

    assert get_planet_house(
        context,
        MARS,
    ) is None


@pytest.mark.parametrize(
    "house",
    [
        0,
        13,
        -1,
    ],
)
def test_get_planet_house_rejects_invalid_house(
    house,
):
    context = make_context(
        moon_house=house,
        mars_house=5,
    )

    assert get_planet_house(
        context,
        MOON,
    ) is None


@pytest.mark.parametrize(
    "house",
    [
        "5",
        5.0,
    ],
)
def test_get_planet_house_accepts_numeric_house_values(
    house,
):
    context = make_context(
        moon_house=house,
        mars_house=5,
    )

    assert get_planet_house(
        context,
        MOON,
    ) == 5


# ============================================================
# CONJUNCTION
# ============================================================

def test_moon_mars_conjunct():
    context = make_context(
        moon_house=5,
        mars_house=5,
    )

    assert moon_mars_conjunct(
        context
    ) is True


def test_moon_mars_not_conjunct():
    context = make_context(
        moon_house=5,
        mars_house=6,
    )

    assert moon_mars_conjunct(
        context
    ) is False


def test_conjunction_in_first_house():
    context = make_context(
        moon_house=1,
        mars_house=1,
    )

    assert moon_mars_conjunct(
        context
    ) is True


def test_conjunction_in_tenth_house():
    context = make_context(
        moon_house=10,
        mars_house=10,
    )

    assert moon_mars_conjunct(
        context
    ) is True


def test_conjunction_in_twelfth_house():
    context = make_context(
        moon_house=12,
        mars_house=12,
    )

    assert moon_mars_conjunct(
        context
    ) is True


def test_missing_moon_prevents_conjunction():
    context = make_context(
        mars_house=5,
    )

    assert moon_mars_conjunct(
        context
    ) is False


def test_missing_mars_prevents_conjunction():
    context = make_context(
        moon_house=5,
    )

    assert moon_mars_conjunct(
        context
    ) is False


def test_missing_both_planets_prevents_conjunction():
    context = make_context()

    assert moon_mars_conjunct(
        context
    ) is False


# ============================================================
# EVIDENCE
# ============================================================

def test_chandra_mangala_evidence_when_present():
    context = make_context(
        moon_house=5,
        mars_house=5,
    )

    evidence = chandra_mangala_evidence(
        context
    )

    assert len(evidence) == 1

    finding = evidence[0]

    assert finding["planet_a"] == MOON
    assert finding["planet_b"] == MARS
    assert finding["moon_house"] == 5
    assert finding["mars_house"] == 5
    assert finding["association"] == "conjunction"


def test_chandra_mangala_evidence_when_absent():
    context = make_context(
        moon_house=5,
        mars_house=6,
    )

    evidence = chandra_mangala_evidence(
        context
    )

    assert evidence == []


def test_chandra_mangala_evidence_when_moon_missing():
    context = make_context(
        mars_house=5,
    )

    evidence = chandra_mangala_evidence(
        context
    )

    assert evidence == []


def test_chandra_mangala_evidence_when_mars_missing():
    context = make_context(
        moon_house=5,
    )

    evidence = chandra_mangala_evidence(
        context
    )

    assert evidence == []


# ============================================================
# DETECTION
# ============================================================

def test_detect_chandra_mangala_when_conjunct():
    context = make_context(
        moon_house=5,
        mars_house=5,
    )

    result = detect_chandra_mangala(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == CHANDRA_MANGALA_YOGA_NAME
    assert result.category == "Chandra-Mangala Yoga"


def test_detect_chandra_mangala_when_not_conjunct():
    context = make_context(
        moon_house=5,
        mars_house=6,
    )

    result = detect_chandra_mangala(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False
    assert result.name == CHANDRA_MANGALA_YOGA_NAME
    assert result.category == "Chandra-Mangala Yoga"


def test_detect_chandra_mangala_missing_moon():
    context = make_context(
        mars_house=5,
    )

    result = detect_chandra_mangala(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


def test_detect_chandra_mangala_missing_mars():
    context = make_context(
        moon_house=5,
    )

    result = detect_chandra_mangala(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


# ============================================================
# DETECTED RESULT
# ============================================================

def test_detected_result_contains_evidence():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.detected is True
    assert result.evidence
    assert result.conditions_met
    assert result.involved_planets
    assert result.involved_houses


def test_detected_result_involved_planets():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert set(
        result.involved_planets
    ) == {
        MOON,
        MARS,
    }


def test_detected_result_involved_houses():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.involved_houses == [7]


def test_detected_result_evidence_text():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.evidence == [
        "Moon and Mars are conjunct in house 7."
    ]


def test_detected_result_conditions_met():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.conditions_met == [
        (
            "Moon and Mars occupy the same house, "
            "forming the structural conjunction."
        )
    ]


def test_detected_result_metadata():
    context = make_context(
        moon_house=7,
        mars_house=7,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.metadata[
        "formation"
    ] == "moon_mars_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "moon_house"
    ] == 7

    assert result.metadata[
        "mars_house"
    ] == 7


# ============================================================
# NON-DETECTED RESULT
# ============================================================

def test_undetected_result_contains_failed_condition():
    context = make_context(
        moon_house=7,
        mars_house=8,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.detected is False
    assert result.conditions_failed


def test_undetected_result_metadata():
    context = make_context(
        moon_house=7,
        mars_house=8,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.metadata[
        "formation"
    ] == "moon_mars_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "moon_house"
    ] == 7

    assert result.metadata[
        "mars_house"
    ] == 8


# ============================================================
# STRUCTURAL SCOPE
# ============================================================

def test_same_house_is_sufficient_structurally():
    """
    Structural detection depends only on the same-house
    conjunction.
    """

    context = make_context(
        moon_house=4,
        mars_house=4,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.detected is True


def test_different_houses_do_not_form_structural_yoga():
    context = make_context(
        moon_house=4,
        mars_house=10,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.detected is False


# ============================================================
# RULE ADAPTER
# ============================================================

def test_chandra_mangala_rule():
    context = make_context(
        moon_house=9,
        mars_house=9,
    )

    rule = ChandraMangalaYogaRule()

    result = rule.evaluate(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == CHANDRA_MANGALA_YOGA_NAME
    assert result.category == "Chandra-Mangala Yoga"


def test_chandra_mangala_rule_when_not_present():
    context = make_context(
        moon_house=9,
        mars_house=10,
    )

    rule = ChandraMangalaYogaRule()

    result = rule.evaluate(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


# ============================================================
# HOUSE-BY-HOUSE STRUCTURAL COVERAGE
# ============================================================

@pytest.mark.parametrize(
    "house",
    range(1, 13),
)
def test_same_house_conjunction_detected_in_every_house(
    house,
):
    context = make_context(
        moon_house=house,
        mars_house=house,
    )

    result = detect_chandra_mangala(
        context
    )

    assert result.detected is True
    assert result.involved_houses == [house]