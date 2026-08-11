"""
Tests for astrology.planet.

Tests:
    - Single Planet construction
    - Rashi mapping
    - Nakshatra mapping
    - Pada mapping
    - Nakshatra lord mapping
    - Astronomical value preservation
    - Retrograde preservation
    - House isolation
    - Bulk Planet construction
    - Invalid input handling

Compatible with Python 3.9+.
"""

import pytest

from astrology.planet import (
    build_planet,
    build_planets,
)
from models.ephemeris_position import EphemerisPosition
from models.graha import Graha
from models.planet import Planet


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def sun_position():
    """
    Known sidereal Sun position used by the existing
    Kundali Engine test data.
    """

    return EphemerisPosition(
        longitude=256.27,
        latitude=0.0,
        distance=1.0,
        longitude_speed=0.98,
        latitude_speed=0.0,
        distance_speed=0.0,
        retrograde=False,
    )


@pytest.fixture
def retrograde_position():
    """
    Sample retrograde planetary position.
    """

    return EphemerisPosition(
        longitude=304.11,
        latitude=0.5,
        distance=1.5,
        longitude_speed=-0.25,
        latitude_speed=-0.01,
        distance_speed=0.001,
        retrograde=True,
    )


# ============================================================
# SINGLE PLANET CONSTRUCTION
# ============================================================


def test_build_planet_returns_planet(sun_position):
    """build_planet() must return a Planet object."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert isinstance(planet, Planet)


def test_build_planet_sets_graha_name(sun_position):
    """Graha display name must become the Planet name."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.name == "Sun"


def test_build_planet_preserves_longitude(sun_position):
    """Planet longitude must equal the ephemeris longitude."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.longitude == pytest.approx(256.27)


def test_build_planet_preserves_latitude(sun_position):
    """Planet latitude must be preserved."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.latitude == pytest.approx(0.0)


def test_build_planet_preserves_distance(sun_position):
    """Planet distance must be preserved."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.distance == pytest.approx(1.0)


def test_build_planet_uses_longitude_speed(sun_position):
    """
    Planet.speed must contain the longitudinal speed returned
    by Swiss Ephemeris.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.speed == pytest.approx(0.98)


def test_build_planet_preserves_retrograde_status(sun_position):
    """Retrograde status must be preserved."""

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.retrograde is False


# ============================================================
# RASHI / ZODIAC
# ============================================================


def test_build_planet_calculates_sign(sun_position):
    """
    256.27° belongs to Sagittarius.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.sign == "Sagittarius"


def test_build_planet_calculates_sign_number(sun_position):
    """
    Sagittarius is the ninth Rashi.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.sign_number == 9


def test_build_planet_calculates_degree_in_sign(sun_position):
    """
    256.27° absolute longitude corresponds to 16.27°
    within Sagittarius.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.sign_degree == pytest.approx(16.27)


# ============================================================
# NAKSHATRA
# ============================================================


def test_build_planet_calculates_nakshatra(sun_position):
    """
    256.27° lies in Purva Ashadha.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.nakshatra == "Purva Ashadha"


def test_build_planet_calculates_pada(sun_position):
    """
    256.27° lies in Purva Ashadha Pada 1.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.pada == 1


def test_build_planet_calculates_nakshatra_lord(sun_position):
    """
    Purva Ashadha is ruled by Venus.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.nakshatra_lord == "Venus"


# ============================================================
# HOUSE ISOLATION
# ============================================================


def test_build_planet_does_not_calculate_house(sun_position):
    """
    House placement belongs to chart/house assembly and must
    remain at the Planet model default at this layer.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.house == 0


# ============================================================
# FUTURE ASTROLOGICAL CLASSIFICATIONS
# ============================================================


def test_build_planet_does_not_apply_dignity_logic(sun_position):
    """
    Dignity is intentionally outside the responsibility of
    astrology.planet.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.dignity == ""
    assert planet.exalted is False
    assert planet.debilitated is False
    assert planet.own_sign is False
    assert planet.moolatrikona is False


