"""
tests/test_neecha_bhanga.py

Tests for structural Neecha Bhanga Raja Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult

from yogas.neecha_bhanga import (
    NEECHA_BHANGA_NAME,
    KENDRA_HOUSES,
    DEBILITATION_SIGNS,
    EXALTATION_SIGNS,
    DUSTHANA_HOUSES,
    SIGN_LORDS,
    sign_lord,
    is_debilitated,
    debilitated_planets,
    relative_house,
    is_kendra_from,
    debilitation_sign_lord,
    exaltation_sign_lord,
    debilitation_lord_in_kendra_from_lagna,
    exaltation_lord_in_kendra_from_lagna,
    debilitation_lord_in_kendra_from_moon,
    exaltation_lord_in_kendra_from_moon,
    debilitated_planet_in_kendra_from_lagna,
    debilitated_planet_in_kendra_from_moon,
    find_neecha_bhanga_conditions,
    detect_neecha_bhanga,
    NeechaBhangaRajaYogaRule,
)


# ============================================================
# TEST HELPERS
# ============================================================

def make_context(
    planet_data,
):
    """
    Build a minimal chart context.

    planet_data:
        {
            "Sun": {
                "house": 4,
                "sign": 7,
            },
            ...
        }

    Houses are derived from the supplied sign lords.
    """

    planets = {}

    for name, data in planet_data.items():
        planets[name] = SimpleNamespace(
            name=name,
            house=data.get("house"),
            sign=data.get("sign"),
        )

    houses = {}

    for house_number, lord in (
        (1, "Mars"),
        (2, "Venus"),
        (3, "Mercury"),
        (4, "Moon"),
        (5, "Sun"),
        (6, "Mercury"),
        (7, "Venus"),
        (8, "Mars"),
        (9, "Jupiter"),
        (10, "Saturn"),
        (11, "Saturn"),
        (12, "Jupiter"),
    ):
        houses[house_number] = SimpleNamespace(
            number=house_number,
            lord=lord,
        )

    return SimpleNamespace(
        planets=planets,
        houses=houses,
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_kendra_houses():
    assert KENDRA_HOUSES == (
        1,
        4,
        7,
        10,
    )


def test_dusthana_houses():
    assert DUSTHANA_HOUSES == (
        6,
        8,
        12,
    )


def test_debilitation_signs():
    assert DEBILITATION_SIGNS["Sun"] == 7
    assert DEBILITATION_SIGNS["Moon"] == 8
    assert DEBILITATION_SIGNS["Mars"] == 4
    assert DEBILITATION_SIGNS["Mercury"] == 12
    assert DEBILITATION_SIGNS["Jupiter"] == 10
    assert DEBILITATION_SIGNS["Venus"] == 6
    assert DEBILITATION_SIGNS["Saturn"] == 1


def test_exaltation_signs():
    assert EXALTATION_SIGNS["Sun"] == 1
    assert EXALTATION_SIGNS["Moon"] == 2
    assert EXALTATION_SIGNS["Mars"] == 10
    assert EXALTATION_SIGNS["Mercury"] == 6
    assert EXALTATION_SIGNS["Jupiter"] == 4
    assert EXALTATION_SIGNS["Venus"] == 12
    assert EXALTATION_SIGNS["Saturn"] == 7


# ============================================================
# SIGN LORDS
# ============================================================

@pytest.mark.parametrize(
    "sign,lord",
    [
        (1, "Mars"),
        (2, "Venus"),
        (3, "Mercury"),
        (4, "Moon"),
        (5, "Sun"),
        (6, "Mercury"),
        (7, "Venus"),
        (8, "Mars"),
        (9, "Jupiter"),
        (10, "Saturn"),
        (11, "Saturn"),
        (12, "Jupiter"),
    ],
)
def test_sign_lord(
    sign,
    lord,
):
    assert sign_lord(
        sign
    ) == lord


# ============================================================
# RELATIVE HOUSE
# ============================================================

@pytest.mark.parametrize(
    "reference,target,expected",
    [
        (1, 1, 1),
        (1, 4, 4),
        (1, 7, 7),
        (1, 10, 10),
        (5, 5, 1),
        (5, 8, 4),
        (5, 11, 7),
        (5, 2, 10),
    ],
)
def test_relative_house(
    reference,
    target,
    expected,
):
    assert relative_house(
        reference,
        target,
    ) == expected


@pytest.mark.parametrize(
    "reference,target",
    [
        (1, 1),
        (1, 4),
        (1, 7),
        (1, 10),
    ],
)
def test_kendra_from(
    reference,
    target,
):
    assert is_kendra_from(
        reference,
        target,
    )


# ============================================================
# DEBILITATION
# ============================================================

def test_sun_debilitated_in_libra():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
        }
    )

    assert is_debilitated(
        context,
        "Sun",
    )


def test_sun_not_debilitated_in_aries():
    context = make_context(
        {
            "Sun": {
                "house": 1,
                "sign": 1,
            },
        }
    )

    assert not is_debilitated(
        context,
        "Sun",
    )


def test_debilitated_planets():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Moon": {
                "house": 8,
                "sign": 8,
            },
            "Mars": {
                "house": 4,
                "sign": 4,
            },
        }
    )

    planets = debilitated_planets(
        context
    )

    assert "Sun" in planets
    assert "Moon" in planets
    assert "Mars" in planets


# ============================================================
# DEBILITATION / EXALTATION LORDS
# ============================================================

@pytest.mark.parametrize(
    "planet,expected",
    [
        ("Sun", "Venus"),
        ("Moon", "Mars"),
        ("Mars", "Moon"),
        ("Mercury", "Jupiter"),
        ("Jupiter", "Saturn"),
        ("Venus", "Mercury"),
        ("Saturn", "Mars"),
    ],
)
def test_debilitation_sign_lord(
    planet,
    expected,
):
    assert debilitation_sign_lord(
        planet
    ) == expected


@pytest.mark.parametrize(
    "planet,expected",
    [
        ("Sun", "Mars"),
        ("Moon", "Venus"),
        ("Mars", "Saturn"),
        ("Mercury", "Mercury"),
        ("Jupiter", "Moon"),
        ("Venus", "Jupiter"),
        ("Saturn", "Venus"),
    ],
)
def test_exaltation_sign_lord(
    planet,
    expected,
):
    assert exaltation_sign_lord(
        planet
    ) == expected


# ============================================================
# CANCELLATION CONDITIONS
# ============================================================

def test_debilitation_lord_in_kendra_from_lagna():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 4,
                "sign": 2,
            },
        }
    )

    assert debilitation_lord_in_kendra_from_lagna(
        context,
        "Sun",
    )


def test_debilitation_lord_not_in_kendra_from_lagna():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 3,
                "sign": 2,
            },
        }
    )

    assert not debilitation_lord_in_kendra_from_lagna(
        context,
        "Sun",
    )


def test_exaltation_lord_in_kendra_from_lagna():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Mars": {
                "house": 10,
                "sign": 1,
            },
        }
    )

    assert exaltation_lord_in_kendra_from_lagna(
        context,
        "Sun",
    )


def test_debilitation_lord_in_kendra_from_moon():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Moon": {
                "house": 2,
                "sign": 4,
            },
            "Venus": {
                "house": 5,
                "sign": 2,
            },
        }
    )

    assert debilitation_lord_in_kendra_from_moon(
        context,
        "Sun",
    )


def test_exaltation_lord_in_kendra_from_moon():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Moon": {
                "house": 2,
                "sign": 4,
            },
            "Mars": {
                "house": 5,
                "sign": 1,
            },
        }
    )

    assert exaltation_lord_in_kendra_from_moon(
        context,
        "Sun",
    )


# ============================================================
# DETECTION
# ============================================================

def test_detect_neecha_bhanga_from_debilitation_lord():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 4,
                "sign": 2,
            },
        }
    )

    result = detect_neecha_bhanga(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == NEECHA_BHANGA_NAME
    assert result.evidence
    assert result.conditions_met


def test_detect_neecha_bhanga_from_exaltation_lord():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Mars": {
                "house": 10,
                "sign": 1,
            },
        }
    )

    result = detect_neecha_bhanga(
        context
    )

    assert result.detected is True
    assert result.name == NEECHA_BHANGA_NAME


def test_detect_neecha_bhanga_from_debilitated_planet_kendra():
    context = make_context(
        {
            "Sun": {
                "house": 4,
                "sign": 7,
            },
        }
    )

    result = detect_neecha_bhanga(
        context
    )

    assert result.detected is True


def test_no_neecha_bhanga_when_not_debilitated():
    context = make_context(
        {
            "Sun": {
                "house": 4,
                "sign": 1,
            },
            "Venus": {
                "house": 3,
                "sign": 2,
            },
        }
    )

    result = detect_neecha_bhanga(
        context
    )

    assert result.detected is False


def test_no_neecha_bhanga_without_cancellation():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 3,
                "sign": 2,
            },
            "Mars": {
                "house": 2,
                "sign": 1,
            },
        }
    )

    result = detect_neecha_bhanga(
        context
    )

    assert result.detected is False


# ============================================================
# FINDINGS
# ============================================================

def test_find_conditions_returns_evidence():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 4,
                "sign": 2,
            },
        }
    )

    findings = find_neecha_bhanga_conditions(
        context
    )

    assert findings

    assert any(
        finding["planet"] == "Sun"
        for finding in findings
    )


# ============================================================
# RULE ADAPTER
# ============================================================

def test_rule_adapter():
    context = make_context(
        {
            "Sun": {
                "house": 7,
                "sign": 7,
            },
            "Venus": {
                "house": 4,
                "sign": 2,
            },
        }
    )

    rule = NeechaBhangaRajaYogaRule()

    result = rule.evaluate(
        context
    )

    assert result.detected is True
    assert result.name == NEECHA_BHANGA_NAME