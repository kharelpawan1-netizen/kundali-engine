"""
tests/test_yoga_analysis.py

Tests for the Parashari Yoga interpretation layer.

These tests verify that:

    YogaResult
        ->
    interpretation.yoga_analysis
        ->
    YogaInterpretation

works correctly without duplicating the structural Yoga
detection logic contained in the yogas package.

Compatible with Python 3.9.
"""

from dataclasses import FrozenInstanceError

import pytest

from interpretation.yoga_analysis import (
    YOGA_THEMES,
    YOGA_CAUTIONS,
    YogaInterpretation,
    interpret_yoga,
    interpret_yoga_results,
    analyze_yoga_interpretations,
    detected_yoga_interpretations,
    yoga_interpretations_by_category,
    yoga_interpretations_involving_planet,
    yoga_interpretations_involving_house,
    yoga_analysis_report,
)

from yogas.base import (
    YogaResult,
    YogaRule,
)


# ============================================================
# TEST HELPERS
# ============================================================

class DummyContext:
    """Minimal context used by YogaRule test doubles."""

    pass


class PresentRajaYoga(YogaRule):
    """Test Yoga rule that always detects Raja Yoga."""

    name = "Raja Yoga"
    category = "Raja Yoga"

    def evaluate(
        self,
        context,
    ):
        return YogaResult(
            name=self.name,
            detected=True,
            category=self.category,
            strength="strong",
            description="Structural Raja Yoga test result.",
            evidence=[
                "Test Raja Yoga condition satisfied."
            ],
            involved_planets=[
                "Sun",
                "Jupiter",
            ],
            involved_houses=[
                1,
                5,
                9,
            ],
            conditions_met=[
                "Lagna lord associated with a trikona lord."
            ],
            conditions_failed=[],
            metadata={
                "source": "test",
                "rule": "present_raja",
            },
        )


class AbsentDhanaYoga(YogaRule):
    """Test Yoga rule that does not detect Dhana Yoga."""

    name = "Dhana Yoga"
    category = "Dhana Yoga"

    def evaluate(
        self,
        context,
    ):
        return YogaResult(
            name=self.name,
            detected=False,
            category=self.category,
            strength=None,
            description="Structural Dhana Yoga test result.",
            evidence=[
                "Primary wealth association not established."
            ],
            involved_planets=[
                "Jupiter",
                "Venus",
            ],
            involved_houses=[
                2,
                11,
            ],
            conditions_met=[],
            conditions_failed=[
                "Required wealth-lord association is absent."
            ],
            metadata={
                "source": "test",
                "rule": "absent_dhana",
            },
        )


class GenericYoga(YogaRule):
    """Yoga with no predefined theme/caution mapping."""

    name = "Test Experimental Yoga"
    category = "experimental"

    def evaluate(
        self,
        context,
    ):
        return YogaResult(
            name=self.name,
            detected=True,
            category=self.category,
            description="Generic test Yoga.",
            involved_planets=[
                "Saturn",
            ],
            involved_houses=[
                6,
            ],
        )


# ============================================================
# YOGA RESULT FIXTURE
# ============================================================

@pytest.fixture
def present_result():
    """Return a complete detected YogaResult."""

    return YogaResult(
        name="Raja Yoga",
        detected=True,
        category="Raja Yoga",
        strength="strong",
        description="A structural Raja Yoga formation.",
        evidence=[
            "Lagna lord connects with a trikona lord."
        ],
        involved_planets=[
            "Sun",
            "Jupiter",
        ],
        involved_houses=[
            1,
            5,
            9,
        ],
        conditions_met=[
            "Lagna lord associated with 5th lord."
        ],
        conditions_failed=[],
        metadata={
            "test": True,
            "formation": "structural",
        },
    )