def test_build_planet_does_not_apply_combustion_logic(
    sun_position,
):
    """
    Combustion is intentionally outside the responsibility
    of astrology.planet.
    """

    planet = build_planet(
        Graha.SUN,
        sun_position,
    )

    assert planet.combustion is False


# ============================================================
# RETROGRADE PLANET
# ============================================================


def test_build_planet_preserves_retrograde_planet(
    retrograde_position,
):
    """A retrograde astronomical position must remain retrograde."""

    planet = build_planet(
        Graha.MARS,
        retrograde_position,
    )

    assert planet.name == "Mars"
    assert planet.longitude == pytest.approx(304.11)
    assert planet.speed == pytest.approx(-0.25)
    assert planet.retrograde is True


# ============================================================
# ALL GRAHAS
# ============================================================


def test_build_planets_returns_dictionary(
    sun_position,
):
    """build_planets() must return a dictionary."""

    positions = {
        Graha.SUN: sun_position,
    }

    planets = build_planets(positions)

    assert isinstance(planets, dict)


def test_build_planets_preserves_graha_keys(
    sun_position,
):
    """The Graha keys must be preserved."""

    positions = {
        Graha.SUN: sun_position,
    }

    planets = build_planets(positions)

    assert set(planets.keys()) == {
        Graha.SUN
    }


def test_build_planets_returns_planet_values(
    sun_position,
):
    """Every result value must be a Planet."""

    positions = {
        Graha.SUN: sun_position,
    }

    planets = build_planets(positions)

    assert all(
        isinstance(
            planet,
            Planet,
        )
        for planet in planets.values()
    )


def test_build_planets_handles_all_nine_grahas(
    sun_position,
):
    """
    build_planets() must be capable of converting all nine
    Grahas when supplied with valid positions.
    """

    positions = {
        graha: sun_position
        for graha in Graha
    }

    planets = build_planets(positions)

    assert len(planets) == 9
    assert set(planets.keys()) == set(Graha)

    for planet in planets.values():
        assert isinstance(planet, Planet)


# ============================================================
# INPUT VALIDATION
# ============================================================


def test_build_planets_rejects_invalid_position():
    """
    Every position supplied to build_planets() must be an
    EphemerisPosition.
    """

    positions = {
        Graha.SUN: "invalid",
    }

    with pytest.raises(TypeError):
        build_planets(positions)


def test_build_planets_rejects_none_position():
    """None is not a valid astronomical position."""

    positions = {
        Graha.SUN: None,
    }

    with pytest.raises(TypeError):
        build_planets(positions)


# ============================================================
# MULTIPLE PLANETS
# ============================================================


def test_build_planets_preserves_each_planets_data():
    """
    Each Graha must retain its own astronomical data when
    multiple positions are supplied.
    """

    sun = EphemerisPosition(
        longitude=256.27,
        latitude=0.0,
        distance=1.0,
        longitude_speed=0.98,
        latitude_speed=0.0,
        distance_speed=0.0,
        retrograde=False,
    )

    moon = EphemerisPosition(
        longitude=199.47,
        latitude=0.2,
        distance=0.99,
        longitude_speed=13.2,
        latitude_speed=0.1,
        distance_speed=0.001,
        retrograde=False,
    )

    positions = {
        Graha.SUN: sun,
        Graha.MOON: moon,
    }

    planets = build_planets(positions)

    assert planets[Graha.SUN].name == "Sun"
    assert planets[Graha.MOON].name == "Moon"

    assert planets[Graha.SUN].longitude == pytest.approx(
        256.27
    )

    assert planets[Graha.MOON].longitude == pytest.approx(
        199.47
    )

    assert planets[Graha.SUN].speed == pytest.approx(
        0.98
    )

    assert planets[Graha.MOON].speed == pytest.approx(
        13.2
    )