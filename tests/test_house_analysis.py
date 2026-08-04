"""
tests/test_house_analysis.py

Tests for interpretation.house_analysis.

Compatible with Python 3.9.
"""

from datetime import datetime

import pytest

from interpretation.context import (
    PlanetContext,
    DashaContext,
    InterpretationContext,
)

from interpretation.house_analysis import (
    HOUSE_SIGNIFICATIONS,
    KENDRA_HOUSES,
    TRIKONA_HOUSES,
    DUSTHANA_HOUSES,
    UPACHAYA_HOUSES,
    MARAKA_HOUSES,
    ARTHA_HOUSES,
    KAMA_HOUSES,
    MOKSHA_HOUSES,
    HouseInterpretation,
    house_categories,
    find_house_lord_planet,
    occupants_of_house,
    interpret_house,
    analyze_houses,
    occupied_houses,
    empty_houses,
    house_lord_placements,
    house_analysis_report,
)


# ============================================================
# TEST FIXTURES
# ============================================================

class DummyPlanet:
    def __init__(
        self,
        name,
        sign,
        house,
        sign_degree=10.0,
        nakshatra="Ashwini",
        pada=1,
        longitude=10.0,
        retrograde=False,
        dignity=None,
    ):
        self.name = name
        self.sign = sign
        self.house = house
        self.sign_degree = sign_degree
        self.nakshatra = nakshatra
        self.pada = pada
        self.longitude = longitude
        self.retrograde = retrograde
        self.dignity = dignity


def make_context():
    """
    Sagittarius Ascendant test chart.

    Whole-sign houses:

        1  Sagittarius
        2  Capricorn
        3  Aquarius
        4  Pisces
        5  Aries
        6  Taurus
        7  Gemini
        8  Cancer
        9  Leo
        10 Virgo
        11 Libra
        12 Scorpio
    """

    planets = {
        "Sun": PlanetContext(
            name="Sun",
            sign="Sagittarius",
            sign_degree=16.27,
            house=1,
            nakshatra="Purva Ashadha",
            pada=1,
            longitude=256.515697,
            retrograde=False,
            dignity="Neutral",
        ),

        "Moon": PlanetContext(
            name="Moon",
            sign="Libra",
            sign_degree=16.59,
            house=11,
            nakshatra="Swati",
            pada=3,
            longitude=199.470553,
            retrograde=False,
            dignity="Neutral",
        ),

        "Mars": PlanetContext(
            name="Mars",
            sign="Aquarius",
            sign_degree=3.92,
            house=3,
            nakshatra="Dhanishta",
            pada=4,
            longitude=304.110091,
            retrograde=False,
            dignity="Neutral",
        ),

        "Jupiter": PlanetContext(
            name="Jupiter",
            sign="Aries",
            sign_degree=1.39,
            house=5,
            nakshatra="Ashwini",
            pada=1,
            longitude=1.399808,
            retrograde=False,
            dignity="Neutral",
        ),

        "Venus": PlanetContext(
            name="Venus",
            sign="Scorpio",
            sign_degree=7.42,
            house=12,
            nakshatra="Anuradha",
            pada=2,
            longitude=217.712576,
            retrograde=False,
            dignity="Neutral",
        ),

        "Saturn": PlanetContext(
            name="Saturn",
            sign="Aries",
            sign_degree=16.55,
            house=5,
            nakshatra="Bharani",
            pada=1,
            longitude=16.542416,
            retrograde=False,
            dignity="Debilitated",
        ),

        "Rahu": PlanetContext(
            name="Rahu",
            sign="Cancer",
            sign_degree=11.20,
            house=8,
            nakshatra="Pushya",
            pada=3,
            longitude=101.187424,
            retrograde=True,
            dignity="Not Implemented",
        ),

        "Ketu": PlanetContext(
            name="Ketu",
            sign="Capricorn",
            sign_degree=11.20,
            house=2,
            nakshatra="Shravana",
            pada=1,
            longitude=281.187424,
            retrograde=True,
            dignity="Not Implemented",
        ),
    }

    dasha = DashaContext(
        mahadasha="Jupiter",
        antardasha="Saturn",
        pratyantardasha="Mercury",
        sookshma="Venus",
        prana="Mars",
        deha="Moon",
    )

    return InterpretationContext(
        name="Test Native",
        birth_datetime=datetime(
            2000,
            1,
            1,
            12,
            0,
            0,
        ),
        place="Kathmandu",
        latitude=27.7172,
        longitude=85.3240,
        timezone="Asia/Kathmandu",
        ascendant_sign="Sagittarius",
        ascendant_degree=16.515697,
        planets=planets,
        dasha=dasha,
        houses={},
    )


