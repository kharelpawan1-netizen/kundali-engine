"""
tests/test_aspects.py

Tests for classical Parashari planetary aspects (Drishti).

Compatible with Python 3.9.
"""

import pytest

from astrology.aspects import (
    Aspect,
    aspect_distances,
    aspect_target_signs,
    build_aspect_map,
    get_aspects,
    has_aspect,
    jupiter_aspects_5th,
    jupiter_aspects_9th,
    mars_aspects_4th,
    mars_aspects_8th,
    planet_aspects_house,
    planet_aspects_planet,
    saturn_aspects_3rd,
    saturn_aspects_10th,
    sign_distance,
)


# ============================================================
# sign_distance()
# ============================================================


def test_sign_distance_same_sign():
    assert sign_distance(1, 1) == 1


def test_sign_distance_seventh():
    # Aries -> Libra
    assert sign_distance(1, 7) == 7


def test_sign_distance_wraparound():
    # Pisces -> Aries
    assert sign_distance(12, 1) == 2


def test_sign_distance_reverse_wraparound():
    # Aries -> Pisces
    assert sign_distance(1, 12) == 12


def test_sign_distance_invalid_source():
    with pytest.raises(ValueError):
        sign_distance(0, 1)


def test_sign_distance_invalid_target():
    with pytest.raises(ValueError):
        sign_distance(1, 13)


# ============================================================
# aspect_distances()
# ============================================================


def test_sun_has_seventh_aspect():
    assert aspect_distances("Sun") == (7,)


def test_moon_has_seventh_aspect():
    assert aspect_distances("Moon") == (7,)


def test_mercury_has_seventh_aspect():
    assert aspect_distances("Mercury") == (7,)


def test_venus_has_seventh_aspect():
    assert aspect_distances("Venus") == (7,)


def test_mars_special_aspects():
    assert aspect_distances("Mars") == (4, 7, 8)


def test_jupiter_special_aspects():
    assert aspect_distances("Jupiter") == (5, 7, 9)


def test_saturn_special_aspects():
    assert aspect_distances("Saturn") == (3, 7, 10)


def test_rahu_default_aspect():
    assert aspect_distances("Rahu") == (7,)


def test_ketu_default_aspect():
    assert aspect_distances("Ketu") == (7,)


def test_nodes_can_be_disabled():
    assert aspect_distances("Rahu", include_nodes=False) == ()
    assert aspect_distances("Ketu", include_nodes=False) == ()


def test_unknown_planet_rejected():
    with pytest.raises(ValueError):
        aspect_distances("Earth")


# ============================================================
# Custom node aspects
# ============================================================


def test_custom_rahu_aspects():
    custom = {
        "Rahu": (5, 7, 9),
        "Ketu": (5, 7, 9),
    }

    assert aspect_distances(
        "Rahu",
        node_aspects=custom,
    ) == (5, 7, 9)


def test_custom_ketu_aspects():
    custom = {
        "Rahu": (5, 7, 9),
        "Ketu": (5, 7, 9),
    }

    assert aspect_distances(
        "Ketu",
        node_aspects=custom,
    ) == (5, 7, 9)


# ============================================================
# has_aspect()
# ============================================================


def test_sun_aspects_seventh_sign():
    # Sun in Aries -> Libra
    assert has_aspect(
        "Sun",
        1,
        7,
    )


def test_sun_does_not_aspect_fifth_sign():
    # Sun in Aries -> Leo
    assert not has_aspect(
        "Sun",
        1,
        5,
    )


def test_mars_aspects_fourth_sign():
    # Mars in Aries -> Cancer
    assert has_aspect(
        "Mars",
        1,
        4,
    )


def test_mars_aspects_seventh_sign():
    # Mars in Aries -> Libra
    assert has_aspect(
        "Mars",
        1,
        7,
    )


def test_mars_aspects_eighth_sign():
    # Mars in Aries -> Scorpio
    assert has_aspect(
        "Mars",
        1,
        8,
    )


def test_jupiter_aspects_fifth_sign():
    # Jupiter in Aries -> Leo
    assert has_aspect(
        "Jupiter",
        1,
        5,
    )


def test_jupiter_aspects_seventh_sign():
    # Jupiter in Aries -> Libra
    assert has_aspect(
        "Jupiter",
        1,
        7,
    )


def test_jupiter_aspects_ninth_sign():
    # Jupiter in Aries -> Sagittarius
    assert has_aspect(
        "Jupiter",
        1,
        9,
    )


