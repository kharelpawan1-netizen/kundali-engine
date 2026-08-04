"""
Tests for planetary dignity interpretation.

The tests follow the dignity hierarchy used by the
Kundali Engine:

    Exalted
    Debilitated
    Moolatrikona
    Own Sign
    Friend
    Neutral
    Enemy

Compatible with Python 3.9.
"""

from dataclasses import dataclass

import pytest

from interpretation.dignity_analysis import (
    DignityInterpretation,
    analyze_dignities,
    dignity_analysis_report,
    interpret_dignity,
)


# ============================================================
# MOCK CHART MODELS
# ============================================================

@dataclass
class MockPlanet:
    name: str
    sign: str
    sign_degree: float = 15.0


@dataclass
class MockChart:
    planets: dict


def make_chart():
    """
    Create a simple mock chart for testing.
    """

    return MockChart(
        planets={
            "Sun": MockPlanet(
                name="Sun",
                sign="Leo",
                sign_degree=15.0,
            ),
            "Moon": MockPlanet(
                name="Moon",
                sign="Cancer",
                sign_degree=15.0,
            ),
            "Mars": MockPlanet(
                name="Mars",
                sign="Aries",
                sign_degree=10.0,
            ),
            "Jupiter": MockPlanet(
                name="Jupiter",
                sign="Sagittarius",
                sign_degree=15.0,
            ),
            "Saturn": MockPlanet(
                name="Saturn",
                sign="Aries",
                sign_degree=20.0,
            ),
        }
    )


# ============================================================
# BASIC DIGNITY TESTS
# ============================================================

def test_sun_exalted():
    result = interpret_dignity(
        "Sun",
        "Aries",
        10.0,
    )

    assert result.is_exalted
    assert result.dignity == "Exalted"


def test_sun_own_sign():
    """
    Sun in Leo at 15° is Moolatrikona according
    to the configured dignity rules.

    Therefore the result should identify the
    more specific Moolatrikona dignity rather
    than generic Own Sign.
    """

    result = interpret_dignity(
        "Sun",
        "Leo",
        15.0,
    )

    assert result.is_own_sign
    assert result.is_moolatrikona
    assert result.dignity == "Moolatrikona"


def test_sun_moolatrikona():
    result = interpret_dignity(
        "Sun",
        "Leo",
        15.0,
    )

    assert result.is_moolatrikona
    assert result.dignity == "Moolatrikona"


def test_saturn_debilitated():
    result = interpret_dignity(
        "Saturn",
        "Aries",
        20.0,
    )

    assert result.is_debilitated
    assert result.dignity == "Debilitated"


def test_mars_own_sign():
    """
    Mars in Aries is both an own sign and
    Moolatrikona sign under the configured rules.

    The specific dignity takes precedence.
    """

    result = interpret_dignity(
        "Mars",
        "Aries",
        10.0,
    )

    assert result.is_own_sign
    assert result.is_moolatrikona
    assert result.dignity == "Moolatrikona"


def test_jupiter_moolatrikona():
    result = interpret_dignity(
        "Jupiter",
        "Sagittarius",
        5.0,
    )

    assert result.is_own_sign
    assert result.is_moolatrikona
    assert result.dignity == "Moolatrikona"


# ============================================================
# NEUTRAL DIGNITY
# ============================================================

def test_neutral_dignity():
    result = interpret_dignity(
        "Sun",
        "Gemini",
        15.0,
    )

    assert result.dignity == "Neutral"


# ============================================================
# STRUCTURED INTERPRETATION
# ============================================================

def test_interpret_planet_dignity():
    result = interpret_dignity(
        "Sun",
        "Aries",
        10.0,
    )

    assert isinstance(
        result,
        DignityInterpretation,
    )


# ============================================================
# COMPLETE CHART ANALYSIS
# ============================================================

def test_analyze_dignities_returns_dictionary():

    chart = make_chart()

    result = analyze_dignities(
        chart,
    )

    assert isinstance(
        result,
        dict,
    )


def test_analyze_dignities_contains_planets():

    chart = make_chart()

    result = analyze_dignities(
        chart,
    )

    assert "Sun" in result
    assert "Moon" in result
    assert "Mars" in result
    assert "Jupiter" in result
    assert "Saturn" in result


def test_analyze_dignities_values_are_structured():

    chart = make_chart()

    result = analyze_dignities(
        chart,
    )

    for dignity in result.values():

        assert isinstance(
            dignity,
            DignityInterpretation,
        )


# ============================================================
# REPORT
# ============================================================

def test_dignity_analysis_report():

    chart = make_chart()

    result = dignity_analysis_report(
        chart,
    )

    assert result

    assert isinstance(
        result,
        str,
    )


# ============================================================
# VALIDATION
# ============================================================

def test_invalid_planet():

    with pytest.raises(ValueError):

        interpret_dignity(
            "Pluto",
            "Leo",
            15.0,
        )


def test_invalid_sign():

    with pytest.raises(ValueError):

        interpret_dignity(
            "Sun",
            "Atlantis",
            15.0,
        )