from datetime import datetime

import pytest

from interpretation.context import (
    PlanetContext,
    DashaContext,
    InterpretationContext,
    build_interpretation_context,
    get_planet,
    get_planets_in_house,
    get_planets_in_sign,
)


class DummyLocation:
    name = "Kathmandu"
    latitude = 27.7172
    longitude = 85.3240
    timezone = "Asia/Kathmandu"


class DummyBirth:
    name = "Test Native"
    birth_datetime = datetime(2000, 1, 1, 12, 0, 0)
    location = DummyLocation()


class DummyPlanet:
    def __init__(
        self,
        name,
        sign,
        sign_degree,
        house,
        nakshatra,
        pada,
        longitude,
        retrograde=False,
        dignity=None,
    ):
        self.name = name
        self.sign = sign
        self.sign_degree = sign_degree
        self.house = house
        self.nakshatra = nakshatra
        self.pada = pada
        self.longitude = longitude
        self.retrograde = retrograde
        self.dignity = dignity


class DummyDasha:
    planet = "Jupiter"


class DummyAntardasha:
    antardasha_lord = "Saturn"


class DummyPratyantardasha:
    pratyantardasha_lord = "Mercury"


class DummySookshma:
    sookshma_lord = "Venus"


class DummyPrana:
    prana_lord = "Mars"


class DummyDeha:
    deha_lord = "Moon"


class DummyChart:
    ascendant = 256.515697

    planets = {
        "Sun": DummyPlanet(
            "Sun",
            "Sagittarius",
            16.27,
            1,
            "Purva Ashadha",
            1,
            256.515697,
        ),
        "Moon": DummyPlanet(
            "Moon",
            "Libra",
            16.59,
            11,
            "Swati",
            3,
            199.470553,
        ),
        "Mars": DummyPlanet(
            "Mars",
            "Aquarius",
            3.92,
            3,
            "Dhanishta",
            4,
            304.110091,
        ),
    }

    houses = {}

    current_mahadasha = DummyDasha()
    current_antardasha = DummyAntardasha()
    current_pratyantardasha = DummyPratyantardasha()
    current_sookshmadasha = DummySookshma()
    current_pranadasha = DummyPrana()
    current_dehadasha = DummyDeha()


def test_planet_context_defaults():
    planet = PlanetContext(
        name="Sun",
        sign="Aries",
        sign_degree=10.0,
        house=1,
        nakshatra="Ashwini",
        pada=1,
    )

    assert planet.name == "Sun"
    assert planet.sign == "Aries"
    assert planet.house == 1
    assert planet.longitude is None
    assert planet.retrograde is None
    assert planet.dignity is None


def test_dasha_context():
    dasha = DashaContext(
        mahadasha="Jupiter",
        antardasha="Saturn",
        pratyantardasha="Mercury",
        sookshma="Venus",
        prana="Mars",
        deha="Moon",
    )

    assert dasha.mahadasha == "Jupiter"
    assert dasha.antardasha == "Saturn"
    assert dasha.pratyantardasha == "Mercury"
    assert dasha.sookshma == "Venus"
    assert dasha.prana == "Mars"
    assert dasha.deha == "Moon"


def test_build_interpretation_context():
    chart = DummyChart()
    birth = DummyBirth()

    context = build_interpretation_context(
        chart,
        birth,
    )

    assert isinstance(
        context,
        InterpretationContext,
    )

    assert context.name == "Test Native"
    assert context.place == "Kathmandu"
    assert context.timezone == "Asia/Kathmandu"

    assert context.ascendant_sign == "Sagittarius"

    assert context.ascendant_degree == pytest.approx(
        16.515697,
        abs=1e-9,
    )

    assert "Sun" in context.planets
    assert "Moon" in context.planets
    assert "Mars" in context.planets

    assert context.planets["Sun"].sign == "Sagittarius"
    assert context.planets["Sun"].house == 1

    assert context.dasha.mahadasha == "Jupiter"
    assert context.dasha.antardasha == "Saturn"
    assert context.dasha.pratyantardasha == "Mercury"
    assert context.dasha.sookshma == "Venus"
    assert context.dasha.prana == "Mars"
    assert context.dasha.deha == "Moon"


def test_get_planet():
    context = build_interpretation_context(
        DummyChart(),
        DummyBirth(),
    )

    sun = get_planet(
        context,
        "Sun",
    )

    assert sun.name == "Sun"
    assert sun.sign == "Sagittarius"


def test_get_planet_missing():
    context = build_interpretation_context(
        DummyChart(),
        DummyBirth(),
    )

    try:
        get_planet(
            context,
            "Venus",
        )
        assert False
    except KeyError as exc:
        assert "Venus" in str(exc)


def test_get_planets_in_house():
    context = build_interpretation_context(
        DummyChart(),
        DummyBirth(),
    )

    planets = get_planets_in_house(
        context,
        1,
    )

    assert len(planets) == 1
    assert planets[0].name == "Sun"


def test_get_planets_in_sign():
    context = build_interpretation_context(
        DummyChart(),
        DummyBirth(),
    )

    planets = get_planets_in_sign(
        context,
        "sagittarius",
    )

    assert len(planets) == 1
    assert planets[0].name == "Sun"


def test_invalid_house_number():
    context = build_interpretation_context(
        DummyChart(),
        DummyBirth(),
    )

    try:
        get_planets_in_house(
            context,
            13,
        )
        assert False
    except ValueError as exc:
        assert "between 1 and 12" in str(exc)
