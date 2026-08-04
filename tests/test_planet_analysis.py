from datetime import datetime

import pytest

from interpretation.planet_analysis import (
    PlanetInterpretation,
    SIGNS,
    SIGN_LORDS,
    sign_index,
    house_from_sign,
    sign_for_house,
    house_lord,
    planetary_lordships,
    natural_planet_type,
    functional_planet_type,
    interpret_planet,
    analyze_planets,
    planet_analysis_report,
)


# ============================================================
# Dummy Planet
# ============================================================

class DummyPlanet:
    def __init__(
        self,
        name,
        sign,
        sign_degree,
        house=None,
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


# ============================================================
# Dummy Chart
# ============================================================

class DummyChart:
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


# ============================================================
# Sign Tests
# ============================================================

def test_sign_index():
    assert sign_index("Aries") == 0
    assert sign_index("Sagittarius") == 8
    assert sign_index("Pisces") == 11


def test_sign_index_case_insensitive():
    assert sign_index("aries") == 0
    assert sign_index("SAGITTARIUS") == 8


def test_sign_index_invalid():
    with pytest.raises(ValueError):
        sign_index("InvalidSign")


# ============================================================
# House Calculation Tests
# ============================================================

def test_house_from_sign():
    assert house_from_sign(
        "Sagittarius",
        "Sagittarius",
    ) == 1

    assert house_from_sign(
        "Sagittarius",
        "Capricorn",
    ) == 2

    assert house_from_sign(
        "Sagittarius",
        "Libra",
    ) == 11


def test_house_from_sign_wraparound():
    assert house_from_sign(
        "Aries",
        "Pisces",
    ) == 12


def test_sign_for_house():
    assert sign_for_house(
        "Sagittarius",
        1,
    ) == "Sagittarius"

    assert sign_for_house(
        "Sagittarius",
        2,
    ) == "Capricorn"

    assert sign_for_house(
        "Sagittarius",
        12,
    ) == "Scorpio"


def test_sign_for_house_invalid():
    with pytest.raises(ValueError):
        sign_for_house(
            "Sagittarius",
            13,
        )


# ============================================================
# House Lord Tests
# ============================================================

def test_house_lord_sagittarius_lagna():
    # Sagittarius Lagna:
    # 1st Sagittarius -> Jupiter
    # 2nd Capricorn -> Saturn
    # 3rd Aquarius -> Saturn
    # 4th Pisces -> Jupiter
    # 5th Aries -> Mars
    # 6th Taurus -> Venus
    # 7th Gemini -> Mercury
    # 8th Cancer -> Moon
    # 9th Leo -> Sun
    # 10th Virgo -> Mercury
    # 11th Libra -> Venus
    # 12th Scorpio -> Mars

    assert house_lord(
        "Sagittarius",
        1,
    ) == "Jupiter"

    assert house_lord(
        "Sagittarius",
        2,
    ) == "Saturn"

    assert house_lord(
        "Sagittarius",
        5,
    ) == "Mars"

    assert house_lord(
        "Sagittarius",
        9,
    ) == "Sun"

    assert house_lord(
        "Sagittarius",
        10,
    ) == "Mercury"


# ============================================================
# Planetary Lordship Tests
# ============================================================

def test_planetary_lordships_sagittarius():
    assert planetary_lordships(
        "Sagittarius",
        "Jupiter",
    ) == [1, 4]

    assert planetary_lordships(
        "Sagittarius",
        "Saturn",
    ) == [2, 3]

    assert planetary_lordships(
        "Sagittarius",
        "Mars",
    ) == [5, 12]

    assert planetary_lordships(
        "Sagittarius",
        "Mercury",
    ) == [7, 10]


def test_nodes_have_no_classical_lordships():
    assert planetary_lordships(
        "Sagittarius",
        "Rahu",
    ) == []

    assert planetary_lordships(
        "Sagittarius",
        "Ketu",
    ) == []


# ============================================================
# Natural Nature Tests
# ============================================================

def test_natural_planet_type():
    assert natural_planet_type(
        "Jupiter"
    ) == "benefic"

    assert natural_planet_type(
        "Venus"
    ) == "benefic"

    assert natural_planet_type(
        "Moon"
    ) == "benefic"

    assert natural_planet_type(
        "Sun"
    ) == "malefic"

    assert natural_planet_type(
        "Mars"
    ) == "malefic"

    assert natural_planet_type(
        "Saturn"
    ) == "malefic"

    assert natural_planet_type(
        "Rahu"
    ) == "malefic"

    assert natural_planet_type(
        "Ketu"
    ) == "malefic"


# ============================================================
# Functional Nature Tests
# ============================================================

def test_functional_planet_type_sagittarius():
    # Jupiter owns 1 and 4.
    # Because it owns the Lagna, it receives
    # functional benefic classification.
    assert functional_planet_type(
        "Sagittarius",
        "Jupiter",
    ) == "functional_benefic"


def test_functional_planet_type_trikona_lord():
    # Mars owns 5 and 12 for Sagittarius Lagna.
    # 5th lord gives functional benefic bias.
    assert functional_planet_type(
        "Sagittarius",
        "Mars",
    ) == "functional_benefic"


def test_functional_planet_type_dusthana_lord():
    # Venus owns 6 and 11 for Sagittarius Lagna.
    # 6th lord receives functional malefic classification.
    assert functional_planet_type(
        "Sagittarius",
        "Venus",
    ) == "functional_malefic"


def test_functional_planet_type_node():
    assert functional_planet_type(
        "Sagittarius",
        "Rahu",
    ) == "node"

    assert functional_planet_type(
        "Sagittarius",
        "Ketu",
    ) == "node"


# ============================================================
# Planet Interpretation Tests
# ============================================================

def test_interpret_planet_sun():
    chart = DummyChart()

    result = interpret_planet(
        chart,
        chart.planets["Sun"],
    )

    assert isinstance(
        result,
        PlanetInterpretation,
    )

    assert result.planet == "Sun"
    assert result.sign == "Sagittarius"
    assert result.house == 1
    assert result.sign_degree == 16.27

    assert result.house_lordships == [9]
    assert result.is_lagna_lord is False

    assert result.natural_type == "malefic"

    assert result.nakshatra == "Purva Ashadha"
    assert result.pada == 1

    assert result.dignity == "Neutral"


def test_interpret_planet_mars():
    chart = DummyChart()

    result = interpret_planet(
        chart,
        chart.planets["Mars"],
    )

    assert result.planet == "Mars"
    assert result.sign == "Aquarius"
    assert result.house == 3

    assert result.house_lordships == [5, 12]

    assert result.is_lagna_lord is False

    assert result.natural_type == "malefic"

    assert result.functional_type == (
        "functional_benefic"
    )


def test_interpret_planet_contains_keywords():
    chart = DummyChart()

    result = interpret_planet(
        chart,
        chart.planets["Sun"],
    )

    assert "authority" in result.keywords
    assert "leadership" in result.keywords
    assert "status" in result.keywords


def test_interpret_planet_contains_house_theme():
    chart = DummyChart()

    result = interpret_planet(
        chart,
        chart.planets["Sun"],
    )

    assert len(result.themes) == 1
    assert (
        "self"
        in result.themes[0]
    )


def test_interpret_planet_contains_evidence():
    chart = DummyChart()

    result = interpret_planet(
        chart,
        chart.planets["Sun"],
    )

    assert any(
        "Sun occupies Sagittarius in house 1"
        in evidence
        for evidence in result.evidence
    )

    assert any(
        "Sun rules house(s) 9"
        in evidence
        for evidence in result.evidence
    )

    assert any(
        "Natural nature: malefic"
        in evidence
        for evidence in result.evidence
    )


# ============================================================
# Complete Planet Analysis
# ============================================================

def test_analyze_planets():
    chart = DummyChart()

    results = analyze_planets(
        chart
    )

    assert isinstance(
        results,
        dict,
    )

    assert "Sun" in results
    assert "Moon" in results
    assert "Mars" in results

    assert isinstance(
        results["Sun"],
        PlanetInterpretation,
    )

    assert results["Sun"].house == 1
    assert results["Moon"].house == 11
    assert results["Mars"].house == 3


# ============================================================
# Planet Analysis Report
# ============================================================

def test_planet_analysis_report():
    chart = DummyChart()

    report = planet_analysis_report(
        chart
    )

    assert isinstance(
        report,
        list,
    )

    assert len(report) == 3

    assert any(
        line.startswith("Sun:")
        for line in report
    )

    assert any(
        line.startswith("Moon:")
        for line in report
    )

    assert any(
        line.startswith("Mars:")
        for line in report
    )


# ============================================================
# Invalid Planet Tests
# ============================================================

def test_invalid_planet_name():
    with pytest.raises(ValueError):
        natural_planet_type(
            "InvalidPlanet"
        )


def test_invalid_sign_representation():
    chart = DummyChart()

    invalid_planet = DummyPlanet(
        name="Sun",
        sign="InvalidSign",
        sign_degree=10.0,
        house=1,
    )

    with pytest.raises(ValueError):
        interpret_planet(
            chart,
            invalid_planet,
        )