"""
tests/test_knowledge_planets.py

Tests for the permanent planetary knowledge database.

Compatible with Python 3.9.
"""

from knowledge.planets import (
    PLANETS,
    all_planets,
    get_planet,
)
from knowledge.planet import PlanetFacts
from models.graha import Graha


def test_planets_dictionary_exists():
    assert isinstance(PLANETS, dict)


def test_contains_nine_planets():
    assert len(PLANETS) == 9


def test_every_value_is_planetfacts():
    for planet in PLANETS.values():
        assert isinstance(planet, PlanetFacts)


def test_every_key_is_graha():
    for key in PLANETS.keys():
        assert isinstance(key, Graha)


def test_get_planet_returns_planetfacts():
    sun = get_planet(Graha.SUN)

    assert isinstance(sun, PlanetFacts)
    assert sun.name == "Sun"


def test_get_planet_for_moon():
    moon = get_planet(Graha.MOON)

    assert moon.name == "Moon"
    assert moon.sanskrit_name == "Chandra"


def test_get_planet_for_mars():
    mars = get_planet(Graha.MARS)

    assert mars.name == "Mars"


def test_get_planet_for_mercury():
    mercury = get_planet(Graha.MERCURY)

    assert mercury.name == "Mercury"


def test_get_planet_for_jupiter():
    jupiter = get_planet(Graha.JUPITER)

    assert jupiter.name == "Jupiter"


def test_get_planet_for_venus():
    venus = get_planet(Graha.VENUS)

    assert venus.name == "Venus"


def test_get_planet_for_saturn():
    saturn = get_planet(Graha.SATURN)

    assert saturn.name == "Saturn"


def test_get_planet_for_rahu():
    rahu = get_planet(Graha.RAHU)

    assert rahu.name == "Rahu"


def test_get_planet_for_ketu():
    ketu = get_planet(Graha.KETU)

    assert ketu.name == "Ketu"


def test_all_planets_returns_all_objects():
    planets = list(all_planets())

    assert len(planets) == 9

    for planet in planets:
        assert isinstance(planet, PlanetFacts)


def test_planet_names_are_unique():
    names = [planet.name for planet in PLANETS.values()]

    assert len(names) == len(set(names))


def test_sun_is_malefic():
    assert get_planet(Graha.SUN).is_malefic


def test_jupiter_is_benefic():
    assert get_planet(Graha.JUPITER).is_benefic


def test_venus_is_benefic():
    assert get_planet(Graha.VENUS).is_benefic


def test_saturn_is_malefic():
    assert get_planet(Graha.SATURN).is_malefic


def test_rahu_is_malefic():
    assert get_planet(Graha.RAHU).is_malefic


def test_ketu_is_malefic():
    assert get_planet(Graha.KETU).is_malefic


def test_dictionary_contains_all_grahas():
    assert set(PLANETS.keys()) == set(Graha)