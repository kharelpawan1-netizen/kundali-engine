
"""
Tests for the BirthChart model.

Tests:
    - Planet management
    - House management
    - Planetary aspects
    - House aspects
    - Dasha storage
    - Yoga storage
    - Divisional charts
    - Chart status
    - String representation

Compatible with Python 3.9+
"""

from dataclasses import dataclass

import pytest

from models.chart import BirthChart
from models.house import House
from models.planet import Planet


# ============================================================
# MOCK OBJECTS
# ============================================================

@dataclass(frozen=True)
class MockAspect:
    planet: str


@dataclass
class MockDasha:
    name: str


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def chart():
    """Return a fresh BirthChart for each test."""
    return BirthChart()


@pytest.fixture
def planet():
    """Return a sample Sun planet."""
    return Planet(
        name="Sun",
        longitude=256.2,
        latitude=0,
        distance=1,
        speed=0.98,
    )


@pytest.fixture
def house():
    """Return a sample first house."""
    return House(
        number=1,
        longitude=348.3,
        sign="Pisces",
        sign_number=12,
    )


# ============================================================
# BASIC INITIALIZATION
# ============================================================

def test_chart_initializes_empty(chart):
    assert chart.birth_data is None
    assert chart.planets == {}
    assert chart.houses == {}
    assert chart.aspect_map == {}
    assert chart.planetary_aspects == {}
    assert chart.house_aspects == {}
    assert chart.mahadashas == []
    assert chart.antardashas == []
    assert chart.pratyantardashas == []
    assert chart.sookshmadashas == []
    assert chart.pranadashas == []
    assert chart.dehadashas == []
    assert chart.yogas == []
    assert chart.divisional_charts == {}


# ============================================================
# PLANET METHODS
# ============================================================

def test_add_planet(chart, planet):
    chart.add_planet(planet)

    assert "Sun" in chart.planets
    assert chart.planets["Sun"] is planet


def test_get_planet(chart, planet):
    chart.add_planet(planet)

    result = chart.get_planet("Sun")

    assert result is planet


def test_get_missing_planet_returns_none(chart):
    assert chart.get_planet("Mars") is None


def test_has_planet(chart, planet):
    chart.add_planet(planet)

    assert chart.has_planet("Sun")
    assert not chart.has_planet("Mars")


def test_add_planet_replaces_existing_planet(chart, planet):
    chart.add_planet(planet)

    replacement = Planet(
        name="Sun",
        longitude=100.0,
        latitude=1.0,
        distance=2.0,
        speed=1.0,
    )

    chart.add_planet(replacement)

    assert chart.get_planet("Sun") is replacement
    assert chart.planet_count() == 1


def test_planet_count(chart, planet):
    assert chart.planet_count() == 0

    chart.add_planet(planet)

    assert chart.planet_count() == 1


# ============================================================
# HOUSE METHODS
# ============================================================

def test_add_house(chart, house):
    chart.add_house(house)

    assert 1 in chart.houses
    assert chart.houses[1] is house


def test_get_house(chart, house):
    chart.add_house(house)

    result = chart.get_house(1)

    assert result is house


def test_get_missing_house_returns_none(chart):
    assert chart.get_house(1) is None


def test_has_house(chart, house):
    chart.add_house(house)

    assert chart.has_house(1)
    assert not chart.has_house(2)


def test_add_house_replaces_existing_house(chart, house):
    chart.add_house(house)

    replacement = House(
        number=1,
        longitude=100.0,
        sign="Cancer",
        sign_number=4,
    )

    chart.add_house(replacement)

    assert chart.get_house(1) is replacement
    assert chart.house_count() == 1


def test_house_count(chart, house):
    assert chart.house_count() == 0

    chart.add_house(house)

    assert chart.house_count() == 1


# ============================================================
# PLANETARY ASPECT METHODS
# ============================================================

def test_add_aspect(chart):
    aspect = MockAspect(
        planet="Mars"
    )

    chart.add_aspect(aspect)

    assert "Mars" in chart.aspect_map
    assert aspect in chart.aspect_map["Mars"]


def test_add_multiple_aspects(chart):
    aspect_one = MockAspect(
        planet="Mars"
    )

    aspect_two = MockAspect(
        planet="Mars"
    )

    chart.add_aspect(aspect_one)
    chart.add_aspect(aspect_two)

    assert len(chart.get_aspects("Mars")) == 2


def test_get_aspects_for_missing_planet(chart):
    assert chart.get_aspects("Mars") == []


# ============================================================
# PLANET-TO-PLANET ASPECT METHODS
# ============================================================

def test_add_planetary_aspect(chart):
    chart.add_planetary_aspect(
        "Mars",
        "Moon",
    )

    assert chart.planetary_aspects["Mars"] == [
        "Moon"
    ]


def test_add_planetary_aspect_prevents_duplicates(chart):
    chart.add_planetary_aspect(
        "Mars",
        "Moon",
    )

    chart.add_planetary_aspect(
        "Mars",
        "Moon",
    )

    assert chart.planetary_aspects["Mars"] == [
        "Moon"
    ]


def test_add_multiple_planetary_aspects(chart):
    chart.add_planetary_aspect(
        "Mars",
        "Moon",
    )

    chart.add_planetary_aspect(
        "Mars",
        "Jupiter",
    )

    assert chart.get_planetary_aspects("Mars") == [
        "Moon",
        "Jupiter",
    ]


def test_get_planetary_aspects_for_missing_planet(chart):
    assert chart.get_planetary_aspects("Mars") == []


# ============================================================
# PLANET-TO-HOUSE ASPECT METHODS
# ============================================================

def test_add_house_aspect(chart):
    chart.add_house_aspect(
        4,
        "Mars",
    )

    assert chart.house_aspects[4] == [
        "Mars"
    ]


