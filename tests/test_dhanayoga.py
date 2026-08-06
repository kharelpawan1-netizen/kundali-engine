"""
tests/test_dhanayoga.py

Tests for structural Dhana Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult

from yogas.dhanayoga import (
    DHANA_YOGA_NAME,
    WEALTH_HOUSES,
    SUPPORTING_WEALTH_HOUSES,
    DhanaYogaRule,
    detect_dhanayoga,
    find_supporting_wealth_associations,
    find_wealth_lord_associations,
    find_wealth_lords_in_wealth_houses,
    house_lord,
    is_supporting_wealth_house,
    is_wealth_house,
    lords_have_association,
    planets_conjunct,
)


# ============================================================
# TEST HELPER
# ============================================================

def make_context(
    house_lords,
    planet_houses,
):
    """
    Build a minimal test context.

    house_lords:
        {house_number: planet_name}

    planet_houses:
        {planet_name: house_number}
    """

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
        )
        for name, house
        in planet_houses.items()
    }

    return SimpleNamespace(
        houses=houses,
        planets=planets,
    )


# ============================================================
# CONSTANTS
# ============================================================

def test_wealth_houses():
    assert WEALTH_HOUSES == (
        2,
        11,
    )


def test_supporting_wealth_houses():
    assert SUPPORTING_WEALTH_HOUSES == (
        1,
        5,
        9,
    )


# ============================================================
# HOUSE CLASSIFICATION
# ============================================================

def test_primary_wealth_houses():
    assert is_wealth_house(2)
    assert is_wealth_house(11)


@pytest.mark.parametrize(
    "house",
    [
        1,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        12,
    ],
)
def test_non_primary_wealth_houses(
    house,
):
    assert not is_wealth_house(
        house
    )


def test_supporting_wealth_houses():
    assert is_supporting_wealth_house(1)
    assert is_supporting_wealth_house(5)
    assert is_supporting_wealth_house(9)


@pytest.mark.parametrize(
    "house",
    [
        2,
        3,
        4,
        6,
        7,
        8,
        10,
        11,
        12,
    ],
)
def test_non_supporting_wealth_houses(
    house,
):
    assert not is_supporting_wealth_house(
        house
    )


# ============================================================
# HOUSE LORD
# ============================================================

def test_house_lord_returns_lord():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 2,
            "Venus": 11,
        },
    )

    assert house_lord(
        context,
        2,
    ) == "Jupiter"

    assert house_lord(
        context,
        11,
    ) == "Venus"


def test_house_lord_missing_house():
    context = make_context(
        {
            2: "Jupiter",
        },
        {
            "Jupiter": 2,
        },
    )

    assert house_lord(
        context,
        11,
    ) is None


@pytest.mark.parametrize(
    "house",
    [
        0,
        -1,
        13,
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
# CONJUNCTION
# ============================================================

def test_planets_conjunct():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    assert planets_conjunct(
        context,
        "Jupiter",
        "Venus",
    )


def test_planets_not_conjunct():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 2,
            "Venus": 5,
        },
    )

    assert not planets_conjunct(
        context,
        "Jupiter",
        "Venus",
    )


def test_planets_conjunct_missing_planet():
    context = make_context(
        {
            2: "Jupiter",
        },
        {
            "Jupiter": 2,
        },
    )

    assert not planets_conjunct(
        context,
        "Jupiter",
        "Venus",
    )


def test_lords_have_association():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    assert lords_have_association(
        context,
        "Jupiter",
        "Venus",
    )


def test_same_lord_is_not_two_planet_association():
    context = make_context(
        {
            2: "Jupiter",
            11: "Jupiter",
        },
        {
            "Jupiter": 5,
        },
    )

    assert not lords_have_association(
        context,
        "Jupiter",
        "Jupiter",
    )


# ============================================================
# 2ND + 11TH LORD ASSOCIATION
# ============================================================

def test_second_and_eleventh_lords_conjunct():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    associations = (
        find_wealth_lord_associations(
            context
        )
    )

    assert associations

    assert any(
        association[
            "wealth_house_a"
        ] == 2
        and association[
            "wealth_house_b"
        ] == 11
        and association[
            "wealth_lord_a"
        ] == "Jupiter"
        and association[
            "wealth_lord_b"
        ] == "Venus"
        and association[
            "association"
        ] == "conjunction"
        for association in associations
    )


def test_second_and_eleventh_lords_not_conjunct():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 2,
            "Venus": 8,
        },
    )

    associations = (
        find_wealth_lord_associations(
            context
        )
    )

    assert associations == []


# ============================================================
# WEALTH LORDS IN WEALTH HOUSES
# ============================================================

def test_second_lord_in_eleventh_house():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 8,
        },
    )

    findings = (
        find_wealth_lords_in_wealth_houses(
            context
        )
    )

    assert any(
        finding["source_house"] == 2
        and finding["lord"] == "Jupiter"
        and finding["occupied_house"] == 11
        for finding in findings
    )


def test_eleventh_lord_in_second_house():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 7,
            "Venus": 2,
        },
    )

    findings = (
        find_wealth_lords_in_wealth_houses(
            context
        )
    )

    assert any(
        finding["source_house"] == 11
        and finding["lord"] == "Venus"
        and finding["occupied_house"] == 2
        for finding in findings
    )


def test_wealth_lord_outside_wealth_houses():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 9,
        },
    )

    findings = (
        find_wealth_lords_in_wealth_houses(
            context
        )
    )

    assert findings == []


# ============================================================
# SUPPORTING WEALTH ASSOCIATIONS
# ============================================================

def test_second_lord_conjunct_fifth_lord():
    context = make_context(
        {
            1: "Mars",
            2: "Jupiter",
            5: "Moon",
            11: "Venus",
        },
        {
            "Mars": 1,
            "Jupiter": 6,
            "Moon": 6,
            "Venus": 10,
        },
    )

    findings = (
        find_supporting_wealth_associations(
            context
        )
    )

    assert any(
        finding["wealth_house"] == 2
        and finding["wealth_lord"] == "Jupiter"
        and finding["supporting_house"] == 5
        and finding["supporting_lord"] == "Moon"
        and finding["association"] == "conjunction"
        for finding in findings
    )


def test_eleventh_lord_conjunct_ninth_lord():
    context = make_context(
        {
            2: "Jupiter",
            9: "Mars",
            11: "Venus",
        },
        {
            "Jupiter": 3,
            "Venus": 7,
            "Mars": 7,
        },
    )

    findings = (
        find_supporting_wealth_associations(
            context
        )
    )

    assert any(
        finding["wealth_house"] == 11
        and finding["wealth_lord"] == "Venus"
        and finding["supporting_house"] == 9
        and finding["supporting_lord"] == "Mars"
        and finding["association"] == "conjunction"
        for finding in findings
    )


# ============================================================
# DETECTOR
# ============================================================

def test_dhana_yoga_detected_from_2nd_11th_lord_conjunction():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == DHANA_YOGA_NAME
    assert result.category == "Dhana Yoga"


def test_dhana_yoga_detected_from_2nd_lord_in_11th():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 8,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is True


def test_dhana_yoga_detected_from_11th_lord_in_2nd():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 8,
            "Venus": 2,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is True


def test_dhana_yoga_detected_from_supporting_association():
    context = make_context(
        {
            2: "Jupiter",
            5: "Moon",
            11: "Venus",
        },
        {
            "Jupiter": 6,
            "Moon": 6,
            "Venus": 10,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is True


def test_no_dhana_yoga():
    context = make_context(
        {
            1: "Mars",
            2: "Jupiter",
            5: "Moon",
            9: "Sun",
            11: "Venus",
        },
        {
            "Mars": 1,
            "Jupiter": 3,
            "Moon": 6,
            "Sun": 9,
            "Venus": 12,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is False
    assert result.name == DHANA_YOGA_NAME
    assert result.category == "Dhana Yoga"


# ============================================================
# RESULT CONTRACT
# ============================================================

def test_detected_result_contains_evidence():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is True
    assert result.evidence
    assert result.involved_planets
    assert result.involved_houses
    assert result.conditions_met
    assert result.metadata


def test_undetected_result_contains_failed_condition():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 3,
            "Venus": 8,
        },
    )

    result = detect_dhanayoga(
        context
    )

    assert result.detected is False
    assert result.conditions_failed


# ============================================================
# RULE ADAPTER
# ============================================================

def test_dhana_yoga_rule():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 5,
        },
    )

    rule = DhanaYogaRule()

    result = rule.evaluate(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == DHANA_YOGA_NAME
    assert result.category == "Dhana Yoga"