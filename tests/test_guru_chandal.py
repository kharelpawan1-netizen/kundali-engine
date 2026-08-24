"""
tests/test_guru_chandal.py

Tests for structural Guru Chandal Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult
from yogas.guru_chandal import (
    GURU_CHANDAL_YOGA_NAME,
    JUPITER,
    RAHU,
    GuruChandalYogaRule,
    detect_guru_chandal,
    get_planet_house,
    guru_chandal_evidence,
    jupiter_rahu_conjunct,
)


# ============================================================
# TEST HELPERS
# ============================================================

def make_context(
    jupiter_house=None,
    rahu_house=None,
):
    """
    Build a minimal test context.

    The structure mirrors the project's current context
    convention:

        context.planets[planet_name].house
    """

    planets = {}

    if jupiter_house is not None:
        planets[JUPITER] = SimpleNamespace(
            name=JUPITER,
            house=jupiter_house,
        )

    if rahu_house is not None:
        planets[RAHU] = SimpleNamespace(
            name=RAHU,
            house=rahu_house,
        )

    return SimpleNamespace(
        planets=planets,
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_guru_chandal_name():
    assert GURU_CHANDAL_YOGA_NAME == (
        "Guru Chandal Yoga"
    )


def test_jupiter_constant():
    assert JUPITER == "Jupiter"


def test_rahu_constant():
    assert RAHU == "Rahu"


# ============================================================
# PLANET HOUSE HELPER
# ============================================================

def test_get_planet_house_returns_valid_house():
    context = make_context(
        jupiter_house=5,
        rahu_house=5,
    )

    assert get_planet_house(
        context,
        JUPITER,
    ) == 5

    assert get_planet_house(
        context,
        RAHU,
    ) == 5


def test_get_planet_house_missing_planet():
    context = make_context(
        jupiter_house=5,
    )

    assert get_planet_house(
        context,
        RAHU,
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
        jupiter_house=house,
        rahu_house=5,
    )

    assert get_planet_house(
        context,
        JUPITER,
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
        jupiter_house=house,
        rahu_house=5,
    )

    assert get_planet_house(
        context,
        JUPITER,
    ) == 5


# ============================================================
# CONJUNCTION
# ============================================================

def test_jupiter_rahu_conjunct():
    context = make_context(
        jupiter_house=5,
        rahu_house=5,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is True


def test_jupiter_rahu_not_conjunct():
    context = make_context(
        jupiter_house=5,
        rahu_house=6,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is False


def test_conjunction_in_first_house():
    context = make_context(
        jupiter_house=1,
        rahu_house=1,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is True


def test_conjunction_in_tenth_house():
    context = make_context(
        jupiter_house=10,
        rahu_house=10,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is True


def test_conjunction_in_twelfth_house():
    context = make_context(
        jupiter_house=12,
        rahu_house=12,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is True


def test_missing_jupiter_prevents_conjunction():
    context = make_context(
        rahu_house=5,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is False


def test_missing_rahu_prevents_conjunction():
    context = make_context(
        jupiter_house=5,
    )

    assert jupiter_rahu_conjunct(
        context
    ) is False


def test_missing_both_planets_prevents_conjunction():
    context = make_context()

    assert jupiter_rahu_conjunct(
        context
    ) is False


# ============================================================
# EVIDENCE
# ============================================================

def test_guru_chandal_evidence_when_present():
    context = make_context(
        jupiter_house=5,
        rahu_house=5,
    )

    evidence = guru_chandal_evidence(
        context
    )

    assert len(evidence) == 1

    finding = evidence[0]

    assert finding["planet_a"] == JUPITER
    assert finding["planet_b"] == RAHU
    assert finding["jupiter_house"] == 5
    assert finding["rahu_house"] == 5
    assert finding["association"] == "conjunction"


def test_guru_chandal_evidence_when_absent():
    context = make_context(
        jupiter_house=5,
        rahu_house=6,
    )

    evidence = guru_chandal_evidence(
        context
    )

    assert evidence == []


def test_guru_chandal_evidence_when_jupiter_missing():
    context = make_context(
        rahu_house=5,
    )

    evidence = guru_chandal_evidence(
        context
    )

    assert evidence == []


def test_guru_chandal_evidence_when_rahu_missing():
    context = make_context(
        jupiter_house=5,
    )

    evidence = guru_chandal_evidence(
        context
    )

    assert evidence == []


# ============================================================
# DETECTION
# ============================================================

def test_detect_guru_chandal_when_conjunct():
    context = make_context(
        jupiter_house=5,
        rahu_house=5,
    )

    result = detect_guru_chandal(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == GURU_CHANDAL_YOGA_NAME
    assert result.category == "Guru Chandal Yoga"


def test_detect_guru_chandal_when_not_conjunct():
    context = make_context(
        jupiter_house=5,
        rahu_house=6,
    )

    result = detect_guru_chandal(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False
    assert result.name == GURU_CHANDAL_YOGA_NAME
    assert result.category == "Guru Chandal Yoga"


def test_detect_guru_chandal_missing_jupiter():
    context = make_context(
        rahu_house=5,
    )

    result = detect_guru_chandal(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


def test_detect_guru_chandal_missing_rahu():
    context = make_context(
        jupiter_house=5,
    )

    result = detect_guru_chandal(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


# ============================================================
# DETECTED RESULT CONTENT
# ============================================================

def test_detected_result_contains_evidence():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.detected is True
    assert result.evidence
    assert result.conditions_met
    assert result.involved_planets
    assert result.involved_houses


def test_detected_result_involved_planets():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert set(
        result.involved_planets
    ) == {
        JUPITER,
        RAHU,
    }


def test_detected_result_involved_houses():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.involved_houses == [7]


def test_detected_result_evidence_text():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.evidence == [
        "Jupiter and Rahu are conjunct in house 7."
    ]


def test_detected_result_conditions_met():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.conditions_met == [
        (
            "Jupiter and Rahu occupy the same house, "
            "forming the structural conjunction."
        )
    ]


def test_detected_result_metadata():
    context = make_context(
        jupiter_house=7,
        rahu_house=7,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.metadata[
        "formation"
    ] == "jupiter_rahu_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "jupiter_house"
    ] == 7

    assert result.metadata[
        "rahu_house"
    ] == 7


# ============================================================
# NON-DETECTED RESULT CONTENT
# ============================================================

def test_undetected_result_contains_failed_condition():
    context = make_context(
        jupiter_house=7,
        rahu_house=8,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.detected is False
    assert result.conditions_failed


def test_undetected_result_metadata():
    context = make_context(
        jupiter_house=7,
        rahu_house=8,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.metadata[
        "formation"
    ] == "jupiter_rahu_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "jupiter_house"
    ] == 7

    assert result.metadata[
        "rahu_house"
    ] == 8


# ============================================================
# STRUCTURAL SCOPE
# ============================================================

def test_same_house_is_sufficient_structurally():
    """
    Structural detection depends only on the same-house
    conjunction.

    No dignity or strength data is required.
    """

    context = make_context(
        jupiter_house=4,
        rahu_house=4,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.detected is True


def test_different_houses_do_not_form_structural_yoga():
    context = make_context(
        jupiter_house=4,
        rahu_house=10,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.detected is False


# ============================================================
# RULE ADAPTER
# ============================================================

def test_guru_chandal_rule():
    context = make_context(
        jupiter_house=9,
        rahu_house=9,
    )

    rule = GuruChandalYogaRule()

    result = rule.evaluate(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == GURU_CHANDAL_YOGA_NAME
    assert result.category == "Guru Chandal Yoga"


def test_guru_chandal_rule_when_not_present():
    context = make_context(
        jupiter_house=9,
        rahu_house=10,
    )

    rule = GuruChandalYogaRule()

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
        jupiter_house=house,
        rahu_house=house,
    )

    result = detect_guru_chandal(
        context
    )

    assert result.detected is True
    assert result.involved_houses == [house]