@pytest.fixture
def absent_result():
    """Return a complete non-detected YogaResult."""

    return YogaResult(
        name="Dhana Yoga",
        detected=False,
        category="Dhana Yoga",
        description="A structural Dhana Yoga evaluation.",
        evidence=[
            "Required wealth association is absent."
        ],
        involved_planets=[
            "Jupiter",
            "Venus",
        ],
        involved_houses=[
            2,
            11,
        ],
        conditions_met=[],
        conditions_failed=[
            "2nd and 11th lords lack the required association."
        ],
        metadata={
            "test": True,
        },
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_yoga_themes_contains_core_yogas():

    assert "Raja Yoga" in YOGA_THEMES
    assert "Dhana Yoga" in YOGA_THEMES
    assert "Gaja Kesari Yoga" in YOGA_THEMES
    assert "Budha-Aditya Yoga" in YOGA_THEMES
    assert "Chandra-Mangala Yoga" in YOGA_THEMES
    assert "Neecha Bhanga Raja Yoga" in YOGA_THEMES


def test_yoga_cautions_contains_core_yogas():

    assert "Raja Yoga" in YOGA_CAUTIONS
    assert "Dhana Yoga" in YOGA_CAUTIONS
    assert "Gaja Kesari Yoga" in YOGA_CAUTIONS
    assert "Budha-Aditya Yoga" in YOGA_CAUTIONS
    assert "Chandra-Mangala Yoga" in YOGA_CAUTIONS
    assert "Neecha Bhanga Raja Yoga" in YOGA_CAUTIONS


# ============================================================
# SINGLE YOGA INTERPRETATION
# ============================================================

def test_interpret_yoga_detected_result(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert isinstance(
        interpretation,
        YogaInterpretation,
    )

    assert interpretation.name == (
        "Raja Yoga"
    )

    assert interpretation.category == (
        "Raja Yoga"
    )

    assert interpretation.detected is True

    assert interpretation.is_present is True

    assert interpretation.interpretive_status == (
        "structurally_present"
    )


def test_interpret_yoga_preserves_description(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.description == (
        present_result.description
    )


def test_interpret_yoga_preserves_strength(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.strength == (
        "strong"
    )


def test_interpret_yoga_preserves_involved_planets(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.involved_planets == [
        "Sun",
        "Jupiter",
    ]


def test_interpret_yoga_preserves_involved_houses(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.involved_houses == [
        1,
        5,
        9,
    ]


def test_interpret_yoga_preserves_conditions(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.conditions_met == [
        "Lagna lord associated with 5th lord."
    ]

    assert interpretation.conditions_failed == []


def test_interpret_yoga_preserves_metadata(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.metadata == {
        "test": True,
        "formation": "structural",
    }


def test_interpret_yoga_preserves_existing_evidence(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert (
        "Lagna lord connects with a trikona lord."
        in interpretation.evidence
    )


def test_interpret_yoga_adds_structural_presence_evidence(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert any(
        "structurally present"
        in evidence
        for evidence in interpretation.evidence
    )


def test_interpret_yoga_uses_named_themes(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.themes == YOGA_THEMES[
        "Raja Yoga"
    ]


def test_interpret_yoga_uses_named_cautions(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    assert interpretation.cautions == YOGA_CAUTIONS[
        "Raja Yoga"
    ]


# ============================================================
# NON-DETECTED YOGA
# ============================================================

def test_interpret_yoga_non_detected_result(
    absent_result,
):

    interpretation = interpret_yoga(
        absent_result
    )

    assert interpretation.detected is False

    assert interpretation.is_present is False

    assert interpretation.interpretive_status == (
        "not_detected"
    )


def test_interpret_yoga_non_detected_adds_absence_evidence(
    absent_result,
):

    interpretation = interpret_yoga(
        absent_result
    )

    assert any(
        "not structurally detected"
        in evidence
        for evidence in interpretation.evidence
    )


def test_interpret_yoga_non_detected_preserves_failed_conditions(
    absent_result,
):

    interpretation = interpret_yoga(
        absent_result
    )

    assert interpretation.conditions_failed == [
        "2nd and 11th lords lack the required association."
    ]


# ============================================================
# INVALID INPUT
# ============================================================

@pytest.mark.parametrize(
    "invalid_result",
    [
        None,
        True,
        False,
        "Raja Yoga",
        {},
        object(),
    ],
)
def test_interpret_yoga_rejects_invalid_input(
    invalid_result,
):

    with pytest.raises(
        TypeError
    ):
        interpret_yoga(
            invalid_result
        )


# ============================================================
# SERIALIZATION
# ============================================================

def test_yoga_interpretation_to_dict(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    data = interpretation.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert data["name"] == (
        "Raja Yoga"
    )

    assert data["category"] == (
        "Raja Yoga"
    )

    assert data["detected"] is True

    assert data["strength"] == (
        "strong"
    )

    assert data["involved_planets"] == [
        "Sun",
        "Jupiter",
    ]

    assert data["involved_houses"] == [
        1,
        5,
        9,
    ]

    assert data["metadata"] == {
        "test": True,
        "formation": "structural",
    }


def test_yoga_interpretation_to_dict_returns_copies(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    data = interpretation.to_dict()

    data["themes"].append(
        "modified"
    )

    data["involved_planets"].append(
        "Mars"
    )

    data["metadata"]["modified"] = True

    assert "modified" not in (
        interpretation.themes
    )

    assert "Mars" not in (
        interpretation.involved_planets
    )

    assert "modified" not in (
        interpretation.metadata
    )


def test_yoga_interpretation_is_immutable(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        interpretation.name = (
            "Changed"
        )


# ============================================================
# COLLECTION INTERPRETATION
# ============================================================

def test_interpret_yoga_results_preserves_order(
    present_result,
    absent_result,
):

    results = [
        present_result,
        absent_result,
    ]

    interpretations = interpret_yoga_results(
        results
    )

    assert len(
        interpretations
    ) == 2

    assert interpretations[0].name == (
        "Raja Yoga"
    )

    assert interpretations[1].name == (
        "Dhana Yoga"
    )


def test_interpret_yoga_results_preserves_non_detected_results(
    present_result,
    absent_result,
):

    interpretations = interpret_yoga_results(
        [
            present_result,
            absent_result,
        ]
    )

    assert any(
        not interpretation.detected
        for interpretation
        in interpretations
    )


def test_interpret_yoga_results_accepts_empty_iterable():

    interpretations = interpret_yoga_results(
        []
    )

    assert interpretations == []


# ============================================================
# CHART YOGA ANALYSIS
# ============================================================

def test_analyze_yoga_interpretations_returns_all_results():

    context = DummyContext()

    results = analyze_yoga_interpretations(
        context,
        [
            PresentRajaYoga(),
            AbsentDhanaYoga(),
        ],
    )

    assert len(
        results
    ) == 2

    assert results[0].name == (
        "Raja Yoga"
    )

    assert results[0].detected is True

    assert results[1].name == (
        "Dhana Yoga"
    )

    assert results[1].detected is False


def test_analyze_yoga_interpretations_detected_only():

    context = DummyContext()

    results = analyze_yoga_interpretations(
        context,
        [
            PresentRajaYoga(),
            AbsentDhanaYoga(),
        ],
        detected_only=True,
    )

    assert len(
        results
    ) == 1

    assert results[0].name == (
        "Raja Yoga"
    )

    assert results[0].detected is True


def test_analyze_yoga_interpretations_with_empty_rules():

    context = DummyContext()

    results = analyze_yoga_interpretations(
        context,
        [],
    )

    assert results == []


def test_analyze_yoga_interpretations_does_not_create_implicit_rules():

    context = DummyContext()

    results = analyze_yoga_interpretations(
        context
    )

    assert results == []


# ============================================================
# DETECTED YOGA ACCESSOR
# ============================================================

def test_detected_yoga_interpretations_returns_only_detected():

    context = DummyContext()

    results = detected_yoga_interpretations(
        context,
        [
            PresentRajaYoga(),
            AbsentDhanaYoga(),
        ],
    )

    assert len(
        results
    ) == 1

    assert results[0].name == (
        "Raja Yoga"
    )

    assert results[0].detected is True


def test_detected_yoga_interpretations_with_no_rules():

    context = DummyContext()

    results = detected_yoga_interpretations(
        context
    )

    assert results == []


# ============================================================
# CATEGORY FILTER
# ============================================================

def test_yoga_interpretations_by_category(
    present_result,
    absent_result,
):

    interpretations = interpret_yoga_results(
        [
            present_result,
            absent_result,
        ]
    )

    results = yoga_interpretations_by_category(
        interpretations,
        "Raja Yoga",
    )

    assert len(
        results
    ) == 1

    assert results[0].name == (
        "Raja Yoga"
    )


def test_yoga_interpretations_by_category_is_case_insensitive(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    results = yoga_interpretations_by_category(
        [interpretation],
        "raja yoga",
    )

    assert len(
        results
    ) == 1


def test_yoga_interpretations_by_category_returns_empty_for_unknown_category(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    results = yoga_interpretations_by_category(
        [interpretation],
        "unknown",
    )

    assert results == []


def test_yoga_interpretations_by_category_rejects_none(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    with pytest.raises(
        ValueError
    ):
        yoga_interpretations_by_category(
            [interpretation],
            None,
        )


# ============================================================
# PLANET FILTER
# ============================================================

def test_yoga_interpretations_involving_planet(
    present_result,
    absent_result,
):

    interpretations = interpret_yoga_results(
        [
            present_result,
            absent_result,
        ]
    )

    results = yoga_interpretations_involving_planet(
        interpretations,
        "Jupiter",
    )

    assert len(
        results
    ) == 2


def test_yoga_interpretations_involving_planet_is_case_insensitive(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    results = yoga_interpretations_involving_planet(
        [interpretation],
        "jupiter",
    )

    assert len(
        results
    ) == 1


def test_yoga_interpretations_involving_planet_returns_empty_for_unknown_planet(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    results = yoga_interpretations_involving_planet(
        [interpretation],
        "Saturn",
    )

    assert results == []


def test_yoga_interpretations_involving_planet_rejects_none(
    present_result,
):

    interpretation = interpret_yoga(
        present_result
    )

    with pytest.raises(
        ValueError
    ):
        yoga_interpretations_involving_planet(
            [interpretation],
            None,
        )


# ============================================================
# HOUSE FILTER
# ============================================================

def test_yoga_interpretations_involving_house(
    present_result,
    absent_result,
):

    interpretations = interpret_yoga_results(
        [
            present_result,
            absent_result,
        ]
    )

    results = yoga_interpretations_involving_house(
        interpretations,
        5,
    )

    assert len(
        results
    ) == 1

    assert results[0].name == (
        "Raja Yoga"
    )


@pytest.mark.parametrize(
    "house",
    [
        0,
        -1,
        13,
        100,
    ],
)
def test_yoga_interpretations_involving_house_rejects_invalid_house(
    present_result,
    house,
):

    interpretation = interpret_yoga(
        present_result
    )

    with pytest.raises(
        ValueError
    ):
        yoga_interpretations_involving_house(
            [interpretation],
            house,
        )


# ============================================================
# FALLBACK THEMES AND CAUTIONS
# ============================================================

def test_unknown_yoga_uses_fallback_themes():

    result = YogaResult(
        name="Unknown Yoga",
        detected=True,
        category="unknown",
    )

    interpretation = interpret_yoga(
        result
    )

    assert interpretation.themes == [
        "interpretation depends on the specific Yoga formation",
    ]


def test_unknown_yoga_uses_fallback_cautions():

    result = YogaResult(
        name="Unknown Yoga",
        detected=True,
        category="unknown",
    )

    interpretation = interpret_yoga(
        result
    )

    assert interpretation.cautions == [
        "Structural Yoga formation should not be treated as a guaranteed prediction."
    ]


def test_category_fallback_for_themes():

    result = YogaResult(
        name="Custom Raja Formation",
        detected=True,
        category="Raja Yoga",
    )

    interpretation = interpret_yoga(
        result
    )

    assert interpretation.themes == YOGA_THEMES[
        "Raja Yoga"
    ]


def test_category_fallback_for_cautions():

    result = YogaResult(
        name="Custom Raja Formation",
        detected=True,
        category="Raja Yoga",
    )

    interpretation = interpret_yoga(
        result
    )

    assert interpretation.cautions == YOGA_CAUTIONS[
        "Raja Yoga"
    ]


# ============================================================
# GENERIC YOGA FALLBACK
# ============================================================

def test_generic_yoga_interpretation():

    result = YogaResult(
        name="Test Experimental Yoga",
        detected=True,
        category="experimental",
    )

    interpretation = interpret_yoga(
        result
    )

    assert interpretation.name == (
        "Test Experimental Yoga"
    )

    assert interpretation.category == (
        "experimental"
    )

    assert interpretation.detected is True

    assert interpretation.themes == [
        "interpretation depends on the specific Yoga formation",
    ]

    assert interpretation.cautions == [
        "Structural Yoga formation should not be treated as a guaranteed prediction."
    ]


# ============================================================
# REPORT
# ============================================================

def test_yoga_analysis_report_detected_only():

    context = DummyContext()

    report = yoga_analysis_report(
        context,
        [
            PresentRajaYoga(),
            AbsentDhanaYoga(),
        ],
    )

    assert len(
        report
    ) == 1

    assert report[0].startswith(
        "Raja Yoga: detected;"
    )

    assert "category=Raja Yoga" in (
        report[0]
    )

    assert "Sun, Jupiter" in (
        report[0]
    )

    assert "1, 5, 9" in (
        report[0]
    )


def test_yoga_analysis_report_includes_non_detected_when_requested():

    context = DummyContext()

    report = yoga_analysis_report(
        context,
        [
            PresentRajaYoga(),
            AbsentDhanaYoga(),
        ],
        detected_only=False,
    )

    assert len(
        report
    ) == 2

    assert report[0].startswith(
        "Raja Yoga: detected;"
    )

    assert report[1].startswith(
        "Dhana Yoga: not detected;"
    )


def test_yoga_analysis_report_with_no_rules():

    context = DummyContext()

    report = yoga_analysis_report(
        context
    )

    assert report == []


# ============================================================
# FULL INTEGRATION PATH
# ============================================================

def test_full_yoga_interpretation_pipeline():

    context = DummyContext()

    rules = [
        PresentRajaYoga(),
        AbsentDhanaYoga(),
    ]

    all_results = analyze_yoga_interpretations(
        context,
        rules,
    )

    detected_results = detected_yoga_interpretations(
        context,
        rules,
    )

    assert len(
        all_results
    ) == 2

    assert len(
        detected_results
    ) == 1

    assert detected_results[0].name == (
        all_results[0].name
    )

    assert detected_results[0].detected is True

    category_results = (
        yoga_interpretations_by_category(
            all_results,
            "Raja Yoga",
        )
    )

    assert len(
        category_results
    ) == 1

    planet_results = (
        yoga_interpretations_involving_planet(
            all_results,
            "Jupiter",
        )
    )

    assert len(
        planet_results
    ) == 2

    house_results = (
        yoga_interpretations_involving_house(
            all_results,
            5,
        )
    )

    assert len(
        house_results
    ) == 1

    serialized = (
        detected_results[0].to_dict()
    )

    assert serialized["name"] == (
        "Raja Yoga"
    )

    assert serialized["detected"] is True


# ============================================================
# PUBLIC API SANITY
# ============================================================

def test_public_api_exports():

    import interpretation.yoga_analysis as module

    expected = {
        "YOGA_THEMES",
        "YOGA_CAUTIONS",
        "YogaInterpretation",
        "interpret_yoga",
        "interpret_yoga_results",
        "analyze_yoga_interpretations",
        "detected_yoga_interpretations",
        "yoga_interpretations_by_category",
        "yoga_interpretations_involving_planet",
        "yoga_interpretations_involving_house",
        "yoga_analysis_report",
    }

    assert expected.issubset(
        set(module.__all__)
    )