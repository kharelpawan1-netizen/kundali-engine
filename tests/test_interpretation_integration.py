"""
tests/test_interpretation_integration.py

Integration tests for the complete interpretation layer.

These tests verify that independently computed interpretation
modules can be combined through the chart-level synthesis layer:

    Planet Analysis
          +
    House Analysis
          +
    Dignity Analysis
          +
    Aspect Analysis
          +
    Yoga Analysis
          |
          v
    Chart Synthesis
          |
          v
    ChartInterpretation

The tests intentionally verify module boundaries and data flow.

They do NOT test the internal calculation mathematics of each
interpretation module. Those responsibilities belong to their
respective unit-test modules.

Compatible with Python 3.9.
"""

import pytest

from interpretation.planet_analysis import (
    analyze_planets,
)

from interpretation.house_analysis import (
    analyze_houses,
)

from interpretation.dignity_analysis import (
    analyze_dignities,
)

from interpretation.aspect_analysis import (
    analyze_aspects,
)

from interpretation.yoga_analysis import (
    analyze_yoga_interpretations,
    detected_yoga_interpretations,
)

from interpretation.synthesis import (
    ChartInterpretation,
    synthesize_chart,
    detected_yogas,
    synthesis_report,
)


# ============================================================
# INTEGRATION FIXTURES
# ============================================================

class DummyPlanet:
    """
    Minimal planet object compatible with the interpretation
    modules used by the integration test.
    """

    def __init__(
        self,
        name,
        sign,
        sign_degree,
        house,
        nakshatra=None,
        pada=None,
        dignity=None,
    ):
        self.name = name
        self.sign = sign
        self.sign_degree = sign_degree
        self.house = house
        self.nakshatra = nakshatra
        self.pada = pada
        self.dignity = dignity


class DummyChart:
    """
    Minimal chart object representing a Sagittarius Lagna chart.

    The chart deliberately contains a small planetary set so the
    integration tests remain focused and deterministic.
    """

    ascendant = 256.515697
    ascendant_sign = "Sagittarius"

    planets = {
        "Sun": DummyPlanet(
            name="Sun",
            sign="Sagittarius",
            sign_degree=16.27,
            house=1,
            nakshatra="Purva Ashadha",
            pada=1,
            dignity="Neutral",
        ),
        "Moon": DummyPlanet(
            name="Moon",
            sign="Libra",
            sign_degree=16.59,
            house=11,
            nakshatra="Swati",
            pada=3,
            dignity="Neutral",
        ),
        "Mars": DummyPlanet(
            name="Mars",
            sign="Aquarius",
            sign_degree=3.92,
            house=3,
            nakshatra="Dhanishta",
            pada=4,
            dignity="Neutral",
        ),
    }


class DummyContext:
    """
    Minimal Yoga-analysis context.

    Yoga analysis is deliberately exercised through the public
    Yoga analysis API rather than through structural Yoga classes.
    """

    pass


# ============================================================
# PLANET INTERPRETATION INTEGRATION
# ============================================================

def test_planet_analysis_integrates_with_chart():

    chart = DummyChart()

    interpretations = analyze_planets(
        chart
    )

    assert isinstance(
        interpretations,
        dict,
    )

    assert "Sun" in interpretations
    assert "Moon" in interpretations
    assert "Mars" in interpretations

    sun = interpretations["Sun"]

    assert sun.planet == "Sun"
    assert sun.sign == "Sagittarius"
    assert sun.house == 1


# ============================================================
# HOUSE INTERPRETATION INTEGRATION
# ============================================================

def test_house_analysis_integrates_with_chart():

    chart = DummyChart()

    interpretations = analyze_houses(
        chart
    )

    assert isinstance(
        interpretations,
        dict,
    )

    assert len(
        interpretations
    ) == 12

    assert 1 in interpretations
    assert 5 in interpretations
    assert 9 in interpretations
    assert 12 in interpretations


# ============================================================
# DIGNITY INTERPRETATION INTEGRATION
# ============================================================

def test_dignity_analysis_integrates_with_chart():

    chart = DummyChart()

    interpretations = analyze_dignities(
        chart
    )

    assert isinstance(
        interpretations,
        dict,
    )

    assert "Sun" in interpretations
    assert "Moon" in interpretations
    assert "Mars" in interpretations


