"""
Tests for Parashari planetary aspect analysis.
"""

from dataclasses import dataclass

import pytest

from interpretation.aspect_analysis import (
    ASPECT_RULES,
    AspectInterpretation,
    aspect_houses_from_house,
    aspecting_planets,
    analyze_aspects,
    interpret_aspect,
    planet_aspects,
)


@dataclass
class MockPlanet:
    name: str
    house: int
    sign: str = "Sagittarius"


@dataclass
class MockChart:
    planets: dict


def make_chart():
    return MockChart(
        planets={
            "Mars": MockPlanet(
                name="Mars",
                house=1,
            ),
            "Jupiter": MockPlanet(
                name="Jupiter",
                house=2,
            ),
            "Saturn": MockPlanet(
                name="Saturn",
                house=3,
            ),
            "Sun": MockPlanet(
                name="Sun",
                house=4,
            ),
            "Moon": MockPlanet(
                name="Moon",
                house=5,
            ),
        }
    )


# ============================================================
# ASPECT RULES
# ============================================================

def test_mars_has_special_aspects():
    assert ASPECT_RULES["Mars"] == [4, 7, 8]


def test_jupiter_has_special_aspects():
    assert ASPECT_RULES["Jupiter"] == [5, 7, 9]


def test_saturn_has_special_aspects():
    assert ASPECT_RULES["Saturn"] == [3, 7, 10]


def test_sun_has_seventh_aspect():
    assert ASPECT_RULES["Sun"] == [7]


def test_moon_has_seventh_aspect():
    assert ASPECT_RULES["Moon"] == [7]


# ============================================================
# HOUSE CALCULATION
# ============================================================

def test_planet_aspects_seventh_house():
    assert planet_aspects(
        "Sun",
        1,
    ) == [7]


def test_mars_aspects_from_first_house():
    assert planet_aspects(
        "Mars",
        1,
    ) == [4, 7, 8]


def test_jupiter_aspects_from_second_house():
    assert planet_aspects(
        "Jupiter",
        2,
    ) == [6, 8, 10]


def test_saturn_aspects_from_third_house():
    assert planet_aspects(
        "Saturn",
        3,
    ) == [5, 9, 12]


def test_aspect_houses_wrap_around():
    assert aspect_houses_from_house(
        10,
        [5, 7, 9],
    ) == [2, 4, 6]


def test_invalid_house_low():
    with pytest.raises(ValueError):
        planet_aspects(
            "Mars",
            0,
        )


def test_invalid_house_high():
    with pytest.raises(ValueError):
        planet_aspects(
            "Mars",
            13,
        )


def test_unknown_planet():
    with pytest.raises(ValueError):
        planet_aspects(
            "Pluto",
            1,
        )


# ============================================================
# ASPECT INTERPRETATION
# ============================================================

def test_interpret_aspect_returns_expected_type():

    result = interpret_aspect(
        "Mars",
        1,
        4,
    )

    assert isinstance(
        result,
        AspectInterpretation,
    )


def test_interpret_aspect_contains_planet():
    result = interpret_aspect(
        "Mars",
        1,
        4,
    )

    assert result.planet == "Mars"


def test_interpret_aspect_contains_source_house():
    result = interpret_aspect(
        "Mars",
        1,
        4,
    )

    assert result.source_house == 1


def test_interpret_aspect_contains_target_house():
    result = interpret_aspect(
        "Mars",
        1,
        4,
    )

    assert result.target_house == 4


def test_interpret_aspect_contains_evidence():

    result = interpret_aspect(
        "Mars",
        1,
        4,
    )

    assert result.evidence


# ============================================================
# CHART ANALYSIS
# ============================================================

def test_aspecting_planets():

    chart = make_chart()

    result = aspecting_planets(
        chart,
        4,
    )

    assert "Mars" in result


def test_aspecting_planets_jupiter():

    chart = make_chart()

    result = aspecting_planets(
        chart,
        6,
    )

    assert "Jupiter" in result


def test_analyze_aspects_returns_dictionary():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    assert isinstance(
        result,
        dict,
    )


def test_analyze_aspects_contains_planets():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    assert "Mars" in result
    assert "Jupiter" in result
    assert "Saturn" in result


def test_analyze_aspects_contains_expected_targets():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    assert 4 in result["Mars"]
    assert 7 in result["Mars"]
    assert 8 in result["Mars"]


def test_mars_aspects_fourth_house():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    mars_aspects = result["Mars"]

    assert mars_aspects[4].target_house == 4


def test_jupiter_aspects_fifth_from_second():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    jupiter_aspects = result["Jupiter"]

    assert 6 in jupiter_aspects


def test_saturn_aspects_tenth_from_third():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    saturn_aspects = result["Saturn"]

    assert 12 in saturn_aspects


def test_no_duplicate_aspect_targets():

    chart = make_chart()

    result = analyze_aspects(
        chart,
    )

    for planet_results in result.values():

        targets = list(
            planet_results.keys()
        )

        assert len(targets) == len(
            set(targets)
        )