# ============================================================
# HOUSE CATEGORY TESTS
# ============================================================

def test_house_categories_kendra():
    assert set(KENDRA_HOUSES) == {
        1,
        4,
        7,
        10,
    }

    assert "kendra" in house_categories(1)
    assert "kendra" in house_categories(4)
    assert "kendra" in house_categories(7)
    assert "kendra" in house_categories(10)


def test_house_categories_trikona():
    assert "trikona" in house_categories(1)
    assert "trikona" in house_categories(5)
    assert "trikona" in house_categories(9)


def test_house_categories_dusthana():
    assert "dusthana" in house_categories(6)
    assert "dusthana" in house_categories(8)
    assert "dusthana" in house_categories(12)


def test_house_categories_upachaya():
    assert "upachaya" in house_categories(3)
    assert "upachaya" in house_categories(6)
    assert "upachaya" in house_categories(10)
    assert "upachaya" in house_categories(11)


def test_house_categories_maraka():
    assert "maraka" in house_categories(2)
    assert "maraka" in house_categories(7)


def test_house_categories_artha():
    assert "artha" in house_categories(2)
    assert "artha" in house_categories(6)
    assert "artha" in house_categories(10)


def test_house_categories_kama():
    assert "kama" in house_categories(3)
    assert "kama" in house_categories(7)
    assert "kama" in house_categories(11)


def test_house_categories_moksha():
    assert "moksha" in house_categories(4)
    assert "moksha" in house_categories(8)
    assert "moksha" in house_categories(12)


def test_house_categories_invalid_low():
    with pytest.raises(ValueError):
        house_categories(0)


def test_house_categories_invalid_high():
    with pytest.raises(ValueError):
        house_categories(13)


# ============================================================
# HOUSE LORD TESTS
# ============================================================

def test_find_house_lord_planet():
    context = make_context()

    # Sagittarius Lagna:
    # 1st house = Sagittarius
    # Sagittarius lord = Jupiter
    # Jupiter is in Aries, house 5.
    lord = find_house_lord_planet(
        context,
        1,
    )

    assert lord is not None
    assert lord.name == "Jupiter"
    assert lord.sign == "Aries"
    assert lord.house == 5


def test_find_house_lord_for_second_house():
    context = make_context()

    # Capricorn is 2nd house.
    # Capricorn lord = Saturn.
    lord = find_house_lord_planet(
        context,
        2,
    )

    assert lord is not None
    assert lord.name == "Saturn"
    assert lord.sign == "Aries"
    assert lord.house == 5


def test_find_house_lord_for_tenth_house():
    context = make_context()

    # Virgo is 10th house.
    # Virgo lord = Mercury.
    # Mercury is intentionally absent from this fixture.
    lord = find_house_lord_planet(
        context,
        10,
    )

    assert lord is None


def test_find_house_lord_invalid_house():
    context = make_context()

    with pytest.raises(ValueError):
        find_house_lord_planet(
            context,
            13,
        )


# ============================================================
# OCCUPANT TESTS
# ============================================================

def test_occupants_of_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        5,
    )

    names = {
        planet.name
        for planet in occupants
    }

    assert names == {
        "Jupiter",
        "Saturn",
    }


def test_occupants_of_house_single_planet():
    context = make_context()

    occupants = occupants_of_house(
        context,
        1,
    )

    assert len(occupants) == 1
    assert occupants[0].name == "Sun"


def test_occupants_of_empty_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        4,
    )

    assert occupants == []


def test_occupants_of_house_invalid():
    context = make_context()

    with pytest.raises(ValueError):
        occupants_of_house(
            context,
            0,
        )


# ============================================================
# HOUSE INTERPRETATION TESTS
# ============================================================

def test_interpret_house_returns_expected_type():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert isinstance(
        result,
        HouseInterpretation,
    )


def test_interpret_first_house():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert result.house == 1
    assert result.sign == "Sagittarius"
    assert result.lord == "Jupiter"

    assert result.lord_planet == "Jupiter"
    assert result.lord_sign == "Aries"
    assert result.lord_house == 5

    assert result.occupants == ["Sun"]


def test_interpret_fifth_house():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    assert result.house == 5
    assert result.sign == "Aries"
    assert result.lord == "Mars"

    assert set(result.occupants) == {
        "Jupiter",
        "Saturn",
    }


def test_interpret_eighth_house():
    context = make_context()

    result = interpret_house(
        context,
        8,
    )

    assert result.house == 8
    assert result.sign == "Cancer"
    assert result.lord == "Moon"

    assert result.occupants == ["Rahu"]

    assert (
        result.natural_occupant_types["Rahu"]
        == "malefic"
    )