# ============================================================
# ASPECT INTERPRETATION INTEGRATION
# ============================================================

def test_aspect_analysis_integrates_with_chart():

    chart = DummyChart()

    interpretations = analyze_aspects(
        chart
    )

    assert isinstance(
        interpretations,
        dict,
    )


# ============================================================
# YOGA INTERPRETATION INTEGRATION
# ============================================================

def test_yoga_analysis_integrates_with_context():

    context = DummyContext()

    interpretations = analyze_yoga_interpretations(
        context
    )

    assert isinstance(
        interpretations,
        list,
    )


def test_detected_yoga_accessor_integrates_with_yoga_analysis():

    context = DummyContext()

    interpretations = detected_yoga_interpretations(
        context
    )

    assert isinstance(
        interpretations,
        list,
    )


# ============================================================
# PLANET + HOUSE + DIGNITY INTEGRATION
# ============================================================

def test_planet_house_dignity_integration():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    assert planetary
    assert houses
    assert dignities

    assert planetary["Sun"].house == 1

    assert (
        houses[1].sign
        == "Sagittarius"
    )

    assert (
        dignities["Sun"].planet
        == "Sun"
    )


# ============================================================
# COMPLETE INTERPRETATION PIPELINE
# ============================================================

def test_complete_interpretation_pipeline():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    aspects = analyze_aspects(
        chart
    )

    yoga_context = DummyContext()

    yogas = analyze_yoga_interpretations(
        yoga_context
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
        aspects=(
            aspects.values()
            if isinstance(
                aspects,
                dict,
            )
            else aspects
        ),
        yogas=yogas,
        metadata={
            "integration_test": True,
        },
    )

    assert isinstance(
        synthesis,
        ChartInterpretation,
    )

    assert synthesis.planet_count == (
        len(planetary)
    )

    assert synthesis.house_count == (
        len(houses)
    )

    assert synthesis.dignity_count == (
        len(dignities)
    )

    assert synthesis.metadata[
        "integration_test"
    ] is True


# ============================================================
# SYNTHESIS PRESERVES PLANETARY DATA
# ============================================================

def test_synthesis_preserves_planetary_interpretations():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values()
    )

    assert "Sun" in synthesis.planetary
    assert "Moon" in synthesis.planetary
    assert "Mars" in synthesis.planetary

    assert (
        synthesis.planetary["Sun"]
        is planetary["Sun"]
    )


# ============================================================
# SYNTHESIS PRESERVES HOUSE DATA
# ============================================================

def test_synthesis_preserves_house_interpretations():

    chart = DummyChart()

    houses = analyze_houses(
        chart
    )

    synthesis = synthesize_chart(
        houses=houses.values()
    )

    assert 1 in synthesis.houses
    assert 5 in synthesis.houses
    assert 9 in synthesis.houses

    assert (
        synthesis.houses[1]
        is houses[1]
    )


# ============================================================
# SYNTHESIS PRESERVES DIGNITY DATA
# ============================================================

def test_synthesis_preserves_dignity_interpretations():

    chart = DummyChart()

    dignities = analyze_dignities(
        chart
    )

    synthesis = synthesize_chart(
        dignities=dignities.values()
    )

    assert "Sun" in synthesis.dignities
    assert "Moon" in synthesis.dignities
    assert "Mars" in synthesis.dignities

    assert (
        synthesis.dignities["Sun"]
        is dignities["Sun"]
    )


# ============================================================
# YOGA DATA FLOW
# ============================================================

def test_yoga_results_flow_into_synthesis():

    context = DummyContext()

    yogas = analyze_yoga_interpretations(
        context
    )

    synthesis = synthesize_chart(
        yogas=yogas
    )

    assert synthesis.yogas == yogas


def test_detected_yogas_flow_into_synthesis():

    context = DummyContext()

    yogas = detected_yoga_interpretations(
        context
    )

    synthesis = synthesize_chart(
        yogas=yogas
    )

    detected = detected_yogas(
        synthesis
    )

    assert detected == yogas


# ============================================================
# THEMES / EVIDENCE / CAUTIONS AGGREGATION
# ============================================================

