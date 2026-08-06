"""
tests/test_parivartana.py

Tests for structural Parivartana Yoga detection.
"""

from types import SimpleNamespace

import pytest

from yogas.base import YogaResult

from yogas.parivartana import (
    PARIVARTANA_YOGA_NAME,
    MAHA_PARIVARTANA_NAME,
    KHALA_PARIVARTANA_NAME,
    DAINYA_PARIVARTANA_NAME,
    DUSTHANA_HOUSES,
    KHALA_HOUSES,
    MAHA_HOUSES,
    normalize_sign,
    house_lord,
    is_dusthana_house,
    is_khala_house,
    is_maha_house,
    house_lords_exchange,
    classify_parivartana,
    find_parivartana_exchanges,
    detect_parivartana,
    ParivartanaYogaRule,
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
    Build a minimal chart context.

    planet_signs:
        {planet_name: sign_number_or_name}

    The tests use the whole-sign house model.
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

    planets = {}

    all_planets = set(
        planet_houses
    ) | set(
        planet_signs
    )

    for name in all_planets:
        planets[name] = SimpleNamespace(
            name=name,
            house=planet_houses.get(
                name
            ),
            sign=planet_signs.get(
                name
            ),
        )

    return SimpleNamespace(
        houses=houses,
        planets=planets,
    )


# ============================================================
# SIGN NORMALIZATION
# ============================================================

@pytest.mark.parametrize(
    "value,expected",
    [
        (1, 1),
        (12, 12),
        ("Aries", 1),
        ("aries", 1),
        ("Mesha", 1),
        ("Taurus", 2),
        ("Mithuna", 3),
        ("Karka", 4),
        ("Simha", 5),
        ("Kanya", 6),
        ("Tula", 7),
        ("Vrishchika", 8),
        ("Dhanu", 9),
        ("Makara", 10),
        ("Kumbha", 11),
        ("Meena", 12),
    ],
)
def test_normalize_sign(
    value,
    expected,
):
    assert normalize_sign(
        value
    ) == expected


@pytest.mark.parametrize(
    "value",
    [
        None,
        0,
        13,
        "",
        "unknown",
        True,
    ],
)
def test_normalize_sign_invalid(
    value,
):
    assert normalize_sign(
        value
    ) is None


# ============================================================
# HOUSE CLASSIFICATION
# ============================================================

def test_dusthana_houses():
    assert DUSTHANA_HOUSES == (
        6,
        8,
        12,
    )

    for house in DUSTHANA_HOUSES:
        assert is_dusthana_house(
            house
        )


def test_khala_houses():
    assert KHALA_HOUSES == (
        3,
    )

    assert is_khala_house(
        3
    )


def test_maha_houses():
    assert MAHA_HOUSES == (
        1,
        2,
        4,
        5,
        7,
        9,
        10,
        11,
    )

    for house in MAHA_HOUSES:
        assert is_maha_house(
            house
        )


@pytest.mark.parametrize(
    "house",
    [0, 13, -1],
)
def test_house_classification_invalid(
    house,
):
    with pytest.raises(
        ValueError
    ):
        is_dusthana_house(
            house
        )


# ============================================================
# HOUSE LORD
# ============================================================

def test_house_lord():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
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


def test_missing_house_lord():
    context = make_context(
        {},
        {},
    )

    assert house_lord(
        context,
        2,
    ) is None


# ============================================================
# CLASSIFICATION
# ============================================================

def test_classify_maha():
    assert classify_parivartana(
        2,
        11,
    ) == MAHA_PARIVARTANA_NAME


def test_classify_maha_kendra_trikona():
    assert classify_parivartana(
        5,
        10,
    ) == MAHA_PARIVARTANA_NAME


def test_classify_khala():
    assert classify_parivartana(
        3,
        11,
    ) == KHALA_PARIVARTANA_NAME


def test_classify_dainya():
    assert classify_parivartana(
        8,
        9,
    ) == DAINYA_PARIVARTANA_NAME


def test_dainya_takes_precedence_over_khala():
    assert classify_parivartana(
        3,
        8,
    ) == DAINYA_PARIVARTANA_NAME


def test_dusthana_exchange_is_dainya():
    assert classify_parivartana(
        6,
        12,
    ) == DAINYA_PARIVARTANA_NAME


# ============================================================
# HOUSE-LORD EXCHANGE
# ============================================================

def test_house_lords_exchange():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
        },
    )

    assert house_lords_exchange(
        context,
        2,
        11,
    )


def test_reverse_house_order_also_detects_exchange():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
        },
    )

    assert house_lords_exchange(
        context,
        11,
        2,
    )


def test_no_exchange_when_lord_stays_elsewhere():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 5,
            "Venus": 2,
        },
    )

    assert not house_lords_exchange(
        context,
        2,
        11,
    )


def test_same_house_is_not_exchange():
    context = make_context(
        {
            2: "Jupiter",
        },
        {
            "Jupiter": 2,
        },
    )

    assert not house_lords_exchange(
        context,
        2,
        2,
    )


# ============================================================
# FIND EXCHANGES
# ============================================================

def test_find_maha_exchange():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
        },
    )

    findings = find_parivartana_exchanges(
        context
    )

    assert len(
        findings
    ) == 1

    finding = findings[0]

    assert finding[
        "house_a"
    ] == 2

    assert finding[
        "house_b"
    ] == 11

    assert finding[
        "lord_a"
    ] == "Jupiter"

    assert finding[
        "lord_b"
    ] == "Venus"

    assert finding[
        "classification"
    ] == MAHA_PARIVARTANA_NAME


def test_no_exchange():
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

    findings = find_parivartana_exchanges(
        context
    )

    assert findings == []


# ============================================================
# DETECTOR
# ============================================================

def test_detect_maha_parivartana():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
        },
    )

    result = detect_parivartana(
        context
    )

    assert isinstance(
        result,
        YogaResult,
    )

    assert result.detected is True
    assert result.name == MAHA_PARIVARTANA_NAME
    assert result.category == "Parivartana Yoga"
    assert result.evidence
    assert result.involved_planets
    assert result.involved_houses


def test_detect_khala_parivartana():
    context = make_context(
        {
            3: "Mars",
            11: "Venus",
        },
        {
            "Mars": 11,
            "Venus": 3,
        },
    )

    result = detect_parivartana(
        context
    )

    assert result.detected is True
    assert result.name == KHALA_PARIVARTANA_NAME


def test_detect_dainya_parivartana():
    context = make_context(
        {
            8: "Saturn",
            9: "Jupiter",
        },
        {
            "Saturn": 9,
            "Jupiter": 8,
        },
    )

    result = detect_parivartana(
        context
    )

    assert result.detected is True
    assert result.name == DAINYA_PARIVARTANA_NAME


def test_detect_no_parivartana():
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

    result = detect_parivartana(
        context
    )

    assert result.detected is False
    assert result.name == PARIVARTANA_YOGA_NAME


# ============================================================
# RULE ADAPTER
# ============================================================

def test_parivartana_rule():
    context = make_context(
        {
            2: "Jupiter",
            11: "Venus",
        },
        {
            "Jupiter": 11,
            "Venus": 2,
        },
    )

    rule = ParivartanaYogaRule()

    result = rule.evaluate(
        context
    )

    assert result.detected is True
    assert result.name == MAHA_PARIVARTANA_NAME