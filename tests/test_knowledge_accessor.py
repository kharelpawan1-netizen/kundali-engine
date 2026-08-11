"""
tests/test_knowledge_accessor.py

Unit tests for knowledge.accessor.

Verifies the generic BirthChart accessor functions.

Compatible with Python 3.9
"""

from knowledge.accessor import (
    get_house,
    get_houses,
    get_planet,
    get_planets,
    house_count,
    house_exists,
    iter_houses,
    iter_planets,
    planet_count,
    planet_exists,
    planet_names,
)

from models.chart import BirthChart
from models.house import House
from models.planet import Planet


def make_chart() -> BirthChart:
    """
    Create a minimal BirthChart for testing.
    """

    chart = BirthChart()

    mars = Planet(
        name="Mars",
        longitude=10.0,
        latitude=0.0,
        distance=1.0,
        speed=0.5,
    )

    moon = Planet(
        name="Moon",
        longitude=40.0,
        latitude=0.0,
        distance=1.0,
        speed=12.0,
    )

    chart.add_planet(mars)
    chart.add_planet(moon)

    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    for number in range(1, 13):
        chart.add_house(
            House(
                number=number,
                longitude=(number - 1) * 30.0,
                sign=signs[number - 1],
                sign_number=number,
            )
        )

    return chart


# ============================================================
# PLANET TESTS
# ============================================================


def test_get_planet():
    chart = make_chart()

    mars = get_planet(chart, "Mars")

    assert mars is not None
    assert mars.name == "Mars"


def test_get_missing_planet():
    chart = make_chart()

    assert get_planet(chart, "Venus") is None


def test_get_planets():
    chart = make_chart()

    planets = get_planets(chart)

    assert len(planets) == 2
    assert "Mars" in planets
    assert "Moon" in planets


def test_iter_planets():
    chart = make_chart()

    names = [planet.name for planet in iter_planets(chart)]

    assert names == ["Mars", "Moon"]


def test_planet_names():
    chart = make_chart()

    assert planet_names(chart) == ["Mars", "Moon"]


def test_planet_exists():
    chart = make_chart()

    assert planet_exists(chart, "Mars")
    assert not planet_exists(chart, "Venus")


def test_planet_count():
    chart = make_chart()

    assert planet_count(chart) == 2


# ============================================================
# HOUSE TESTS
# ============================================================


def test_get_house():
    chart = make_chart()

    house = get_house(chart, 1)

    assert house is not None
    assert house.number == 1
    assert house.sign == "Aries"


def test_get_missing_house():
    chart = make_chart()

    assert get_house(chart, 13) is None


def test_get_houses():
    chart = make_chart()

    houses = get_houses(chart)

    assert len(houses) == 12


def test_iter_houses():
    chart = make_chart()

    numbers = [house.number for house in iter_houses(chart)]

    assert numbers == list(range(1, 13))


def test_house_exists():
    chart = make_chart()

    assert house_exists(chart, 1)
    assert not house_exists(chart, 13)


def test_house_count():
    chart = make_chart()

    assert house_count(chart) == 12