def test_synthesis_aggregates_interpretive_information():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
    )

    assert isinstance(
        synthesis.themes,
        list,
    )

    assert isinstance(
        synthesis.evidence,
        list,
    )

    assert isinstance(
        synthesis.cautions,
        list,
    )


def test_synthesis_deduplicates_themes():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
    )

    normalized = [
        theme.lower()
        for theme in synthesis.themes
    ]

    assert len(normalized) == len(
        set(normalized)
    )


def test_synthesis_deduplicates_evidence():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values()
    )

    normalized = [
        evidence.lower()
        for evidence in synthesis.evidence
    ]

    assert len(normalized) == len(
        set(normalized)
    )


# ============================================================
# COUNT CONSISTENCY
# ============================================================

def test_chart_interpretation_counts_match_sources():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
    )

    assert (
        synthesis.planet_count
        == len(planetary)
    )

    assert (
        synthesis.house_count
        == len(houses)
    )

    assert (
        synthesis.dignity_count
        == len(dignities)
    )


# ============================================================
# SERIALIZATION INTEGRATION
# ============================================================

def test_complete_synthesis_serializes():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
    )

    data = synthesis.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert "planetary" in data
    assert "houses" in data
    assert "dignities" in data
    assert "aspects" in data
    assert "yogas" in data
    assert "themes" in data
    assert "evidence" in data
    assert "cautions" in data
    assert "metadata" in data

    assert "Sun" in data["planetary"]
    assert 1 in data["houses"]
    assert "Sun" in data["dignities"]


# ============================================================
# REPORT INTEGRATION
# ============================================================

def test_synthesis_report_integrates_with_complete_pipeline():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    aspects = analyze_aspects(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
        aspects=(
            aspects.values()
            if isinstance(
                aspects,
                dict,
            )
            else aspects
        ),
    )

    report = synthesis_report(
        synthesis
    )

    assert isinstance(
        report,
        list,
    )

    assert len(report) >= 5

    assert any(
        "Planetary interpretations:"
        in line
        for line in report
    )

    assert any(
        "House interpretations:"
        in line
        for line in report
    )

    assert any(
        "Dignity interpretations:"
        in line
        for line in report
    )

    assert any(
        "Planetary aspects:"
        in line
        for line in report
    )

    assert any(
        "Structurally detected Yogas:"
        in line
        for line in report
    )


# ============================================================
# EMPTY PIPELINE
# ============================================================

def test_empty_interpretation_pipeline():

    synthesis = synthesize_chart()

    assert isinstance(
        synthesis,
        ChartInterpretation,
    )

    assert synthesis.planet_count == 0
    assert synthesis.house_count == 0
    assert synthesis.dignity_count == 0
    assert synthesis.aspect_count == 0
    assert synthesis.detected_yoga_count == 0

    assert synthesis.themes == []
    assert synthesis.evidence == []
    assert synthesis.cautions == []


# ============================================================
# OPTIONAL INPUTS
# ============================================================

def test_synthesis_accepts_none_for_all_sources():

    synthesis = synthesize_chart(
        planetary=None,
        houses=None,
        dignities=None,
        aspects=None,
        yogas=None,
        metadata=None,
    )

    assert isinstance(
        synthesis,
        ChartInterpretation,
    )

    assert synthesis.planetary == {}
    assert synthesis.houses == {}
    assert synthesis.dignities == {}
    assert synthesis.aspects == {}
    assert synthesis.yogas == []
    assert synthesis.metadata == {}


# ============================================================
# PUBLIC API SANITY
# ============================================================

def test_synthesis_public_api():

    import interpretation.synthesis as module

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

    assert expected.issubset(
        set(module.__all__)
    )


# ============================================================
# CROSS-LAYER IDENTITY CHECK
# ============================================================

def test_synthesis_does_not_recalculate_interpretations():

    chart = DummyChart()

    planetary = analyze_planets(
        chart
    )

    houses = analyze_houses(
        chart
    )

    dignities = analyze_dignities(
        chart
    )

    synthesis = synthesize_chart(
        planetary=planetary.values(),
        houses=houses.values(),
        dignities=dignities.values(),
    )

    assert synthesis.planetary[
        "Sun"
    ] is planetary["Sun"]

    assert synthesis.houses[
        1
    ] is houses[1]

    assert synthesis.dignities[
        "Sun"
    ] is dignities["Sun"]