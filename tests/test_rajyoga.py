
"""
tests/test_rajyoga.py

Tests for structural Raja Yoga detection.

Covered:
    - Kendra classification
    - Trikona classification
    - House lords
    - Conjunction
    - Mutual Parashari aspect
    - Parivartana / sign exchange
    - Kendra-Trikona association
    - YogaResult contract
    - RajaYogaRule adapter
"""

from types import SimpleNamespace

import pytest

from yogas.rajyoga import (
    KENDRA_HOUSES,
    TRIKONA_HOUSES,
    RajaYogaRule,
    detect_rajyoga,
    find_kendra_trikona_associations,
    house_lord,
    is_kendra_house,
    is_trikona_house,
    planets_conjunct,
    planets_mutually_aspect,
    planets_exchange_signs,
    sign_lord,
)


# ============================================================
# TEST HELPERS
# ============================================================

def make_context(
    house_lords,
    planet_houses,
    planet_signs=None,
):
    """
    Build a minimal test context.

    house_lords:
        {house_number: planet_name}

    planet_houses:
        {planet_name: house_number}

    planet_signs:
        {planet_name: zodiac_sign_number}
    """

    if planet_signs is None:
        planet_signs = {}

    houses = {
        house_number: SimpleNamespace(
            number=house_number,
            lord=lord,
        )
        for house_number, lord
        in house_lords.items()
    }

    planets = {
        name: SimpleNamespace(
            name=name,
            house=house,
            sign_number=planet_signs.get(
                name
            ),
        )
        for name, house
        in planet_houses.items()
    }

    return SimpleNamespace(
        houses=houses,
        planets=planets,
    )


# ============================================================
# HOUSE CLASSIFICATION
# ============================================================

def test_kendra_houses():
    assert KENDRA_HOUSES == (
        1,
        4,
        7,
        10,
    )

    for house in KENDRA_HOUSES:
        assert is_kendra_house(house)


def test_non_kendra_houses():
    for house in (
        2,
        3,
        5,
        6,
        8,
        9,
        11,
        12,
    ):
        assert not is_kendra_house(house)


def test_trikona_houses():
    assert TRIKONA_HOUSES == (
        1,
        5,
        9,
    )

    for house in TRIKONA_HOUSES:
        assert is_trikona_house(house)


def test_non_trikona_houses():
    for house in (
        2,
        3,
        4,
        6,
        7,
        8,
        10,
        11,
        12,
    ):
        assert not is_trikona_house(house)


# ============================================================
# HOUSE LORD
# ============================================================

def test_house_lord_returns_lord():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 1,
            "Jupiter": 5,
        },
    )

    assert house_lord(
        context,
        1,
    ) == "Mars"

    assert house_lord(
        context,
        5,
    ) == "Jupiter"


def test_house_lord_missing_house():
    context = make_context(
        {
            1: "Mars",
        },
        {
            "Mars": 1,
        },
    )

    assert house_lord(
        context,
        5,
    ) is None


@pytest.mark.parametrize(
    "house",
    [
        0,
        13,
        -1,
    ],
)
def test_house_lord_invalid_house(
    house,
):
    context = make_context(
        {},
        {},
    )

    with pytest.raises(
        ValueError
    ):
        house_lord(
            context,
            house,
        )


# ============================================================
# SIGN LORD
# ============================================================

def test_sign_lord():
    assert sign_lord(1) == "Mars"
    assert sign_lord(2) == "Venus"
    assert sign_lord(4) == "Moon"
    assert sign_lord(5) == "Sun"
    assert sign_lord(7) == "Venus"
    assert sign_lord(9) == "Jupiter"
    assert sign_lord(10) == "Saturn"
    assert sign_lord(12) == "Jupiter"


@pytest.mark.parametrize(
    "sign_number",
    [
        0,
        13,
        -1,
    ],
)
def test_sign_lord_invalid_sign(
    sign_number,
):
    with pytest.raises(
        ValueError
    ):
        sign_lord(
            sign_number
        )


# ============================================================
# CONJUNCTION
# ============================================================

def test_planets_conjunct():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 5,
            "Jupiter": 5,
        },
    )

    assert planets_conjunct(
        context,
        "Mars",
        "Jupiter",
    )


