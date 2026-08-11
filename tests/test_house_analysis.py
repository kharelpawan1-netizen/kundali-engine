"""
tests/test_house_analysis.py

Tests for interpretation.house_analysis.

These tests validate the actual structural behavior of:
    - interpretation.context
    - interpretation.planet_analysis
    - interpretation.house_analysis

The tests intentionally follow the implementation's declared
Parashari model rather than introducing independent assumptions.

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

    The fixture intentionally contains the classical planets
    plus Rahu and Ketu, while Mercury is omitted so that the
    house-lord-unavailable behavior can also be tested.
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


def test_kendra_houses():
    assert KENDRA_HOUSES == {
        1,
        4,
        7,
        10,
    }

    for house in KENDRA_HOUSES:
        assert "kendra" in house_categories(house)


def test_trikona_houses():
    assert TRIKONA_HOUSES == {
        1,
        5,
        9,
    }

    for house in TRIKONA_HOUSES:
        assert "trikona" in house_categories(house)


def test_dusthana_houses():
    assert DUSTHANA_HOUSES == {
        6,
        8,
        12,
    }

    for house in DUSTHANA_HOUSES:
        assert "dusthana" in house_categories(house)


def test_upachaya_houses():
    assert UPACHAYA_HOUSES == {
        3,
        6,
        10,
        11,
    }

    for house in UPACHAYA_HOUSES:
        assert "upachaya" in house_categories(house)


def test_maraka_houses():
    assert MARAKA_HOUSES == {
        2,
        7,
    }

    for house in MARAKA_HOUSES:
        assert "maraka" in house_categories(house)


def test_artha_houses():
    assert ARTHA_HOUSES == {
        2,
        6,
        10,
    }

    for house in ARTHA_HOUSES:
        assert "artha" in house_categories(house)


def test_kama_houses():
    assert KAMA_HOUSES == {
        3,
        7,
        11,
    }

    for house in KAMA_HOUSES:
        assert "kama" in house_categories(house)


def test_moksha_houses():
    assert MOKSHA_HOUSES == {
        4,
        8,
        12,
    }

    for house in MOKSHA_HOUSES:
        assert "moksha" in house_categories(house)


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 99],
)
def test_house_categories_invalid_house(house):
    with pytest.raises(ValueError):
        house_categories(house)


def test_house_category_combination_for_first_house():
    categories = house_categories(1)

    assert "kendra" in categories
    assert "trikona" in categories
    assert "dusthana" not in categories
    assert "upachaya" not in categories


def test_house_category_combination_for_sixth_house():
    categories = house_categories(6)

    assert "dusthana" in categories
    assert "upachaya" in categories
    assert "artha" in categories


def test_house_category_combination_for_tenth_house():
    categories = house_categories(10)

    assert "kendra" in categories
    assert "upachaya" in categories
    assert "artha" in categories


# ============================================================
# HOUSE SIGNIFICATION TESTS
# ============================================================


def test_house_significations_cover_all_houses():
    assert set(
        HOUSE_SIGNIFICATIONS.keys()
    ) == set(range(1, 13))


@pytest.mark.parametrize(
    "house",
    range(1, 13),
)
def test_each_house_has_significations(house):
    assert isinstance(
        HOUSE_SIGNIFICATIONS[house],
        list,
    )

    assert len(
        HOUSE_SIGNIFICATIONS[house]
    ) > 0


def test_first_house_significations():
    expected = {
        "body",
        "appearance",
        "personality",
        "identity",
        "vitality",
        "self-direction",
        "life orientation",
    }

    assert set(
        HOUSE_SIGNIFICATIONS[1]
    ) == expected


def test_tenth_house_contains_career_significations():
    assert "career" in HOUSE_SIGNIFICATIONS[10]
    assert "profession" in HOUSE_SIGNIFICATIONS[10]
    assert "authority" in HOUSE_SIGNIFICATIONS[10]
    assert "status" in HOUSE_SIGNIFICATIONS[10]


# ============================================================
# HOUSE LORD TESTS
# ============================================================


def test_find_first_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        1,
    )

    assert lord is not None
    assert lord.name == "Jupiter"
    assert lord.sign == "Aries"
    assert lord.house == 5


def test_find_second_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        2,
    )

    assert lord is not None
    assert lord.name == "Saturn"
    assert lord.sign == "Aries"
    assert lord.house == 5


def test_find_third_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        3,
    )

    assert lord is not None
    assert lord.name == "Saturn"
    assert lord.house == 5


def test_find_fourth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        4,
    )

    assert lord is not None
    assert lord.name == "Jupiter"
    assert lord.house == 5


def test_find_fifth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        5,
    )

    assert lord is not None
    assert lord.name == "Mars"
    assert lord.house == 3


def test_find_sixth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        6,
    )

    assert lord is not None
    assert lord.name == "Venus"
    assert lord.house == 12


def test_find_seventh_house_lord_unavailable():
    context = make_context()

    # Gemini is the seventh house and is ruled by Mercury.
    # Mercury is intentionally absent from the fixture.
    lord = find_house_lord_planet(
        context,
        7,
    )

    assert lord is None


def test_find_eighth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        8,
    )

    assert lord is not None
    assert lord.name == "Moon"
    assert lord.house == 11


def test_find_ninth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        9,
    )

    assert lord is not None
    assert lord.name == "Sun"
    assert lord.house == 1


def test_find_tenth_house_lord_unavailable():
    context = make_context()

    # Virgo is the tenth house and is ruled by Mercury.
    lord = find_house_lord_planet(
        context,
        10,
    )

    assert lord is None


def test_find_eleventh_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        11,
    )

    assert lord is not None
    assert lord.name == "Venus"
    assert lord.house == 12


def test_find_twelfth_house_lord():
    context = make_context()

    lord = find_house_lord_planet(
        context,
        12,
    )

    assert lord is not None
    assert lord.name == "Mars"
    assert lord.house == 3


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 99],
)
def test_find_house_lord_invalid_house(house):
    context = make_context()

    with pytest.raises(ValueError):
        find_house_lord_planet(
            context,
            house,
        )


# ============================================================
# OCCUPANT TESTS
# ============================================================


def test_occupants_first_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        1,
    )

    assert [
        planet.name
        for planet in occupants
    ] == ["Sun"]


def test_occupants_fifth_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        5,
    )

    assert {
        planet.name
        for planet in occupants
    } == {
        "Jupiter",
        "Saturn",
    }


def test_occupants_eighth_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        8,
    )

    assert [
        planet.name
        for planet in occupants
    ] == ["Rahu"]


def test_occupants_twelfth_house():
    context = make_context()

    occupants = occupants_of_house(
        context,
        12,
    )

    assert [
        planet.name
        for planet in occupants
    ] == ["Venus"]


def test_occupants_empty_house():
    context = make_context()

    assert occupants_of_house(
        context,
        4,
    ) == []


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 99],
)
def test_occupants_invalid_house(house):
    context = make_context()

    with pytest.raises(ValueError):
        occupants_of_house(
            context,
            house,
        )


# ============================================================
# FIRST HOUSE INTERPRETATION
# ============================================================


def test_first_house_interpretation():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert isinstance(
        result,
        HouseInterpretation,
    )

    assert result.house == 1
    assert result.sign == "Sagittarius"
    assert result.lord == "Jupiter"

    assert result.lord_planet == "Jupiter"
    assert result.lord_sign == "Aries"
    assert result.lord_house == 5

    assert result.occupants == ["Sun"]

    assert "kendra" in result.categories
    assert "trikona" in result.categories

    # According to planet_analysis.py, Sun is a natural malefic.
    assert (
        result.natural_occupant_types["Sun"]
        == "malefic"
    )

    # Sagittarius Ascendant:
    # Sun rules Leo, which is the ninth house.
    # Therefore Sun is functionally benefic in this model.
    assert (
        result.functional_occupant_types["Sun"]
        == "functional_benefic"
    )

    assert (
        "self, body, identity and life direction"
        in result.themes
    )


# ============================================================
# FIFTH HOUSE INTERPRETATION
# ============================================================


def test_fifth_house_interpretation():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    assert result.house == 5
    assert result.sign == "Aries"
    assert result.lord == "Mars"

    assert result.lord_planet == "Mars"
    assert result.lord_sign == "Aquarius"
    assert result.lord_house == 3

    assert set(result.occupants) == {
        "Jupiter",
        "Saturn",
    }

    assert "trikona" in result.categories
    assert "kama" not in result.categories
    assert "dusthana" not in result.categories


def test_fifth_house_occupant_natural_types():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    assert (
        result.natural_occupant_types["Jupiter"]
        == "benefic"
    )

    assert (
        result.natural_occupant_types["Saturn"]
        == "malefic"
    )


def test_fifth_house_occupant_functional_types():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    # Sagittarius Ascendant:
    #
    # Jupiter owns 1 and 4 -> functional benefic.
    # Saturn owns 2 and 3 -> conditional because 2/11 logic
    # is checked before 3 in the implementation.
    assert (
        result.functional_occupant_types["Jupiter"]
        == "functional_benefic"
    )

    assert (
        result.functional_occupant_types["Saturn"]
        == "conditional"
    )


# ============================================================
# EIGHTH HOUSE INTERPRETATION
# ============================================================


def test_eighth_house_interpretation():
    context = make_context()

    result = interpret_house(
        context,
        8,
    )

    assert result.house == 8
    assert result.sign == "Cancer"
    assert result.lord == "Moon"

    assert result.lord_planet == "Moon"
    assert result.lord_sign == "Libra"
    assert result.lord_house == 11

    assert result.occupants == ["Rahu"]

    assert (
        result.natural_occupant_types["Rahu"]
        == "malefic"
    )

    assert (
        result.functional_occupant_types["Rahu"]
        == "node"
    )

    assert "dusthana" in result.categories
    assert "moksha" in result.categories


# ============================================================
# EMPTY HOUSE INTERPRETATION
# ============================================================


def test_empty_house_interpretation():
    context = make_context()

    result = interpret_house(
        context,
        4,
    )

    assert result.house == 4
    assert result.sign == "Pisces"
    assert result.lord == "Jupiter"

    assert result.occupants == []

    assert result.lord_planet == "Jupiter"
    assert result.lord_sign == "Aries"
    assert result.lord_house == 5

    assert result.natural_occupant_types == {}
    assert result.functional_occupant_types == {}

    assert "kendra" in result.categories
    assert "moksha" in result.categories


# ============================================================
# UNAVAILABLE LORD INTERPRETATION
# ============================================================


def test_house_with_unavailable_lord():
    context = make_context()

    result = interpret_house(
        context,
        7,
    )

    assert result.house == 7
    assert result.sign == "Gemini"
    assert result.lord == "Mercury"

    assert result.lord_planet is None
    assert result.lord_sign is None
    assert result.lord_house is None

    assert result.occupants == []


def test_tenth_house_with_unavailable_lord():
    context = make_context()

    result = interpret_house(
        context,
        10,
    )

    assert result.house == 10
    assert result.sign == "Virgo"
    assert result.lord == "Mercury"

    assert result.lord_planet is None
    assert result.lord_sign is None
    assert result.lord_house is None


# ============================================================
# HOUSE INTERPRETATION VALIDATION
# ============================================================


@pytest.mark.parametrize(
    "house",
    [0, -1, 13, 99],
)
def test_interpret_house_invalid_house(house):
    context = make_context()

    with pytest.raises(ValueError):
        interpret_house(
            context,
            house,
        )


def test_house_interpretation_significations_are_copied():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert result.significations == (
        HOUSE_SIGNIFICATIONS[1]
    )

    # The returned list is a separate list.
    assert result.significations is not (
        HOUSE_SIGNIFICATIONS[1]
    )


def test_house_interpretation_categories_are_lists():
    context = make_context()

    for house in range(1, 13):
        result = interpret_house(
            context,
            house,
        )

        assert isinstance(
            result.categories,
            list,
        )


# ============================================================
# THEME TESTS
# ============================================================


def test_first_house_theme():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert (
        "self, body, identity and life direction"
        in result.themes
    )

    assert (
        "major pillar of practical life"
        in result.themes
    )

    assert (
        "dharma and supportive life potential"
        in result.themes
    )


def test_fifth_house_theme():
    context = make_context()

    result = interpret_house(
        context,
        5,
    )

    assert (
        "intelligence, education, creativity, children "
        "and purva punya"
        in result.themes
    )

    assert (
        "dharma and supportive life potential"
        in result.themes
    )


def test_sixth_house_themes():
    context = make_context()

    result = interpret_house(
        context,
        6,
    )

    assert (
        "challenge, transformation and problem-solving"
        in result.themes
    )

    assert (
        "growth through effort, time and experience"
        in result.themes
    )

    assert (
        "material development and practical achievement"
        in result.themes
    )


def test_twelfth_house_themes():
    context = make_context()

    result = interpret_house(
        context,
        12,
    )

    assert (
        "challenge, transformation and problem-solving"
        in result.themes
    )

    assert (
        "emotional depth, release and inner development"
        in result.themes
    )


# ============================================================
# EVIDENCE TESTS
# ============================================================


def test_first_house_evidence():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert len(
        result.evidence
    ) > 0

    evidence_text = " ".join(
        result.evidence
    )

    assert (
        "House 1 falls in Sagittarius."
        in evidence_text
    )

    assert (
        "House 1 is ruled by Jupiter."
        in evidence_text
    )

    assert (
        "Occupying planets: Sun."
        in evidence_text
    )

    assert (
        "Sun occupies house 1 from Sagittarius."
        in evidence_text
    )

    assert (
        "Sun is naturally malefic."
        in evidence_text
    )

    assert (
        "Sun has functional_benefic functional classification."
        in evidence_text
    )

    assert (
        "The house lord Jupiter is placed in house 5 in Aries."
        in evidence_text
    )


def test_empty_house_evidence():
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

    assert (
        "The house lord Jupiter is placed in house 5 in Aries."
        in evidence_text
    )


def test_unavailable_lord_evidence():
    context = make_context()

    result = interpret_house(
        context,
        7,
    )

    evidence_text = " ".join(
        result.evidence
    )

    assert (
        "The house lord Mercury is not available in the normalized planet set."
        in evidence_text
    )


# ============================================================
# COMPLETE HOUSE ANALYSIS
# ============================================================


def test_analyze_houses_returns_twelve_houses():
    context = make_context()

    results = analyze_houses(
        context
    )

    assert isinstance(
        results,
        dict,
    )

    assert len(results) == 12

    assert set(
        results.keys()
    ) == set(range(1, 13))


@pytest.mark.parametrize(
    "house",
    range(1, 13),
)
def test_analyze_houses_returns_house_interpretation(
    house,
):
    context = make_context()

    results = analyze_houses(
        context
    )

    assert isinstance(
        results[house],
        HouseInterpretation,
    )

    assert results[house].house == house


# ============================================================
# OCCUPIED HOUSE TESTS
# ============================================================


def test_occupied_houses():
    context = make_context()

    assert occupied_houses(
        context
    ) == [
        1,
        2,
        3,
        5,
        8,
        11,
        12,
    ]


def test_occupied_houses_are_sorted():
    context = make_context()

    occupied = occupied_houses(
        context
    )

    assert occupied == sorted(
        occupied
    )


def test_empty_houses():
    context = make_context()

    assert empty_houses(
        context
    ) == [
        4,
        6,
        7,
        9,
        10,
    ]


def test_occupied_and_empty_houses_partition_chart():
    context = make_context()

    occupied = set(
        occupied_houses(context)
    )

    empty = set(
        empty_houses(context)
    )

    assert occupied.isdisjoint(
        empty
    )

    assert occupied | empty == set(
        range(1, 13)
    )


# ============================================================
# HOUSE LORD PLACEMENT TESTS
# ============================================================


def test_house_lord_placements():
    context = make_context()

    placements = house_lord_placements(
        context
    )

    assert len(placements) == 12

    assert placements == {
        1: 5,
        2: 5,
        3: 5,
        4: 5,
        5: 3,
        6: 12,
        7: None,
        8: 11,
        9: 1,
        10: None,
        11: 12,
        12: 3,
    }


def test_house_lord_placements_contains_all_houses():
    context = make_context()

    placements = house_lord_placements(
        context
    )

    assert set(
        placements.keys()
    ) == set(range(1, 13))


# ============================================================
# REPORT TESTS
# ============================================================


def test_house_analysis_report_returns_twelve_lines():
    context = make_context()

    report = house_analysis_report(
        context
    )

    assert isinstance(
        report,
        list,
    )

    assert len(report) == 12


def test_house_analysis_report_first_house():
    context = make_context()

    report = house_analysis_report(
        context
    )

    first = report[0]

    assert first.startswith(
        "House 1:"
    )

    assert "Sagittarius" in first
    assert "lord=Jupiter" in first
    assert "lord placed=House 5" in first
    assert "occupants=Sun" in first


def test_house_analysis_report_empty_house():
    context = make_context()

    report = house_analysis_report(
        context
    )

    # House 4 is the fifth entry.
    house_four = report[3]

    assert house_four.startswith(
        "House 4:"
    )

    assert "Pisces" in house_four
    assert "lord=Jupiter" in house_four
    assert "lord placed=House 5" in house_four
    assert "occupants=none" in house_four


def test_house_analysis_report_unavailable_lord():
    context = make_context()

    report = house_analysis_report(
        context
    )

    # House 7 is the seventh entry.
    house_seven = report[6]

    assert house_seven.startswith(
        "House 7:"
    )

    assert "Gemini" in house_seven
    assert "lord=Mercury" in house_seven
    assert "lord placed=not available" in house_seven
    assert "occupants=none" in house_seven


# ============================================================
# DATA MODEL TESTS
# ============================================================


def test_house_interpretation_is_frozen():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    with pytest.raises(
        AttributeError
    ):
        result.house = 2


def test_house_interpretation_contains_expected_fields():
    context = make_context()

    result = interpret_house(
        context,
        1,
    )

    assert hasattr(
        result,
        "house",
    )

    assert hasattr(
        result,
        "sign",
    )

    assert hasattr(
        result,
        "lord",
    )

    assert hasattr(
        result,
        "significations",
    )

    assert hasattr(
        result,
        "occupants",
    )

    assert hasattr(
        result,
        "lord_planet",
    )

    assert hasattr(
        result,
        "lord_sign",
    )

    assert hasattr(
        result,
        "lord_house",
    )

    assert hasattr(
        result,
        "categories",
    )

    assert hasattr(
        result,
        "natural_occupant_types",
    )

    assert hasattr(
        result,
        "functional_occupant_types",
    )

    assert hasattr(
        result,
        "themes",
    )

    assert hasattr(
        result,
        "evidence",
    )