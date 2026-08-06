"""
tests/test_budha_aditya.py

Tests for structural Budha-Aditya Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult
from yogas.budha_aditya import (
    BUDHA_ADITYA_YOGA_NAME,
    MERCURY,
    SUN,
    BudhaAdityaYogaRule,
    budha_aditya_evidence,
    detect_budha_aditya,
    get_planet_house,
    sun_mercury_conjunct,
)


# ============================================================
# TEST HELPERS
# ============================================================

def make_context(
    sun_house=None,
    mercury_house=None,
):
    """
    Build a minimal test context.

    The structure mirrors the project's current context
    convention:

        context.planets[planet_name].house
    """

    planets = {}

    if sun_house is not None:
        planets[SUN] = SimpleNamespace(
            name=SUN,
            house=sun_house,
        )

    if mercury_house is not None:
        planets[MERCURY] = SimpleNamespace(
            name=MERCURY,
            house=mercury_house,
        )

    return SimpleNamespace(
        planets=planets,
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_budha_aditya_name():
    assert BUDHA_ADITYA_YOGA_NAME == (
        "Budha-Aditya Yoga"
    )


def test_sun_constant():
    assert SUN == "Sun"


def test_mercury_constant():
    assert MERCURY == "Mercury"


# ============================================================
# PLANET HOUSE HELPER
# ============================================================

def test_get_planet_house_returns_valid_house():
    context = make_context(
        sun_house=5,
        mercury_house=5,
    )

    assert get_planet_house(
        context,
        SUN,
    ) == 5

    assert get_planet_house(
        context,
        MERCURY,
    ) == 5


def test_get_planet_house_missing_planet():
    context = make_context(
        sun_house=5,
    )

    assert get_planet_house(
        context,
        MERCURY,
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
        sun_house=house,
        mercury_house=5,
    )

    assert get_planet_house(
        context,
        SUN,
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
        sun_house=house,
        mercury_house=5,
    )

    assert get_planet_house(
        context,
        SUN,
    ) == 5


# ============================================================
# CONJUNCTION
# ============================================================

def test_sun_mercury_conjunct():
    context = make_context(
        sun_house=5,
        mercury_house=5,
    )

    assert sun_mercury_conjunct(
        context
    ) is True


def test_sun_mercury_not_conjunct():
    context = make_context(
        sun_house=5,
        mercury_house=6,
    )

    assert sun_mercury_conjunct(
        context
    ) is False


def test_conjunction_in_first_house():
    context = make_context(
        sun_house=1,
        mercury_house=1,
    )

    assert sun_mercury_conjunct(
        context
    ) is True


def test_conjunction_in_tenth_house():
    context = make_context(
        sun_house=10,
        mercury_house=10,
    )

    assert sun_mercury_conjunct(
        context
    ) is True


def test_conjunction_in_twelfth_house():
    context = make_context(
        sun_house=12,
        mercury_house=12,
    )

    assert sun_mercury_conjunct(
        context
    ) is True


def test_missing_sun_prevents_conjunction():
    context = make_context(
        mercury_house=5,
    )

    assert sun_mercury_conjunct(
        context
    ) is False


def test_missing_mercury_prevents_conjunction():
    context = make_context(
        sun_house=5,
    )

    assert sun_mercury_conjunct(
        context
    ) is False


def test_missing_both_planets_prevents_conjunction():
    context = make_context()

    assert sun_mercury_conjunct(
        context
    ) is False


# ============================================================
# EVIDENCE
# ============================================================

def test_budha_aditya_evidence_when_present():
    context = make_context(
        sun_house=5,
        mercury_house=5,
    )

    evidence = budha_aditya_evidence(
        context
    )

    assert len(evidence) == 1

    finding = evidence[0]

    assert finding["planet_a"] == SUN
    assert finding["planet_b"] == MERCURY
    assert finding["sun_house"] == 5
    assert finding["mercury_house"] == 5
    assert finding["association"] == "conjunction"


def test_budha_aditya_evidence_when_absent():
    context = make_context(
        sun_house=5,
        mercury_house=6,
    )

    evidence = budha_aditya_evidence(
        context
    )

    assert evidence == []


def test_budha_aditya_evidence_when_sun_missing():
    context = make_context(
        mercury_house=5,
    )

    evidence = budha_aditya_evidence(
        context
    )

    assert evidence == []


def test_budha_aditya_evidence_when_mercury_missing():
    context = make_context(
        sun_house=5,
    )

    evidence = budha_aditya_evidence(
        context
    )

    assert evidence == []


# ============================================================
# DETECTION
# ============================================================

def test_detect_budha_aditya_when_conjunct():
    context = make_context(
        sun_house=5,
        mercury_house=5,
    )

    result = detect_budha_aditya(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == BUDHA_ADITYA_YOGA_NAME
    assert result.category == "Budha-Aditya Yoga"


def test_detect_budha_aditya_when_not_conjunct():
    context = make_context(
        sun_house=5,
        mercury_house=6,
    )

    result = detect_budha_aditya(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False
    assert result.name == BUDHA_ADITYA_YOGA_NAME
    assert result.category == "Budha-Aditya Yoga"


def test_detect_budha_aditya_missing_sun():
    context = make_context(
        mercury_house=5,
    )

    result = detect_budha_aditya(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is False


def test_detect_budha_aditya_missing_mercury():
    context = make_context(
        sun_house=5,
    )

    result = detect_budha_aditya(
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
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.detected is True
    assert result.evidence
    assert result.conditions_met
    assert result.involved_planets
    assert result.involved_houses


def test_detected_result_involved_planets():
    context = make_context(
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert set(
        result.involved_planets
    ) == {
        SUN,
        MERCURY,
    }


def test_detected_result_involved_houses():
    context = make_context(
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.involved_houses == [7]


def test_detected_result_evidence_text():
    context = make_context(
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.evidence == [
        "Sun and Mercury are conjunct in house 7."
    ]


def test_detected_result_conditions_met():
    context = make_context(
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.conditions_met == [
        (
            "Sun and Mercury occupy the same house, "
            "forming the structural conjunction."
        )
    ]


def test_detected_result_metadata():
    context = make_context(
        sun_house=7,
        mercury_house=7,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.metadata[
        "formation"
    ] == "sun_mercury_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "sun_house"
    ] == 7

    assert result.metadata[
        "mercury_house"
    ] == 7


# ============================================================
# NON-DETECTED RESULT CONTENT
# ============================================================

def test_undetected_result_contains_failed_condition():
    context = make_context(
        sun_house=7,
        mercury_house=8,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.detected is False
    assert result.conditions_failed


def test_undetected_result_metadata():
    context = make_context(
        sun_house=7,
        mercury_house=8,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.metadata[
        "formation"
    ] == "sun_mercury_conjunction"

    assert result.metadata[
        "association_type"
    ] == "conjunction"

    assert result.metadata[
        "sun_house"
    ] == 7

    assert result.metadata[
        "mercury_house"
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
        sun_house=4,
        mercury_house=4,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.detected is True


def test_different_houses_do_not_form_structural_yoga():
    context = make_context(
        sun_house=4,
        mercury_house=10,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.detected is False


# ============================================================
# RULE ADAPTER
# ============================================================

def test_budha_aditya_rule():
    context = make_context(
        sun_house=9,
        mercury_house=9,
    )

    rule = BudhaAdityaYogaRule()

    result = rule.evaluate(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == BUDHA_ADITYA_YOGA_NAME
    assert result.category == "Budha-Aditya Yoga"


def test_budha_aditya_rule_when_not_present():
    context = make_context(
        sun_house=9,
        mercury_house=10,
    )

    rule = BudhaAdityaYogaRule()

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
        sun_house=house,
        mercury_house=house,
    )

    result = detect_budha_aditya(
        context
    )

    assert result.detected is True
    assert result.involved_houses == [house]