def test_interpret_empty_house():
    context = make_context()

    result = interpret_house(
        context,
        4,
    )

    assert result.occupants == []
    assert result.lord_planet == "Jupiter"
    assert result.lord_house == 5


def test_interpret_house_invalid():
    context = make_context()

    with pytest.raises(ValueError):
        interpret_house(
            context,
            13,
        )


# ============================================================
# THEME TESTS
# ============================================================

def test_house_interpretation_contains_house_theme():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert (
        HOUSE_SIGNIFICATIONS[1][0]
        in result.significations
    )

    assert (
        "self, body, identity and life direction"
        in result.themes
    )


def test_house_interpretation_categories():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    assert "trikona" in result.categories
    assert "kama" not in result.categories


# ============================================================
# EVIDENCE TESTS
# ============================================================

def test_interpret_house_contains_evidence():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert len(result.evidence) > 0

    evidence_text = " ".join(
        result.evidence
    )

    assert "House 1 falls in Sagittarius." in evidence_text
    assert "House 1 is ruled by Jupiter." in evidence_text
    assert "Sun" in evidence_text
    assert "Jupiter" in evidence_text


def test_empty_house_contains_evidence():
    context = make_context()

    result = interpret_house(
        context,
        4,
    )

    evidence_text = " ".join(
        result.evidence
    )

    assert (
        "No classical planet occupies this house."
        in evidence_text
    )


# ============================================================
# COMPLETE HOUSE ANALYSIS
# ============================================================

def test_analyze_houses():
    context = make_context()

    results = analyze_houses(
        context
    )

    assert isinstance(
        results,
        dict,
    )

    assert len(results) == 12

    assert set(results.keys()) == set(
        range(1, 13)
    )

    for house in range(1, 13):
        assert isinstance(
            results[house],
            HouseInterpretation,
        )


# ============================================================
# OCCUPIED / EMPTY HOUSE TESTS
# ============================================================

def test_occupied_houses():
    context = make_context()

    occupied = occupied_houses(
        context
    )

    assert occupied == [
        1,
        2,
        3,
        5,
        8,
        11,
        12,
    ]


def test_empty_houses():
    context = make_context()

    empty = empty_houses(
        context
    )

    assert empty == [
        4,
        6,
        7,
        9,
        10,
    ]


# ============================================================
# HOUSE LORD PLACEMENT TESTS
# ============================================================

def test_house_lord_placements():
    context = make_context()

    placements = house_lord_placements(
        context
    )

    assert len(placements) == 12

    # Sagittarius Lagna:
    #
    # 1st Sagittarius -> Jupiter -> 5th
    # 2nd Capricorn -> Saturn -> 5th
    # 3rd Aquarius -> Saturn -> 5th
    # 4th Pisces -> Jupiter -> 5th
    # 5th Aries -> Mars -> 3rd
    # 6th Taurus -> Venus -> 12th
    # 7th Gemini -> Mercury -> unavailable
    # 8th Cancer -> Moon -> 11th
    # 9th Leo -> Sun -> 1st
    # 10th Virgo -> Mercury -> unavailable
    # 11th Libra -> Venus -> 12th
    # 12th Scorpio -> Mars -> 3rd

    assert placements[1] == 5
    assert placements[2] == 5
    assert placements[3] == 5
    assert placements[4] == 5
    assert placements[5] == 3
    assert placements[6] == 12
    assert placements[7] is None
    assert placements[8] == 11
    assert placements[9] == 1
    assert placements[10] is None
    assert placements[11] == 12
    assert placements[12] == 3


# ============================================================
# REPORT TEST
# ============================================================

def test_house_analysis_report():
    context = make_context()

    report = house_analysis_report(
        context
    )

    assert isinstance(
        report,
        list,
    )

    assert len(report) == 12

    assert report[0].startswith(
        "House 1:"
    )

    assert "Sagittarius" in report[0]
    assert "lord=Jupiter" in report[0]
    assert "occupants=Sun" in report[0]


# ============================================================
# PUBLIC DATA CONSISTENCY
# ============================================================

def test_house_significations_cover_all_houses():
    assert set(
        HOUSE_SIGNIFICATIONS.keys()
    ) == set(
        range(1, 13)
    )

    for house in range(1, 13):
        assert len(
            HOUSE_SIGNIFICATIONS[house]
        ) > 0


def test_house_categories_are_lists():
    for house in range(1, 13):
        categories = house_categories(
            house
        )

        assert isinstance(
            categories,
            list,
        )