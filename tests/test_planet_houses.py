"""
Tests for planet-to-house assignment.
"""

from astronomy.houses import whole_sign_houses
from astronomy.planet_houses import (
    assign_planet_to_house,
    assign_planets_to_houses,
)
from models.planet import Planet


def make_planet(
    name: str,
    longitude: float,
) -> Planet:
    """Create a minimal Planet for house-assignment tests."""

    return Planet(
        name=name,
        longitude=longitude,
        latitude=0.0,
        distance=1.0,
        speed=0.0,
    )


def test_assign_planet_to_house():
    """Planet should receive the correct Whole Sign house."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Sun", 15.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 1
    assert planet.house == 1


def test_planet_in_second_house():
    """Planet in the next sign should occupy house 2."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Moon", 45.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 2
    assert planet.house == 2


def test_planet_at_sign_boundary():
    """A planet exactly at 30° should enter the second house."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Mars", 30.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 2


def test_planet_at_zero_degrees():
    """0° should belong to the first house."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Mercury", 0.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 1


def test_longitude_wraparound():
    """Longitudes above 360° should normalize correctly."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Jupiter", 375.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 1
    assert planet.house == 1


def test_negative_longitude():
    """Negative longitudes should normalize correctly."""

    houses = whole_sign_houses(0.0)
    planet = make_planet("Venus", -1.0)

    house = assign_planet_to_house(
        planet,
        houses,
    )

    assert house == 12
    assert planet.house == 12


def test_multiple_planets_are_assigned():
    """Multiple planets should be assigned to their houses."""

    houses = whole_sign_houses(0.0)

    planets = [
        make_planet("Sun", 10.0),
        make_planet("Moon", 40.0),
        make_planet("Mars", 80.0),
    ]

    updated_planets, updated_houses = assign_planets_to_houses(
        planets,
        houses,
    )

    assert [planet.house for planet in updated_planets] == [
        1,
        2,
        3,
    ]

    assert "Sun" in updated_houses[1].planets
    assert "Moon" in updated_houses[2].planets
    assert "Mars" in updated_houses[3].planets


def test_multiple_planets_can_share_house():
    """Several planets may occupy the same house."""

    houses = whole_sign_houses(0.0)

    planets = [
        make_planet("Sun", 5.0),
        make_planet("Mercury", 10.0),
        make_planet("Venus", 25.0),
    ]

    _, updated_houses = assign_planets_to_houses(
        planets,
        houses,
    )

    assert updated_houses[1].planets == [
        "Sun",
        "Mercury",
        "Venus",
    ]


def test_invalid_planet_type():
    """Non-Planet objects should be rejected."""

    houses = whole_sign_houses(0.0)

    try:
        assign_planets_to_houses(
            ["Sun"],
            houses,
        )
    except TypeError as exc:
        assert "Planet" in str(exc)
    else:
        raise AssertionError("Expected TypeError for invalid planet")
