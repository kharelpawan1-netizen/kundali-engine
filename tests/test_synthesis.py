"""
tests/test_synthesis.py

Comprehensive tests for interpretation/synthesis.py.

The synthesis layer is responsible only for aggregating already-computed
interpretation evidence. These tests verify:

    - ChartInterpretation data model
    - serialization
    - normalization
    - theme/evidence/caution collection
    - planetary synthesis
    - house synthesis
    - dignity synthesis
    - aspect synthesis
    - Yoga synthesis
    - complete chart synthesis
    - detected Yoga filtering
    - synthesis reporting
    - duplicate handling
    - invalid/incomplete input handling
    - immutability
    - public API exports

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

import interpretation.synthesis as synthesis_module

from interpretation.synthesis import (
    ChartInterpretation,
    collect_cautions,
    collect_evidence,
    collect_themes,
    detected_yogas,
    synthesize_aspects,
    synthesize_chart,
    synthesize_dignities,
    synthesize_houses,
    synthesize_planets,
    synthesize_yogas,
    synthesis_report,
)


# ============================================================
# TEST HELPERS
# ============================================================


class InterpretationStub:
    """
    Minimal interpretation object used by synthesis tests.

    The production synthesis layer serializes interpretation objects
    through their public to_dict() method. These fixtures therefore
    implement the same contract.
    """

    def __init__(
        self,
        **values,
    ):
        for key, value in values.items():
            setattr(
                self,
                key,
                value,
            )

    def to_dict(self):
        """Return the public interpretation fields."""

        data = {}

        for key, value in self.__dict__.items():
            data[key] = value

        return data

    def __eq__(self, other):
        """Allow fixture comparisons by public attributes."""

        if not isinstance(
            other,
            InterpretationStub,
        ):
            return NotImplemented

        return self.__dict__ == other.__dict__


def make_planet(
    planet="Sun",
    themes=None,
    evidence=None,
    cautions=None,
):
    """Create a minimal planetary interpretation object."""

    return InterpretationStub(
        planet=planet,
        themes=list(themes or []),
        evidence=list(evidence or []),
        cautions=list(cautions or []),
    )


def make_house(
    house=1,
    themes=None,
    evidence=None,
    cautions=None,
):
    """Create a minimal house interpretation object."""

    return InterpretationStub(
        house=house,
        themes=list(themes or []),
        evidence=list(evidence or []),
        cautions=list(cautions or []),
    )


def make_dignity(
    planet="Sun",
    name=None,
    themes=None,
    evidence=None,
    cautions=None,
):
    """Create a minimal dignity interpretation object."""

    values = {
        "themes": list(themes or []),
        "evidence": list(evidence or []),
        "cautions": list(cautions or []),
    }

    if planet is not None:
        values["planet"] = planet

    if name is not None:
        values["name"] = name

    return InterpretationStub(
        **values
    )


def make_aspect(
    planet="Mars",
    target_house=4,
    themes=None,
    evidence=None,
    cautions=None,
):
    """Create a minimal aspect interpretation object."""

    return InterpretationStub(
        planet=planet,
        target_house=target_house,
        themes=list(themes or []),
        evidence=list(evidence or []),
        cautions=list(cautions or []),
    )


def make_yoga(
    name="Raja Yoga",
    detected=True,
    themes=None,
    evidence=None,
    cautions=None,
):
    """Create a minimal Yoga interpretation object."""

    return InterpretationStub(
        name=name,
        detected=detected,
        themes=list(themes or []),
        evidence=list(evidence or []),
        cautions=list(cautions or []),
    )


# ============================================================
# CHART INTERPRETATION DATA MODEL
# ============================================================


def test_chart_interpretation_default_values():
    """ChartInterpretation should initialize all collections safely."""

    result = ChartInterpretation()

    assert result.planetary == {}
    assert result.houses == {}
    assert result.dignities == {}
    assert result.aspects == {}
    assert result.yogas == []
    assert result.themes == []
    assert result.evidence == []
    assert result.cautions == []
    assert result.metadata == {}


def test_chart_interpretation_counts():
    """All count properties should reflect their underlying data."""

    result = ChartInterpretation(
        planetary={
            "Sun": object(),
            "Moon": object(),
        },
        houses={
            1: object(),
            10: object(),
            11: object(),
        },
        dignities={
            "Sun": object(),
        },
        aspects={
            "Mars": {
                4: object(),
                7: object(),
                8: object(),
            },
            "Jupiter": {
                5: object(),
                7: object(),
            },
        },
        yogas=[
            InterpretationStub(detected=True),
            InterpretationStub(detected=False),
            InterpretationStub(detected=True),
        ],
    )

    assert result.planet_count == 2
    assert result.house_count == 3
    assert result.dignity_count == 1
    assert result.aspect_count == 5
    assert result.detected_yoga_count == 2


def test_chart_interpretation_detected_yoga_count_missing_detected_attribute():
    """Missing detected should safely behave as False."""

    result = ChartInterpretation(
        yogas=[
            InterpretationStub(),
            InterpretationStub(detected=True),
            InterpretationStub(detected=False),
        ]
    )

    assert result.detected_yoga_count == 1


def test_chart_interpretation_is_frozen():
    """ChartInterpretation should remain immutable."""

    result = ChartInterpretation()

    with pytest.raises(FrozenInstanceError):
        result.themes = ["authority"]


# ============================================================
# SERIALIZATION
# ============================================================


def test_chart_interpretation_to_dict_contains_all_fields():
    """to_dict should expose every public field."""

    result = ChartInterpretation(
        planetary={"Sun": "planet"},
        houses={1: "house"},
        dignities={"Sun": "dignity"},
        aspects={"Mars": {4: "aspect"}},
        yogas=["yoga"],
        themes=["authority"],
        evidence=["Sun is in house 1."],
        cautions=["Strength requires evaluation."],
        metadata={"source": "test"},
    )

    data = result.to_dict()

    assert set(data.keys()) == {
        "planetary",
        "houses",
        "dignities",
        "aspects",
        "yogas",
        "themes",
        "evidence",
        "cautions",
        "metadata",
    }


def test_chart_interpretation_to_dict_serializes_to_dict_objects():
    """Nested interpretation objects with to_dict should be serialized."""

    class Serializable:
        def to_dict(self):
            return {
                "name": "Sun",
                "value": 10,
            }

    result = ChartInterpretation(
        planetary={
            "Sun": Serializable()
        }
    )

    data = result.to_dict()

    assert data["planetary"]["Sun"] == {
        "name": "Sun",
        "value": 10,
    }


def test_chart_interpretation_to_dict_serializes_nested_sequences():
    """Nested lists and tuples should be recursively serialized."""

    class Serializable:
        def to_dict(self):
            return {"value": 1}

    result = ChartInterpretation(
        yogas=[
            Serializable(),
            (
                Serializable(),
                "plain",
            ),
        ]
    )

    data = result.to_dict()

    assert data["yogas"] == [
        {"value": 1},
        [
            {"value": 1},
            "plain",
        ],
    ]


def test_chart_interpretation_to_dict_returns_collection_copies():
    """to_dict should not expose the original collection objects."""

    themes = ["authority"]
    evidence = ["statement"]
    cautions = ["caution"]
    metadata = {"source": "test"}

    result = ChartInterpretation(
        themes=themes,
        evidence=evidence,
        cautions=cautions,
        metadata=metadata,
    )

    data = result.to_dict()

    data["themes"].append("new")
    data["evidence"].append("new")
    data["cautions"].append("new")
    data["metadata"]["new"] = True

    assert result.themes == ["authority"]
    assert result.evidence == ["statement"]
    assert result.cautions == ["caution"]
    assert result.metadata == {"source": "test"}


# ============================================================
# THEME COLLECTION
# ============================================================


def test_collect_themes_collects_themes():
    """Themes should be collected from interpretation objects."""

    first = make_planet(
        themes=["authority", "leadership"]
    )

    second = make_house(
        themes=["career", "authority"]
    )

    result = collect_themes(
        [first, second]
    )

    assert result == [
        "authority",
        "leadership",
        "career",
    ]


def test_collect_themes_is_case_insensitive_for_duplicates():
    """Duplicate themes should be removed case-insensitively."""

    first = make_planet(
        themes=[
            "Authority",
            "leadership",
        ]
    )

    second = make_house(
        themes=[
            "authority",
            "LEADERSHIP",
        ]
    )

    result = collect_themes(
        [first, second]
    )

    assert result == [
        "Authority",
        "leadership",
    ]


def test_collect_themes_preserves_first_occurrence():
    """The first spelling/order of a theme should be preserved."""

    result = collect_themes(
        [
            make_planet(
                themes=[
                    "  Authority  ",
                    "Leadership",
                ]
            ),
            make_house(
                themes=[
                    "authority",
                    "Career",
                ]
            ),
        ]
    )

    assert result == [
        "Authority",
        "Leadership",
        "Career",
    ]


def test_collect_themes_removes_empty_values():
    """Empty theme strings should not appear."""

    result = collect_themes(
        [
            make_planet(
                themes=[
                    "",
                    "   ",
                    None,
                    "Authority",
                ]
            )
        ]
    )

    assert result == ["Authority"]


def test_collect_themes_accepts_objects_without_themes():
    """Objects without themes should contribute nothing."""

    result = collect_themes(
        [
            object(),
            InterpretationStub(),
            make_planet(themes=["authority"]),
        ]
    )

    assert result == ["authority"]


def test_collect_themes_accepts_empty_iterable():
    """Empty input should return an empty list."""

    assert collect_themes([]) == []


# ============================================================
# EVIDENCE COLLECTION
# ============================================================


def test_collect_evidence_collects_evidence():
    """Evidence should be collected from all interpretation layers."""

    first = make_planet(
        evidence=[
            "Sun occupies house 1.",
            "Sun rules house 5.",
        ]
    )

    second = make_house(
        evidence=[
            "House 10 is occupied.",
            "Sun occupies house 1.",
        ]
    )

    result = collect_evidence(
        [first, second]
    )

    assert result == [
        "Sun occupies house 1.",
        "Sun rules house 5.",
        "House 10 is occupied.",
    ]


def test_collect_evidence_removes_case_insensitive_duplicates():
    """Duplicate evidence should be removed case-insensitively."""

    result = collect_evidence(
        [
            make_planet(
                evidence=["Sun is strong."]
            ),
            make_house(
                evidence=["sun is strong."]
            ),
        ]
    )

    assert result == ["Sun is strong."]


def test_collect_evidence_strips_whitespace():
    """Evidence should be normalized by trimming whitespace."""

    result = collect_evidence(
        [
            make_planet(
                evidence=[
                    "  Sun occupies house 1.  "
                ]
            )
        ]
    )

    assert result == [
        "Sun occupies house 1."
    ]


def test_collect_evidence_ignores_missing_evidence():
    """Objects without evidence should be ignored safely."""

    assert collect_evidence(
        [object(), InterpretationStub()]
    ) == []


def test_collect_evidence_accepts_empty_iterable():
    """Empty input should return an empty evidence list."""

    assert collect_evidence([]) == []


# ============================================================
# CAUTION COLLECTION
# ============================================================


def test_collect_cautions_collects_cautions():
    """Cautions should be collected from interpretation objects."""

    first = make_planet(
        cautions=[
            "Evaluate dignity.",
            "Evaluate strength.",
        ]
    )

    second = make_yoga(
        cautions=[
            "Evaluate strength.",
            "Evaluate timing.",
        ]
    )

    result = collect_cautions(
        [first, second]
    )

    assert result == [
        "Evaluate dignity.",
        "Evaluate strength.",
        "Evaluate timing.",
    ]


def test_collect_cautions_is_case_insensitive():
    """Duplicate cautions should be case-insensitive."""

    result = collect_cautions(
        [
            make_planet(
                cautions=["Evaluate strength."]
            ),
            make_yoga(
                cautions=["evaluate strength."]
            ),
        ]
    )

    assert result == [
        "Evaluate strength."
    ]


def test_collect_cautions_removes_empty_values():
    """Empty caution values should be removed."""

    result = collect_cautions(
        [
            make_planet(
                cautions=[
                    "",
                    " ",
                    None,
                    "Evaluate dignity.",
                ]
            )
        ]
    )

    assert result == [
        "Evaluate dignity."
    ]


def test_collect_cautions_accepts_objects_without_cautions():
    """Objects without cautions should contribute nothing."""

    assert collect_cautions(
        [object(), InterpretationStub()]
    ) == []


# ============================================================
# PLANETARY SYNTHESIS
# ============================================================


def test_synthesize_planets_indexes_by_planet_name():
    """Planetary interpretations should be indexed by planet."""

    sun = make_planet("Sun")
    moon = make_planet("Moon")

    result = synthesize_planets(
        [sun, moon]
    )

    assert result == {
        "Sun": sun,
        "Moon": moon,
    }


def test_synthesize_planets_ignores_missing_planet():
    """Objects without a planet name should be ignored."""

    result = synthesize_planets(
        [
            InterpretationStub(),
            make_planet("Sun"),
        ]
    )

    assert list(result.keys()) == ["Sun"]


def test_synthesize_planets_ignores_empty_planet_name():
    """Empty planet names should be ignored."""

    result = synthesize_planets(
        [
            InterpretationStub(planet=""),
            InterpretationStub(planet="   "),
            make_planet("Sun"),
        ]
    )

    assert result == {
        "Sun": result["Sun"]
    }


def test_synthesize_planets_preserves_last_duplicate():
    """Duplicate planet names should use the latest interpretation."""

    first = make_planet(
        "Sun",
        themes=["first"],
    )

    second = make_planet(
        "Sun",
        themes=["second"],
    )

    result = synthesize_planets(
        [first, second]
    )

    assert result["Sun"] is second


# ============================================================
# HOUSE SYNTHESIS
# ============================================================


@pytest.mark.parametrize(
    "house",
    [1, 2, 6, 10, 12],
)
def test_synthesize_houses_accepts_valid_houses(house):
    """Valid house numbers should be included."""

    interpretation = make_house(
        house=house
    )

    result = synthesize_houses(
        [interpretation]
    )

    assert result[house] is interpretation


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 100],
)
def test_synthesize_houses_ignores_invalid_houses(house):
    """Invalid house numbers should be ignored."""

    interpretation = make_house(
        house=house
    )

    result = synthesize_houses(
        [interpretation]
    )

    assert result == {}


def test_synthesize_houses_ignores_missing_house():
    """Objects without a house should be ignored."""

    result = synthesize_houses(
        [
            InterpretationStub(),
            make_house(1),
        ]
    )

    assert result == {
        1: result[1]
    }


def test_synthesize_houses_converts_numeric_house():
    """Numeric string house values should be converted to integers."""

    interpretation = InterpretationStub(
        house="10"
    )

    result = synthesize_houses(
        [interpretation]
    )

    assert 10 in result
    assert "10" not in result


def test_synthesize_houses_preserves_last_duplicate():
    """Duplicate house numbers should use the latest interpretation."""

    first = make_house(
        10,
        themes=["first"],
    )

    second = make_house(
        10,
        themes=["second"],
    )

    result = synthesize_houses(
        [first, second]
    )

    assert result[10] is second


# ============================================================
# DIGNITY SYNTHESIS
# ============================================================


def test_synthesize_dignities_uses_planet_attribute():
    """Planet attribute should be preferred."""

    dignity = make_dignity(
        planet="Sun"
    )

    result = synthesize_dignities(
        [dignity]
    )

    assert result["Sun"] is dignity


def test_synthesize_dignities_falls_back_to_name():
    """Name should be used when planet is unavailable."""

    dignity = make_dignity(
        planet=None,
        name="Moon",
    )

    result = synthesize_dignities(
        [dignity]
    )

    assert result["Moon"] is dignity


def test_synthesize_dignities_ignores_missing_name():
    """Objects without planet or name should be ignored."""

    result = synthesize_dignities(
        [
            InterpretationStub(),
            InterpretationStub(planet=""),
            InterpretationStub(name=""),
        ]
    )

    assert result == {}


def test_synthesize_dignities_prefers_planet_over_name():
    """Planet attribute should take precedence over name."""

    dignity = make_dignity(
        planet="Sun",
        name="Moon",
    )

    result = synthesize_dignities(
        [dignity]
    )

    assert result == {
        "Sun": dignity
    }


# ============================================================
# ASPECT SYNTHESIS
# ============================================================


def test_synthesize_aspects_groups_by_planet_and_target_house():
    """Aspects should be grouped by planet and target house."""

    mars_4 = make_aspect(
        planet="Mars",
        target_house=4,
    )

    mars_7 = make_aspect(
        planet="Mars",
        target_house=7,
    )

    jupiter_5 = make_aspect(
        planet="Jupiter",
        target_house=5,
    )

    result = synthesize_aspects(
        [
            mars_4,
            mars_7,
            jupiter_5,
        ]
    )

    assert result == {
        "Mars": {
            4: mars_4,
            7: mars_7,
        },
        "Jupiter": {
            5: jupiter_5,
        },
    }


def test_synthesize_aspects_ignores_missing_planet():
    """Aspects without a planet should be ignored."""

    result = synthesize_aspects(
        [
            InterpretationStub(
                target_house=4
            )
        ]
    )

    assert result == {}


def test_synthesize_aspects_ignores_missing_target_house():
    """Aspects without a target house should be ignored."""

    result = synthesize_aspects(
        [
            InterpretationStub(
                planet="Mars"
            )
        ]
    )

    assert result == {}


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 100],
)
def test_synthesize_aspects_ignores_invalid_target_house(
    house,
):
    """Invalid target houses should be ignored."""

    result = synthesize_aspects(
        [
            make_aspect(
                target_house=house
            )
        ]
    )

    assert result == {}


def test_synthesize_aspects_converts_numeric_target_house():
    """Numeric string target houses should be converted to integers."""

    aspect = make_aspect(
        target_house="7"
    )

    result = synthesize_aspects(
        [aspect]
    )

    assert result["Mars"][7] is aspect


def test_synthesize_aspects_preserves_last_duplicate():
    """Duplicate planet/target pairs should use the latest result."""

    first = make_aspect(
        planet="Mars",
        target_house=4,
        evidence=["first"],
    )

    second = make_aspect(
        planet="Mars",
        target_house=4,
        evidence=["second"],
    )

    result = synthesize_aspects(
        [first, second]
    )

    assert result["Mars"][4] is second


# ============================================================
# YOGA SYNTHESIS
# ============================================================


def test_synthesize_yogas_preserves_order():
    """Yoga interpretations should remain in their original order."""

    first = make_yoga(
        name="Raja Yoga"
    )

    second = make_yoga(
        name="Dhana Yoga"
    )

    third = make_yoga(
        name="Gaja Kesari Yoga"
    )

    result = synthesize_yogas(
        [first, second, third]
    )

    assert result == [
        first,
        second,
        third,
    ]


def test_synthesize_yogas_returns_new_list():
    """Yoga synthesis should create a new list."""

    original = [
        make_yoga("Raja Yoga")
    ]

    result = synthesize_yogas(
        original
    )

    assert result == original
    assert result is not original


def test_synthesize_yogas_accepts_empty_iterable():
    """Empty Yoga input should produce an empty list."""

    assert synthesize_yogas([]) == []


# ============================================================
# COMPLETE SYNTHESIS
# ============================================================


def test_synthesize_chart_with_all_layers():
    """Complete synthesis should aggregate every interpretation layer."""

    sun = make_planet(
        planet="Sun",
        themes=["authority"],
        evidence=["Sun occupies house 1."],
        cautions=["Evaluate strength."],
    )

    house = make_house(
        house=10,
        themes=["career"],
        evidence=["House 10 is prominent."],
        cautions=["Evaluate lordship."],
    )

    dignity = make_dignity(
        planet="Sun",
        themes=["strength"],
        evidence=["Sun is exalted."],
        cautions=["Evaluate exact degree."],
    )

    aspect = make_aspect(
        planet="Jupiter",
        target_house=5,
        themes=["wisdom"],
        evidence=["Jupiter aspects house 5."],
        cautions=["Evaluate Jupiter strength."],
    )

    yoga = make_yoga(
        name="Raja Yoga",
        detected=True,
        themes=["leadership"],
        evidence=["Raja Yoga is structurally present."],
        cautions=["Evaluate timing."],
    )

    result = synthesize_chart(
        planetary=[sun],
        houses=[house],
        dignities=[dignity],
        aspects=[aspect],
        yogas=[yoga],
        metadata={
            "source": "test",
            "version": 1,
        },
    )

    assert result.planetary["Sun"] is sun
    assert result.houses[10] is house
    assert result.dignities["Sun"] is dignity
    assert result.aspects["Jupiter"][5] is aspect
    assert result.yogas == [yoga]

    assert result.themes == [
        "authority",
        "career",
        "strength",
        "wisdom",
        "leadership",
    ]

    assert result.evidence == [
        "Sun occupies house 1.",
        "House 10 is prominent.",
        "Sun is exalted.",
        "Jupiter aspects house 5.",
        "Raja Yoga is structurally present.",
    ]

    assert result.cautions == [
        "Evaluate strength.",
        "Evaluate lordship.",
        "Evaluate exact degree.",
        "Evaluate Jupiter strength.",
        "Evaluate timing.",
    ]

    assert result.metadata == {
        "source": "test",
        "version": 1,
    }


def test_synthesize_chart_with_no_arguments():
    """All synthesis layers should be safely optional."""

    result = synthesize_chart()

    assert isinstance(
        result,
        ChartInterpretation,
    )

    assert result.planetary == {}
    assert result.houses == {}
    assert result.dignities == {}
    assert result.aspects == {}
    assert result.yogas == []
    assert result.themes == []
    assert result.evidence == []
    assert result.cautions == []
    assert result.metadata == {}


def test_synthesize_chart_accepts_generators():
    """Synthesis should accept arbitrary iterables, not only lists."""

    planets = (
        item
        for item in [
            make_planet("Sun"),
            make_planet("Moon"),
        ]
    )

    houses = (
        item
        for item in [
            make_house(1),
            make_house(2),
        ]
    )

    result = synthesize_chart(
        planetary=planets,
        houses=houses,
    )

    assert list(result.planetary.keys()) == [
        "Sun",
        "Moon",
    ]

    assert list(result.houses.keys()) == [
        1,
        2,
    ]


def test_synthesize_chart_preserves_metadata_values():
    """Caller metadata should be preserved."""

    metadata = {
        "chart_id": "TEST-001",
        "ayanamsa": "Lahiri",
        "custom": {
            "value": 42
        },
    }

    result = synthesize_chart(
        metadata=metadata
    )

    assert result.metadata == metadata


def test_synthesize_chart_copies_metadata_mapping():
    """The resulting metadata mapping should not be the same object."""

    metadata = {
        "source": "test"
    }

    result = synthesize_chart(
        metadata=metadata
    )

    assert result.metadata is not metadata


def test_synthesize_chart_does_not_generate_predictions():
    """
    Synthesis should aggregate evidence only and should not invent
    predictive fields.
    """

    result = synthesize_chart(
        planetary=[
            make_planet(
                themes=["authority"],
                evidence=["Sun is in house 10."],
            )
        ]
    )

    data = result.to_dict()

    assert "prediction" not in data
    assert "predictions" not in data
    assert "future" not in data


# ============================================================
# DETECTED YOGAS
# ============================================================


def test_detected_yogas_returns_only_detected():
    """Only structurally detected Yogas should be returned."""

    detected = make_yoga(
        name="Raja Yoga",
        detected=True,
    )

    not_detected = make_yoga(
        name="Dhana Yoga",
        detected=False,
    )

    second_detected = make_yoga(
        name="Gaja Kesari Yoga",
        detected=True,
    )

    synthesis = ChartInterpretation(
        yogas=[
            detected,
            not_detected,
            second_detected,
        ]
    )

    result = detected_yogas(
        synthesis
    )

    assert result == [
        detected,
        second_detected,
    ]


def test_detected_yogas_ignores_objects_without_detected_attribute():
    """Objects without detected should safely be excluded."""

    detected = make_yoga(
        detected=True
    )

    synthesis = ChartInterpretation(
        yogas=[
            InterpretationStub(),
            detected,
        ]
    )

    assert detected_yogas(
        synthesis
    ) == [detected]


def test_detected_yogas_returns_empty_for_no_yogas():
    """No Yogas should produce an empty list."""

    synthesis = ChartInterpretation()

    assert detected_yogas(
        synthesis
    ) == []


# ============================================================
# SYNTHESIS REPORT
# ============================================================


def test_synthesis_report_contains_core_counts():
    """Report should contain all major synthesis counts."""

    synthesis = ChartInterpretation(
        planetary={
            "Sun": object(),
            "Moon": object(),
        },
        houses={
            1: object(),
            10: object(),
        },
        dignities={
            "Sun": object(),
        },
        aspects={
            "Mars": {
                4: object(),
                7: object(),
                8: object(),
            }
        },
        yogas=[
            InterpretationStub(detected=True),
            InterpretationStub(detected=False),
        ],
    )

    report = synthesis_report(
        synthesis
    )

    assert report[0] == (
        "Planetary interpretations: 2."
    )

    assert report[1] == (
        "House interpretations: 2."
    )

    assert report[2] == (
        "Dignity interpretations: 1."
    )

    assert report[3] == (
        "Planetary aspects: 3."
    )

    assert report[4] == (
        "Structurally detected Yogas: 1."
    )


def test_synthesis_report_includes_themes():
    """Themes should be included when available."""

    synthesis = ChartInterpretation(
        themes=[
            "authority",
            "career",
            "wisdom",
        ]
    )

    report = synthesis_report(
        synthesis
    )

    assert report[-1] == (
        "Themes: authority, career, wisdom."
    )


def test_synthesis_report_omits_themes_when_empty():
    """No themes should mean no Themes report line."""

    synthesis = ChartInterpretation()

    report = synthesis_report(
        synthesis
    )

    assert len(report) == 5


def test_synthesis_report_is_evidence_oriented():
    """Report should not introduce deterministic prediction language."""

    synthesis = ChartInterpretation(
        themes=["leadership"]
    )

    report = synthesis_report(
        synthesis
    )

    text = " ".join(report).lower()

    assert "guaranteed" not in text
    assert "will happen" not in text
    assert "certainly" not in text


# ============================================================
# SERIALIZATION HELPERS
# ============================================================


def test_private_serialize_value_handles_plain_values():
    """Plain values should pass through unchanged."""

    assert (
        synthesis_module._serialize_value("Sun")
        == "Sun"
    )

    assert (
        synthesis_module._serialize_value(10)
        == 10
    )

    assert (
        synthesis_module._serialize_value(None)
        is None
    )


def test_private_serialize_value_handles_dicts():
    """Dictionaries should be recursively serialized."""

    value = {
        "a": 1,
        "b": {
            "c": 2
        },
    }

    assert synthesis_module._serialize_value(
        value
    ) == value


def test_private_serialize_value_handles_lists_and_tuples():
    """Lists and tuples should become recursively serialized lists."""

    value = (
        1,
        [2, 3],
    )

    assert synthesis_module._serialize_value(
        value
    ) == [
        1,
        [2, 3],
    ]


def test_private_serialize_mapping():
    """Mapping serialization should process every value."""

    class Serializable:
        def to_dict(self):
            return {"value": 1}

    result = synthesis_module._serialize_mapping(
        {
            "Sun": Serializable(),
            "Moon": 2,
        }
    )

    assert result == {
        "Sun": {"value": 1},
        "Moon": 2,
    }


def test_private_serialize_nested_mapping():
    """Nested mapping serialization should process inner values."""

    class Serializable:
        def to_dict(self):
            return {"value": 1}

    result = synthesis_module._serialize_nested_mapping(
        {
            "Mars": {
                4: Serializable(),
                7: "plain",
            }
        }
    )

    assert result == {
        "Mars": {
            4: {"value": 1},
            7: "plain",
        }
    }


def test_private_serialize_sequence():
    """Sequence serialization should process every item."""

    class Serializable:
        def to_dict(self):
            return {"value": 1}

    result = synthesis_module._serialize_sequence(
        [
            Serializable(),
            "plain",
        ]
    )

    assert result == [
        {"value": 1},
        "plain",
    ]


# ============================================================
# NORMALIZATION HELPERS
# ============================================================


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, ""),
        ("Sun", "Sun"),
        ("  Sun  ", "Sun"),
        (10, "10"),
        (True, "True"),
    ],
)
def test_text_normalization(value, expected):
    """_text should normalize values into stripped strings."""

    assert synthesis_module._text(
        value
    ) == expected


def test_unique_preserve_order():
    """Duplicate normalized strings should be removed in order."""

    result = synthesis_module._unique_preserve_order(
        [
            "Authority",
            "Leadership",
            "authority",
            " ",
            "CAREER",
            "career",
        ]
    )

    assert result == [
        "Authority",
        "Leadership",
        "CAREER",
    ]


# ============================================================
# CROSS-LAYER INTEGRATION
# ============================================================


def test_full_synthesis_pipeline():
    """
    Verify a realistic evidence aggregation pipeline across all
    interpretation categories.
    """

    planetary = [
        make_planet(
            planet="Sun",
            themes=[
                "authority",
                "identity",
            ],
            evidence=[
                "Sun occupies house 10.",
            ],
            cautions=[
                "Evaluate dignity.",
            ],
        ),
        make_planet(
            planet="Jupiter",
            themes=[
                "wisdom",
                "guidance",
            ],
            evidence=[
                "Jupiter occupies house 9.",
            ],
            cautions=[
                "Evaluate strength.",
            ],
        ),
    ]

    houses = [
        make_house(
            house=9,
            themes=[
                "dharma",
                "higher learning",
            ],
            evidence=[
                "House 9 is occupied by Jupiter.",
            ],
            cautions=[
                "Evaluate lordship.",
            ],
        ),
        make_house(
            house=10,
            themes=[
                "career",
                "authority",
            ],
            evidence=[
                "Sun occupies house 10.",
            ],
            cautions=[
                "Evaluate dignity.",
            ],
        ),
    ]

    dignities = [
        make_dignity(
            planet="Sun",
            themes=[
                "strength"
            ],
            evidence=[
                "Sun has recorded dignity."
            ],
            cautions=[
                "Evaluate exact degree."
            ],
        )
    ]

    aspects = [
        make_aspect(
            planet="Jupiter",
            target_house=1,
            themes=[
                "wisdom"
            ],
            evidence=[
                "Jupiter aspects house 1."
            ],
            cautions=[
                "Evaluate Jupiter condition."
            ],
        ),
        make_aspect(
            planet="Saturn",
            target_house=10,
            themes=[
                "discipline"
            ],
            evidence=[
                "Saturn aspects house 10."
            ],
            cautions=[
                "Evaluate Saturn strength."
            ],
        ),
    ]

    yogas = [
        make_yoga(
            name="Raja Yoga",
            detected=True,
            themes=[
                "leadership"
            ],
            evidence=[
                "Raja Yoga is structurally present."
            ],
            cautions=[
                "Evaluate Dasha timing."
            ],
        ),
        make_yoga(
            name="Dhana Yoga",
            detected=False,
            themes=[
                "wealth"
            ],
            evidence=[
                "Dhana Yoga is not structurally detected."
            ],
            cautions=[
                "Evaluate financial factors."
            ],
        ),
    ]

    synthesis = synthesize_chart(
        planetary=planetary,
        houses=houses,
        dignities=dignities,
        aspects=aspects,
        yogas=yogas,
        metadata={
            "pipeline": "integration-test"
        },
    )

    assert synthesis.planet_count == 2
    assert synthesis.house_count == 2
    assert synthesis.dignity_count == 1
    assert synthesis.aspect_count == 2
    assert synthesis.detected_yoga_count == 1

    assert set(
        synthesis.planetary.keys()
    ) == {
        "Sun",
        "Jupiter",
    }

    assert set(
        synthesis.houses.keys()
    ) == {
        9,
        10,
    }

    assert set(
        synthesis.dignities.keys()
    ) == {
        "Sun",
    }

    assert set(
        synthesis.aspects.keys()
    ) == {
        "Jupiter",
        "Saturn",
    }

    assert detected_yogas(
        synthesis
    ) == [yogas[0]]

    assert synthesis.metadata == {
        "pipeline": "integration-test"
    }

    assert "authority" in synthesis.themes
    assert "wisdom" in synthesis.themes
    assert "wealth" in synthesis.themes
    assert "leadership" in synthesis.themes

    assert (
        "Sun occupies house 10."
        in synthesis.evidence
    )

    assert (
        "Evaluate dignity."
        in synthesis.cautions
    )


def test_full_synthesis_serialization_pipeline():
    """A complete synthesis should serialize cleanly."""

    planetary = [
        make_planet(
            "Sun",
            themes=["authority"],
            evidence=["Sun occupies house 10."],
        )
    ]

    houses = [
        make_house(
            10,
            themes=["career"],
            evidence=["House 10 is prominent."],
        )
    ]

    dignities = [
        make_dignity(
            planet="Sun",
            themes=["strength"],
            evidence=["Sun is exalted."],
        )
    ]

    aspects = [
        make_aspect(
            planet="Jupiter",
            target_house=5,
            themes=["wisdom"],
            evidence=["Jupiter aspects house 5."],
        )
    ]

    yogas = [
        make_yoga(
            name="Raja Yoga",
            detected=True,
            themes=["leadership"],
            evidence=[
                "Raja Yoga is structurally present."
            ],
        )
    ]

    synthesis = synthesize_chart(
        planetary=planetary,
        houses=houses,
        dignities=dignities,
        aspects=aspects,
        yogas=yogas,
    )

    serialized = synthesis.to_dict()

    assert serialized["planetary"]["Sun"] == {
        "planet": "Sun",
        "themes": ["authority"],
        "evidence": ["Sun occupies house 10."],
        "cautions": [],
    }

    assert serialized["houses"][10] == {
        "house": 10,
        "themes": ["career"],
        "evidence": ["House 10 is prominent."],
        "cautions": [],
    }

    assert serialized["dignities"]["Sun"] == {
        "planet": "Sun",
        "themes": ["strength"],
        "evidence": ["Sun is exalted."],
        "cautions": [],
    }

    assert serialized["aspects"]["Jupiter"][5] == {
        "planet": "Jupiter",
        "target_house": 5,
        "themes": ["wisdom"],
        "evidence": ["Jupiter aspects house 5."],
        "cautions": [],
    }

    assert serialized["yogas"][0]["name"] == "Raja Yoga"
    assert serialized["yogas"][0]["detected"] is True


# ============================================================
# PUBLIC API
# ============================================================


def test_public_api_exports():
    """All documented public API symbols should be exported."""

    expected = {
        "ChartInterpretation",
        "collect_themes",
        "collect_evidence",
        "collect_cautions",
        "synthesize_planets",
        "synthesize_houses",
        "synthesize_dignities",
        "synthesize_aspects",
        "synthesize_yogas",
        "synthesize_chart",
        "detected_yogas",
        "synthesis_report",
    }

    assert set(
        synthesis_module.__all__
    ) == expected

    for name in expected:
        assert hasattr(
            synthesis_module,
            name,
        )