def test_planets_not_conjunct():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 1,
            "Jupiter": 5,
        },
    )

    assert not planets_conjunct(
        context,
        "Mars",
        "Jupiter",
    )


# ============================================================
# MUTUAL PARASHARI ASPECT
# ============================================================

def test_planets_mutually_aspect_7th():
    """
    Moon in Aries.
    Jupiter in Libra.

    Aries -> Libra = 7th.
    Libra -> Aries = 7th.

    Therefore mutual aspect exists.
    """

    context = make_context(
        {
            1: "Moon",
            5: "Jupiter",
        },
        {
            "Moon": 1,
            "Jupiter": 7,
        },
        {
            "Moon": 1,
            "Jupiter": 7,
        },
    )

    assert planets_mutually_aspect(
        context,
        "Moon",
        "Jupiter",
    ) is True


def test_planets_not_mutually_aspect():
    """
    Moon in Aries.
    Jupiter in Leo.

    Aries -> Leo = 5th.
    Leo -> Aries = 9th.

    Moon and Jupiter do not mutually aspect.
    """

    context = make_context(
        {
            1: "Moon",
            5: "Jupiter",
        },
        {
            "Moon": 1,
            "Jupiter": 5,
        },
        {
            "Moon": 1,
            "Jupiter": 5,
        },
    )

    assert planets_mutually_aspect(
        context,
        "Moon",
        "Jupiter",
    ) is False


def test_mutual_aspect_missing_sign_numbers():
    context = make_context(
        {
            1: "Moon",
            5: "Jupiter",
        },
        {
            "Moon": 1,
            "Jupiter": 7,
        },
    )

    assert planets_mutually_aspect(
        context,
        "Moon",
        "Jupiter",
    ) is False


def test_same_planet_cannot_mutually_aspect_itself():
    context = make_context(
        {
            1: "Moon",
        },
        {
            "Moon": 1,
        },
        {
            "Moon": 1,
        },
    )

    assert planets_mutually_aspect(
        context,
        "Moon",
        "Moon",
    ) is False


# ============================================================
# PARIVARTANA / SIGN EXCHANGE
# ============================================================

def test_planets_exchange_signs():
    """
    Mars owns Aries.
    Venus owns Taurus.

    Mars in Taurus.
    Venus in Aries.

    Therefore Mars and Venus exchange signs.
    """

    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
    )

    assert planets_exchange_signs(
        context,
        "Mars",
        "Venus",
    ) is True


def test_planets_do_not_exchange_signs():
    """
    Mars in Aries.
    Venus in Taurus.

    Each planet is in its own sign, so there is
    no exchange.
    """

    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 1,
            "Venus": 2,
        },
        {
            "Mars": 1,
            "Venus": 2,
        },
    )

    assert planets_exchange_signs(
        context,
        "Mars",
        "Venus",
    ) is False


def test_parivartana_requires_both_directions():
    """
    Mars in Taurus means Mars occupies Venus's sign.

    But Venus in Gemini is Mercury's sign,
    not Mars's sign.

    Therefore there is no exchange.
    """

    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 2,
            "Venus": 3,
        },
        {
            "Mars": 2,
            "Venus": 3,
        },
    )

    assert planets_exchange_signs(
        context,
        "Mars",
        "Venus",
    ) is False


def test_parivartana_missing_sign_numbers():
    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
    )

    assert planets_exchange_signs(
        context,
        "Mars",
        "Venus",
    ) is False


def test_same_planet_cannot_exchange_signs():
    context = make_context(
        {
            1: "Mars",
        },
        {
            "Mars": 2,
        },
        {
            "Mars": 2,
        },
    )

    assert planets_exchange_signs(
        context,
        "Mars",
        "Mars",
    ) is False


# ============================================================
# RAJA YOGA FORMATION
# ============================================================