def test_add_house_aspect_prevents_duplicates(chart):
    chart.add_house_aspect(
        4,
        "Mars",
    )

    chart.add_house_aspect(
        4,
        "Mars",
    )

    assert chart.house_aspects[4] == [
        "Mars"
    ]


def test_add_multiple_house_aspects(chart):
    chart.add_house_aspect(
        4,
        "Mars",
    )

    chart.add_house_aspect(
        4,
        "Jupiter",
    )

    assert chart.get_house_aspects(4) == [
        "Mars",
        "Jupiter",
    ]


def test_get_house_aspects_for_missing_house(chart):
    assert chart.get_house_aspects(4) == []


# ============================================================
# DASHA METHODS
# ============================================================

def test_add_mahadasha(chart):
    dasha = MockDasha(
        name="Sun"
    )

    chart.add_mahadasha(dasha)

    assert chart.mahadashas == [dasha]


def test_add_antardasha(chart):
    dasha = MockDasha(
        name="Moon"
    )

    chart.add_antardasha(dasha)

    assert chart.antardashas == [dasha]


def test_add_pratyantardasha(chart):
    dasha = MockDasha(
        name="Mars"
    )

    chart.add_pratyantardasha(dasha)

    assert chart.pratyantardashas == [dasha]


def test_add_sookshmadasha(chart):
    dasha = MockDasha(
        name="Mercury"
    )

    chart.add_sookshmadasha(dasha)

    assert chart.sookshmadashas == [dasha]


def test_add_pranadasha(chart):
    dasha = MockDasha(
        name="Jupiter"
    )

    chart.add_pranadasha(dasha)

    assert chart.pranadashas == [dasha]


def test_add_dehadasha(chart):
    dasha = MockDasha(
        name="Venus"
    )

    chart.add_dehadasha(dasha)

    assert chart.dehadashas == [dasha]


# ============================================================
# YOGA METHODS
# ============================================================

def test_add_yoga(chart):
    yoga = {
        "name": "Gaja Kesari Yoga"
    }

    chart.add_yoga(yoga)

    assert chart.yogas == [yoga]


def test_add_multiple_yogas(chart):
    yoga_one = {
        "name": "Gaja Kesari Yoga"
    }

    yoga_two = {
        "name": "Budha Aditya Yoga"
    }

    chart.add_yoga(yoga_one)
    chart.add_yoga(yoga_two)

    assert chart.yogas == [
        yoga_one,
        yoga_two,
    ]


# ============================================================
# DIVISIONAL CHART METHODS
# ============================================================

def test_add_divisional_chart(chart):
    d9_chart = {
        "name": "Navamsa"
    }

    chart.add_divisional_chart(
        "D9",
        d9_chart,
    )

    assert chart.divisional_charts["D9"] is d9_chart


def test_get_divisional_chart(chart):
    d9_chart = {
        "name": "Navamsa"
    }

    chart.add_divisional_chart(
        "D9",
        d9_chart,
    )

    assert chart.get_divisional_chart("D9") is d9_chart


def test_get_missing_divisional_chart_returns_none(chart):
    assert chart.get_divisional_chart("D9") is None


def test_add_divisional_chart_replaces_existing(chart):
    first = {
        "name": "First D9"
    }

    second = {
        "name": "Second D9"
    }

    chart.add_divisional_chart(
        "D9",
        first,
    )

    chart.add_divisional_chart(
        "D9",
        second,
    )

    assert chart.get_divisional_chart("D9") is second


# ============================================================
# COMPLETENESS
# ============================================================

def test_empty_chart_is_not_complete(chart):
    assert not chart.is_complete()


def test_chart_with_planets_and_houses_but_no_ascendant_is_not_complete(
    chart,
    planet,
):
    chart.add_planet(planet)

    for number in range(1, 13):
        chart.add_house(
            House(
                number=number,
                longitude=float(number),
                sign="Aries",
                sign_number=1,
            )
        )

    assert not chart.is_complete()


def test_chart_is_complete_when_basic_structure_exists(
    chart,
    planet,
):
    chart.add_planet(planet)

    for number in range(1, 13):
        chart.add_house(
            House(
                number=number,
                longitude=float(number),
                sign="Aries",
                sign_number=1,
            )
        )

    chart.ascendant = 15.0

    assert chart.is_complete()


# ============================================================
# STRING REPRESENTATION
# ============================================================

def test_chart_string_representation(chart):
    result = str(chart)

    assert "BirthChart(" in result
    assert "0 planets" in result
    assert "0 houses" in result


def test_chart_string_representation_counts_planets_and_houses(
    chart,
    planet,
    house,
):
    chart.add_planet(planet)
    chart.add_house(house)

    result = str(chart)

    assert "1 planets" in result
    assert "1 houses" in result


# ============================================================
# COMPLETE WORKFLOW
# ============================================================

def test_basic_chart_workflow(chart, planet, house):
    chart.add_planet(planet)
    chart.add_house(house)

    chart.add_planetary_aspect(
        "Mars",
        "Sun",
    )

    chart.add_house_aspect(
        4,
        "Mars",
    )

    chart.add_yoga(
        {
            "name": "Test Yoga"
        }
    )

    chart.add_divisional_chart(
        "D9",
        {
            "name": "Navamsa"
        },
    )

    assert chart.get_planet("Sun") is planet
    assert chart.get_house(1) is house
    assert chart.get_planetary_aspects("Mars") == [
        "Sun"
    ]
    assert chart.get_house_aspects(4) == [
        "Mars"
    ]
    assert len(chart.yogas) == 1
    assert chart.get_divisional_chart("D9") == {
        "name": "Navamsa"
    }