def test_saturn_aspects_third_sign():
    # Saturn in Aries -> Gemini
    assert has_aspect(
        "Saturn",
        1,
        3,
    )


def test_saturn_aspects_seventh_sign():
    # Saturn in Aries -> Libra
    assert has_aspect(
        "Saturn",
        1,
        7,
    )


def test_saturn_aspects_tenth_sign():
    # Saturn in Aries -> Capricorn
    assert has_aspect(
        "Saturn",
        1,
        10,
    )


# ============================================================
# get_aspects()
# ============================================================


def test_mars_aspects_from_aries():
    aspects = get_aspects(
        "Mars",
        1,
    )

    assert len(aspects) == 3

    assert aspects[0] == Aspect(
        planet="Mars",
        target_sign=4,
        distance=4,
        special=True,
    )

    assert aspects[1] == Aspect(
        planet="Mars",
        target_sign=7,
        distance=7,
        special=False,
    )

    assert aspects[2] == Aspect(
        planet="Mars",
        target_sign=8,
        distance=8,
        special=True,
    )


def test_jupiter_aspects_from_aries():
    aspects = get_aspects(
        "Jupiter",
        1,
    )

    assert [a.target_sign for a in aspects] == [
        5,
        7,
        9,
    ]


def test_saturn_aspects_from_aries():
    aspects = get_aspects(
        "Saturn",
        1,
    )

    assert [a.target_sign for a in aspects] == [
        3,
        7,
        10,
    ]


# ============================================================
# aspect_target_signs()
# ============================================================


def test_mars_target_signs():
    assert aspect_target_signs(
        "Mars",
        1,
    ) == [4, 7, 8]


def test_jupiter_target_signs():
    assert aspect_target_signs(
        "Jupiter",
        1,
    ) == [5, 7, 9]


def test_saturn_target_signs():
    assert aspect_target_signs(
        "Saturn",
        1,
    ) == [3, 7, 10]


# ============================================================
# Complete aspect map
# ============================================================


def test_build_aspect_map():
    planet_signs = {
        "Sun": 10,
        "Moon": 8,
        "Mars": 12,
        "Jupiter": 1,
        "Saturn": 1,
    }

    aspect_map = build_aspect_map(
        planet_signs,
    )

    assert set(aspect_map.keys()) == set(
        planet_signs.keys()
    )

    assert len(aspect_map["Sun"]) == 1
    assert len(aspect_map["Moon"]) == 1
    assert len(aspect_map["Mars"]) == 3
    assert len(aspect_map["Jupiter"]) == 3
    assert len(aspect_map["Saturn"]) == 3


def test_build_aspect_map_with_nodes():
    planet_signs = {
        "Rahu": 5,
        "Ketu": 11,
    }

    aspect_map = build_aspect_map(
        planet_signs,
    )

    assert len(aspect_map["Rahu"]) == 1
    assert len(aspect_map["Ketu"]) == 1


# ============================================================
# Planet-to-planet aspects
# ============================================================


def test_planet_aspects_planet_true():
    # Mars in Aries aspects Saturn in Libra.
    assert planet_aspects_planet(
        "Mars",
        1,
        "Saturn",
        7,
    )


def test_planet_aspects_planet_false():
    # Mars in Aries does not aspect Mercury in Leo.
    assert not planet_aspects_planet(
        "Mars",
        1,
        "Mercury",
        5,
    )


def test_jupiter_aspects_saturn():
    # Jupiter in Aries -> Libra via 7th.
    assert planet_aspects_planet(
        "Jupiter",
        1,
        "Saturn",
        7,
    )


# ============================================================
# Planet-to-house aspects
# ============================================================


def test_planet_aspects_house_true():
    assert planet_aspects_house(
        "Jupiter",
        1,
        5,
    )


def test_planet_aspects_house_false():
    assert not planet_aspects_house(
        "Jupiter",
        1,
        6,
    )


# ============================================================
# Special aspect helpers
# ============================================================


def test_mars_4th_helper():
    assert mars_aspects_4th(1) == 4


def test_mars_8th_helper():
    assert mars_aspects_8th(1) == 8


def test_jupiter_5th_helper():
    assert jupiter_aspects_5th(1) == 5


def test_jupiter_9th_helper():
    assert jupiter_aspects_9th(1) == 9


def test_saturn_3rd_helper():
    assert saturn_aspects_3rd(1) == 3


def test_saturn_10th_helper():
    assert saturn_aspects_10th(1) == 10