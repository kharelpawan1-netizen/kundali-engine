"""
tests/test_knowledge_planet.py

Unit tests for the immutable PlanetFacts model.

Python Version:
    3.9+
"""

from dataclasses import FrozenInstanceError

import pytest

from knowledge.planet import PlanetFacts


@pytest.fixture
def planet() -> PlanetFacts:
    """
    Sample PlanetFacts instance.
    """

    return PlanetFacts(
        name="Sun",
        sanskrit_name="Surya",
        is_benefic=False,
        gender="Male",
        element="Fire",
        guna="Sattva",
        caste="Kshatriya",
        temperament="Cruel",
        dosha="Pitta",
        direction="East",
        color="Red",
        metal="Copper",
        gemstone="Ruby",
        deity="Surya",
        weekday="Sunday",
        own_signs=("Leo",),
        exaltation_sign="Aries",
        exaltation_degree=10.0,
        debilitation_sign="Libra",
        debilitation_degree=10.0,
        moolatrikona_sign="Leo",
        friends=("Moon", "Mars", "Jupiter"),
        enemies=("Venus", "Saturn"),
        neutrals=("Mercury",),
        karakatwas=("Soul", "Father", "Authority"),
        natural_houses=(1, 9, 10),
        body_parts=("Heart", "Bones"),
        diseases=("Heart Disease",),
        professions=("Government", "Politics"),
        keywords=("authority", "leadership"),
    )


def test_name(planet):
    assert planet.name == "Sun"


def test_sanskrit_name(planet):
    assert planet.sanskrit_name == "Surya"


def test_is_benefic(planet):
    assert planet.is_benefic is False


def test_is_malefic(planet):
    assert planet.is_malefic is True


def test_gender(planet):
    assert planet.gender == "Male"


def test_element(planet):
    assert planet.element == "Fire"


def test_guna(planet):
    assert planet.guna == "Sattva"


def test_caste(planet):
    assert planet.caste == "Kshatriya"


def test_temperament(planet):
    assert planet.temperament == "Cruel"


def test_dosha(planet):
    assert planet.dosha == "Pitta"


def test_direction(planet):
    assert planet.direction == "East"


def test_color(planet):
    assert planet.color == "Red"


def test_metal(planet):
    assert planet.metal == "Copper"


def test_gemstone(planet):
    assert planet.gemstone == "Ruby"


def test_deity(planet):
    assert planet.deity == "Surya"


def test_weekday(planet):
    assert planet.weekday == "Sunday"


def test_own_signs(planet):
    assert planet.own_signs == ("Leo",)


def test_exaltation(planet):
    assert planet.exaltation_sign == "Aries"
    assert planet.exaltation_degree == 10.0


def test_debilitation(planet):
    assert planet.debilitation_sign == "Libra"
    assert planet.debilitation_degree == 10.0


def test_moolatrikona(planet):
    assert planet.moolatrikona_sign == "Leo"


def test_friendships(planet):
    assert "Moon" in planet.friends
    assert "Venus" in planet.enemies
    assert "Mercury" in planet.neutrals


def test_karakatwas(planet):
    assert "Soul" in planet.karakatwas


def test_natural_houses(planet):
    assert planet.natural_houses == (1, 9, 10)


def test_body_parts(planet):
    assert "Heart" in planet.body_parts


def test_diseases(planet):
    assert "Heart Disease" in planet.diseases


def test_professions(planet):
    assert "Government" in planet.professions


def test_keywords(planet):
    assert "authority" in planet.keywords


def test_string_representation(planet):
    assert str(planet) == "Sun"


def test_frozen_dataclass(planet):
    with pytest.raises(FrozenInstanceError):
        planet.name = "Moon"


def test_equality():
    p1 = PlanetFacts(
        name="Sun",
        sanskrit_name="Surya",
        is_benefic=False,
        gender="Male",
        element="Fire",
        guna="Sattva",
        caste="Kshatriya",
        temperament="Cruel",
        dosha="Pitta",
        direction="East",
        color="Red",
        metal="Copper",
        gemstone="Ruby",
        deity="Surya",
        weekday="Sunday",
        own_signs=("Leo",),
        exaltation_sign="Aries",
        exaltation_degree=10.0,
        debilitation_sign="Libra",
        debilitation_degree=10.0,
        moolatrikona_sign="Leo",
        friends=("Moon",),
        enemies=("Venus",),
        neutrals=("Mercury",),
        karakatwas=("Soul",),
        natural_houses=(1,),
        body_parts=("Heart",),
        diseases=("Heart Disease",),
        professions=("Government",),
        keywords=("authority",),
    )

    p2 = PlanetFacts(
        name="Sun",
        sanskrit_name="Surya",
        is_benefic=False,
        gender="Male",
        element="Fire",
        guna="Sattva",
        caste="Kshatriya",
        temperament="Cruel",
        dosha="Pitta",
        direction="East",
        color="Red",
        metal="Copper",
        gemstone="Ruby",
        deity="Surya",
        weekday="Sunday",
        own_signs=("Leo",),
        exaltation_sign="Aries",
        exaltation_degree=10.0,
        debilitation_sign="Libra",
        debilitation_degree=10.0,
        moolatrikona_sign="Leo",
        friends=("Moon",),
        enemies=("Venus",),
        neutrals=("Mercury",),
        karakatwas=("Soul",),
        natural_houses=(1,),
        body_parts=("Heart",),
        diseases=("Heart Disease",),
        professions=("Government",),
        keywords=("authority",),
    )

    assert p1 == p2


def test_hashable(planet):
    planets = {planet}
    assert planet in planets