def test_kendra_trikona_lords_conjunct():
    """
    Example:

        1st lord = Mars
        5th lord = Jupiter

    Mars and Jupiter occupy house 5.

    Therefore a structural Kendra-Trikona
    lord association exists.
    """

    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
            9: "Venus",
            4: "Mercury",
            7: "Saturn",
            10: "Moon",
        },
        {
            "Mars": 5,
            "Jupiter": 5,
            "Venus": 2,
            "Mercury": 8,
            "Saturn": 11,
            "Moon": 3,
        },
    )

    associations = (
        find_kendra_trikona_associations(
            context
        )
    )

    assert associations

    assert any(
        association["kendra_house"] == 1
        and association["trikona_house"] == 5
        and association["kendra_lord"] == "Mars"
        and association["trikona_lord"] == "Jupiter"
        and association["association"]
        == "conjunction"
        for association in associations
    )


def test_kendra_trikona_lords_mutually_aspect():
    """
    1st lord = Moon.
    5th lord = Jupiter.

    Moon in Aries.
    Jupiter in Libra.

    Aries and Libra are 7th from each other.
    """

    context = make_context(
        {
            1: "Moon",
            5: "Jupiter",
        },
        {
            "Moon": 1,
            "Jupiter": 7,
        },
        {
            "Moon": 1,
            "Jupiter": 7,
        },
    )

    associations = (
        find_kendra_trikona_associations(
            context
        )
    )

    assert any(
        association["kendra_house"] == 1
        and association["trikona_house"] == 5
        and association["kendra_lord"] == "Moon"
        and association["trikona_lord"] == "Jupiter"
        and association["association"]
        == "mutual_aspect"
        for association in associations
    )


def test_kendra_trikona_lords_parivartana():
    """
    1st lord = Mars.
    5th lord = Venus.

    Mars owns Aries.
    Venus owns Taurus.

    Mars in Taurus.
    Venus in Aries.

    Therefore the Kendra lord and Trikona lord
    form Parivartana.
    """

    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
    )

    associations = (
        find_kendra_trikona_associations(
            context
        )
    )

    assert any(
        association["kendra_house"] == 1
        and association["trikona_house"] == 5
        and association["kendra_lord"] == "Mars"
        and association["trikona_lord"] == "Venus"
        and association["association"]
        == "parivartana"
        for association in associations
    )


def test_no_kendra_trikona_association():
    context = make_context(
        {
            1: "Mars",
            4: "Mercury",
            7: "Saturn",
            10: "Moon",
            5: "Jupiter",
            9: "Venus",
        },
        {
            "Mars": 1,
            "Mercury": 4,
            "Saturn": 7,
            "Moon": 10,
            "Jupiter": 5,
            "Venus": 9,
        },
    )

    result = detect_rajyoga(
        context
    )

    assert result.detected is False


# ============================================================
# RESULT CONTRACT
# ============================================================

def test_detected_result_is_yoga_result():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 5,
            "Jupiter": 5,
        },
    )

    result = detect_rajyoga(
        context
    )

    assert result.detected is True
    assert result.name == "Raja Yoga"
    assert result.category == "Raja Yoga"


def test_undetected_result_is_yoga_result():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 1,
            "Jupiter": 5,
        },
    )

    result = detect_rajyoga(
        context
    )

    assert result.detected is False
    assert result.name == "Raja Yoga"


def test_detected_result_contains_evidence():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 5,
            "Jupiter": 5,
        },
    )

    result = detect_rajyoga(
        context
    )

    assert result.detected is True
    assert result.evidence
    assert result.involved_planets
    assert result.involved_houses
    assert result.conditions_met


def test_parivartana_result_contains_metadata():
    context = make_context(
        {
            1: "Mars",
            5: "Venus",
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
        {
            "Mars": 2,
            "Venus": 1,
        },
    )

    result = detect_rajyoga(
        context
    )

    assert result.detected is True

    assert (
        "parivartana"
        in result.metadata["association_types"]
    )

    assert any(
        association["association"]
        == "parivartana"
        for association
        in result.metadata["associations"]
    )

    assert any(
        "Parivartana"
        in evidence
        for evidence
        in result.evidence
    )


# ============================================================
# RULE ADAPTER
# ============================================================

def test_raja_yoga_rule():
    context = make_context(
        {
            1: "Mars",
            5: "Jupiter",
        },
        {
            "Mars": 5,
            "Jupiter": 5,
        },
    )

    rule = RajaYogaRule()

    result = rule.evaluate(
        context
    )

    assert result.detected is True
    assert result.name == "Raja Yoga"
