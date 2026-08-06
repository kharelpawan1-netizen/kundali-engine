"""
Tests for the Yoga Engine foundation.

These tests deliberately test infrastructure only.
Classical Yoga definitions are introduced in later milestones.
"""

from dataclasses import FrozenInstanceError

import pytest

from yogas.base import (
    YogaResult,
    YogaRule,
)

from yogas.analyzer import (
    YogaAnalyzer,
    analyze_yogas,
    detected_yogas,
)


class DummyContext:
    pass


class AlwaysPresentYoga(YogaRule):

    name = "Test Yoga"
    category = "test"

    def evaluate(
        self,
        context,
    ):

        return YogaResult(
            name=self.name,
            detected=True,
            category=self.category,
            strength="strong",
            description="Test Yoga detected.",
            evidence=[
                "Test condition satisfied."
            ],
            involved_planets=[
                "Sun",
                "Jupiter",
            ],
            involved_houses=[
                1,
                5,
            ],
        )


class AlwaysAbsentYoga(YogaRule):

    name = "Absent Test Yoga"
    category = "test"

    def evaluate(
        self,
        context,
    ):

        return YogaResult(
            name=self.name,
            detected=False,
            category=self.category,
            conditions_failed=[
                "Test condition not satisfied."
            ],
        )


def test_yoga_result_creation():

    result = YogaResult(
        name="Test Yoga",
        detected=True,
    )

    assert result.name == "Test Yoga"
    assert result.detected is True
    assert result.is_present is True
    assert result.category == "general"


def test_yoga_result_to_dict():

    result = YogaResult(
        name="Test Yoga",
        detected=True,
        category="raja",
        involved_planets=[
            "Jupiter"
        ],
        involved_houses=[
            1,
            5,
        ],
    )

    data = result.to_dict()

    assert data["name"] == "Test Yoga"
    assert data["detected"] is True
    assert data["category"] == "raja"
    assert data["involved_planets"] == [
        "Jupiter"
    ]
    assert data["involved_houses"] == [
        1,
        5,
    ]


def test_yoga_result_is_immutable():

    result = YogaResult(
        name="Test Yoga",
        detected=True,
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        result.name = "Changed"


def test_analyzer_evaluates_registered_rules():

    context = DummyContext()

    analyzer = YogaAnalyzer(
        [
            AlwaysPresentYoga(),
            AlwaysAbsentYoga(),
        ]
    )

    results = analyzer.evaluate(
        context
    )

    assert len(results) == 2

    assert results[0].name == (
        "Test Yoga"
    )

    assert results[0].detected is True

    assert results[1].name == (
        "Absent Test Yoga"
    )

    assert results[1].detected is False


def test_analyzer_detected_only():

    context = DummyContext()

    analyzer = YogaAnalyzer(
        [
            AlwaysPresentYoga(),
            AlwaysAbsentYoga(),
        ]
    )

    results = analyzer.detected(
        context
    )

    assert len(results) == 1
    assert results[0].name == (
        "Test Yoga"
    )


def test_analyzer_add_rule():

    analyzer = YogaAnalyzer()

    analyzer.add_rule(
        AlwaysPresentYoga()
    )

    assert len(
        analyzer.rules
    ) == 1


def test_analyzer_rejects_invalid_rule():

    analyzer = YogaAnalyzer()

    with pytest.raises(
        TypeError
    ):
        analyzer.add_rule(
            object()
        )


def test_analyzer_rejects_invalid_result():

    class BadRule(YogaRule):

        def evaluate(
            self,
            context,
        ):
            return True

    analyzer = YogaAnalyzer(
        [BadRule()]
    )

    with pytest.raises(
        TypeError
    ):
        analyzer.evaluate(
            DummyContext()
        )


def test_convenience_analyze_yogas():

    context = DummyContext()

    results = analyze_yogas(
        context,
        [
            AlwaysPresentYoga()
        ],
    )

    assert len(results) == 1
    assert results[0].detected is True


def test_convenience_detected_yogas():

    context = DummyContext()

    results = detected_yogas(
        context,
        [
            AlwaysPresentYoga(),
            AlwaysAbsentYoga(),
        ],
    )

    assert len(results) == 1
    assert results[0].name == (
        "Test Yoga"
    )