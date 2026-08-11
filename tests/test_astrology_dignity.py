"""
tests/test_astrology_dignity.py

Unit tests for astrology.dignity.

The tests validate the actual dignity model implemented in
astrology.dignity.

Covered:
    - Exaltation
    - Debilitation
    - Own Sign
    - Moolatrikona
    - Friendly Sign
    - Enemy Sign
    - Neutral Sign
    - Dignity priority
    - Sign lord relationships
    - Mapping integrity
    - Unknown planet/sign validation

Compatible with Python 3.9.
"""

import pytest

from astrology.dignity import (
    DEBILITATION_SIGNS,
    EXALTATION_SIGNS,
    MOOLATRIKONA_SIGNS,
    NATURAL_ENEMIES,
    NATURAL_FRIENDS,
    OWN_SIGNS,
    SIGN_LORDS,
    get_dignity,
    is_debilitated,
    is_exalted,
    is_moolatrikona,
    is_own_sign,
)


# ============================================================
# Exaltation
# ============================================================


@pytest.mark.parametrize(
    "planet, sign",
    list(EXALTATION_SIGNS.items()),
)
def test_is_exalted(planet, sign):
    """Every configured exaltation relationship is recognized."""

    assert is_exalted(planet, sign)
    assert get_dignity(planet, sign) == "Exalted"


@pytest.mark.parametrize(
    "planet, sign",
    list(DEBILITATION_SIGNS.items()),
)
def test_exaltation_and_debilitation_are_distinct(planet, sign):
    """A planet's exaltation and debilitation signs are distinct."""

    assert EXALTATION_SIGNS[planet] != sign
    assert not is_exalted(planet, sign)


# ============================================================
# Debilitation
# ============================================================


@pytest.mark.parametrize(
    "planet, sign",
    list(DEBILITATION_SIGNS.items()),
)
def test_is_debilitated(planet, sign):
    """Every configured debilitation relationship is recognized."""

    assert is_debilitated(planet, sign)
    assert get_dignity(planet, sign) == "Debilitated"


@pytest.mark.parametrize(
    "planet, sign",
    list(EXALTATION_SIGNS.items()),
)
def test_exaltation_sign_is_not_debilitation_sign(planet, sign):
    """A planet's exaltation sign is not its debilitation sign."""

    assert not is_debilitated(planet, sign)


# ============================================================
# Own Signs
# ============================================================


@pytest.mark.parametrize(
    "planet, signs",
    list(OWN_SIGNS.items()),
)
def test_is_own_sign(planet, signs):
    """Every configured own-sign relationship is recognized."""

    for sign in signs:
        assert is_own_sign(planet, sign)


@pytest.mark.parametrize(
    "planet, signs",
    list(OWN_SIGNS.items()),
)
def test_own_signs_are_exactly_the_configured_signs(planet, signs):
    """
    Own-sign detection must agree exactly with OWN_SIGNS.

    This deliberately does not assume that an own sign must have
    a particular final dignity because Moolatrikona and exaltation
    have higher priority in get_dignity().
    """

    for sign in SIGN_LORDS:
        expected = sign in signs
        assert is_own_sign(planet, sign) == expected


# ============================================================
# Moolatrikona
# ============================================================


@pytest.mark.parametrize(
    "planet, sign",
    list(MOOLATRIKONA_SIGNS.items()),
)
def test_is_moolatrikona(planet, sign):
    """Every configured Moolatrikona relationship is recognized."""

    assert is_moolatrikona(planet, sign)


def test_moolatrikona_detection_matches_mapping():
    """
    Moolatrikona detection must agree exactly with the configured
    MOOLATRIKONA_SIGNS mapping.
    """

    for planet in MOOLATRIKONA_SIGNS:
        for sign in SIGN_LORDS:
            expected = MOOLATRIKONA_SIGNS[planet] == sign
            assert is_moolatrikona(planet, sign) == expected


def test_moolatrikona_is_independent_of_own_sign():
    """
    Moolatrikona and own-sign status are separate classifications.

    The configured model intentionally contains cases such as
    Moon -> Taurus, where Taurus is Moolatrikona but is not listed
    as Moon's own sign.
    """

    assert is_moolatrikona("Moon", "Taurus")
    assert not is_own_sign("Moon", "Taurus")

    assert is_moolatrikona("Sun", "Leo")
    assert is_own_sign("Sun", "Leo")

    assert is_moolatrikona("Mars", "Aries")
    assert is_own_sign("Mars", "Aries")

    assert is_moolatrikona("Mercury", "Virgo")
    assert is_own_sign("Mercury", "Virgo")


# ============================================================
# Moolatrikona and dignity priority
# ============================================================


def test_moolatrikona_priority_over_own_sign():
    """
    Where Moolatrikona and own-sign mappings overlap, the final
    dignity is Moolatrikona unless a higher-priority dignity applies.
    """

    assert get_dignity("Sun", "Leo") == "Moolatrikona"
    assert get_dignity("Mars", "Aries") == "Moolatrikona"
    assert get_dignity("Mercury", "Virgo") == "Exalted"
    assert get_dignity("Jupiter", "Sagittarius") == "Moolatrikona"
    assert get_dignity("Venus", "Libra") == "Moolatrikona"
    assert get_dignity("Saturn", "Aquarius") == "Moolatrikona"


def test_moon_moolatrikona_is_overridden_by_exaltation():
    """
    Moon in Taurus is both configured as Moolatrikona and exalted.

    Exaltation has higher priority in get_dignity().
    """

    assert is_moolatrikona("Moon", "Taurus")
    assert is_exalted("Moon", "Taurus")
    assert get_dignity("Moon", "Taurus") == "Exalted"


def test_mercury_moolatrikona_is_overridden_by_exaltation():
    """
    Mercury in Virgo is both configured as Moolatrikona and exalted.

    Exaltation has higher priority in get_dignity().
    """

    assert is_moolatrikona("Mercury", "Virgo")
    assert is_exalted("Mercury", "Virgo")
    assert get_dignity("Mercury", "Virgo") == "Exalted"


# ============================================================
# Friendly Signs
# ============================================================


def _expected_relationship_dignity(planet, sign):
    """
    Calculate the expected relationship dignity from the actual
    natural relationship tables.

    This helper intentionally mirrors the relationship portion of
    astrology.dignity without reproducing the higher-priority
    exaltation/debilitation/Moolatrikona/own-sign checks.
    """

    sign_lord = SIGN_LORDS[sign]

    if sign_lord in NATURAL_FRIENDS.get(planet, ()):
        return "Friendly Sign"

    if sign_lord in NATURAL_ENEMIES.get(planet, ()):
        return "Enemy Sign"

    return "Neutral Sign"


def test_friendly_sign_relationships():
    """
    Every sign whose lord is configured as a natural friend should
    resolve to Friendly Sign when no higher-priority dignity applies.
    """

    checked = 0

    for planet in SIGN_LORDS.values():
        if planet not in NATURAL_FRIENDS:
            continue

        for sign, sign_lord in SIGN_LORDS.items():
            if sign_lord not in NATURAL_FRIENDS[planet]:
                continue

            if (
                EXALTATION_SIGNS.get(planet) == sign
                or DEBILITATION_SIGNS.get(planet) == sign
                or MOOLATRIKONA_SIGNS.get(planet) == sign
                or sign in OWN_SIGNS.get(planet, ())
            ):
                continue

            assert get_dignity(planet, sign) == "Friendly Sign"
            checked += 1

    assert checked > 0


# ============================================================
# Enemy Signs
# ============================================================


def test_enemy_sign_relationships():
    """
    Every sign whose lord is configured as a natural enemy should
    resolve to Enemy Sign when no higher-priority dignity applies.
    """

    checked = 0

    for planet in SIGN_LORDS.values():
        if planet not in NATURAL_ENEMIES:
            continue

        for sign, sign_lord in SIGN_LORDS.items():
            if sign_lord not in NATURAL_ENEMIES[planet]:
                continue

            if (
                EXALTATION_SIGNS.get(planet) == sign
                or DEBILITATION_SIGNS.get(planet) == sign
                or MOOLATRIKONA_SIGNS.get(planet) == sign
                or sign in OWN_SIGNS.get(planet, ())
            ):
                continue

            assert get_dignity(planet, sign) == "Enemy Sign"
            checked += 1

    assert checked > 0


# ============================================================
# Neutral Signs
# ============================================================


def test_neutral_sign_relationships():
    """
    Every sign whose lord is neither a configured natural friend
    nor a configured natural enemy should resolve to Neutral Sign,
    provided no higher-priority dignity applies.
    """

    checked = 0

    for planet in SIGN_LORDS.values():
        for sign, sign_lord in SIGN_LORDS.items():

            if sign_lord in NATURAL_FRIENDS.get(planet, ()):
                continue

            if sign_lord in NATURAL_ENEMIES.get(planet, ()):
                continue

            if (
                EXALTATION_SIGNS.get(planet) == sign
                or DEBILITATION_SIGNS.get(planet) == sign
                or MOOLATRIKONA_SIGNS.get(planet) == sign
                or sign in OWN_SIGNS.get(planet, ())
            ):
                continue

            assert get_dignity(planet, sign) == "Neutral Sign"
            checked += 1

    assert checked > 0


# ============================================================
# Direct relationship examples
# ============================================================


def test_known_friendly_relationships():
    """Representative configured friendly relationships."""

    assert get_dignity("Sun", "Cancer") == "Friendly Sign"
    assert get_dignity("Sun", "Sagittarius") == "Friendly Sign"

    assert get_dignity("Mars", "Leo") == "Friendly Sign"
    assert get_dignity("Mars", "Sagittarius") == "Friendly Sign"

    assert get_dignity("Jupiter", "Aries") == "Friendly Sign"

    assert get_dignity("Venus", "Gemini") == "Friendly Sign"
    assert get_dignity("Venus", "Capricorn") == "Friendly Sign"

    assert get_dignity("Saturn", "Gemini") == "Friendly Sign"


def test_known_enemy_relationships():
    """Representative configured enemy relationships."""

    assert get_dignity("Sun", "Taurus") == "Enemy Sign"
    assert get_dignity("Sun", "Capricorn") == "Enemy Sign"

    assert get_dignity("Mars", "Gemini") == "Enemy Sign"

    assert get_dignity("Mercury", "Cancer") == "Enemy Sign"

    assert get_dignity("Jupiter", "Gemini") == "Enemy Sign"

    assert get_dignity("Venus", "Leo") == "Enemy Sign"

    assert get_dignity("Saturn", "Leo") == "Enemy Sign"


# ============================================================
# Dignity priority
# ============================================================


def test_exaltation_has_highest_priority():
    """Exaltation must be returned before other classifications."""

    for planet, sign in EXALTATION_SIGNS.items():
        assert get_dignity(planet, sign) == "Exalted"


def test_debilitation_has_priority_over_relationship():
    """
    Debilitation must take priority over friendly/enemy/neutral
    relationship classification.
    """

    for planet, sign in DEBILITATION_SIGNS.items():
        assert get_dignity(planet, sign) == "Debilitated"


def test_moolatrikona_has_priority_over_own_sign_when_not_exalted():
    """
    Moolatrikona takes priority over Own Sign when the sign is not
    simultaneously an exaltation sign.
    """

    for planet, sign in MOOLATRIKONA_SIGNS.items():

        if EXALTATION_SIGNS.get(planet) == sign:
            assert get_dignity(planet, sign) == "Exalted"
            continue

        assert sign in OWN_SIGNS.get(planet, ())
        assert get_dignity(planet, sign) == "Moolatrikona"


# ============================================================
# Sign Lords
# ============================================================


@pytest.mark.parametrize(
    "sign,lord",
    [
        ("Aries", "Mars"),
        ("Taurus", "Venus"),
        ("Gemini", "Mercury"),
        ("Cancer", "Moon"),
        ("Leo", "Sun"),
        ("Virgo", "Mercury"),
        ("Libra", "Venus"),
        ("Scorpio", "Mars"),
        ("Sagittarius", "Jupiter"),
        ("Capricorn", "Saturn"),
        ("Aquarius", "Saturn"),
        ("Pisces", "Jupiter"),
    ],
)
def test_sign_lords(sign, lord):
    """Every zodiac sign has the configured classical lord."""

    assert SIGN_LORDS[sign] == lord


def test_all_twelve_signs_have_lords():
    """The sign-lord mapping contains exactly twelve signs."""

    assert len(SIGN_LORDS) == 12


# ============================================================
# Mapping integrity
# ============================================================


def test_exaltation_mapping_contains_seven_planets():
    """Seven classical planets must have exaltation signs."""

    assert len(EXALTATION_SIGNS) == 7


def test_debilitation_mapping_contains_seven_planets():
    """Seven classical planets must have debilitation signs."""

    assert len(DEBILITATION_SIGNS) == 7


def test_own_sign_mapping_contains_seven_planets():
    """Seven classical planets must have own-sign mappings."""

    assert len(OWN_SIGNS) == 7


def test_moolatrikona_mapping_contains_seven_planets():
    """Seven classical planets must have Moolatrikona mappings."""

    assert len(MOOLATRIKONA_SIGNS) == 7


def test_all_dignity_planets_are_consistent():
    """
    All four primary dignity mappings should refer to the same
    seven classical planets.
    """

    expected_planets = set(EXALTATION_SIGNS)

    assert set(DEBILITATION_SIGNS) == expected_planets
    assert set(OWN_SIGNS) == expected_planets
    assert set(MOOLATRIKONA_SIGNS) == expected_planets


def test_all_dignity_signs_are_valid_signs():
    """All configured dignity signs must exist in SIGN_LORDS."""

    valid_signs = set(SIGN_LORDS)

    for sign in EXALTATION_SIGNS.values():
        assert sign in valid_signs

    for sign in DEBILITATION_SIGNS.values():
        assert sign in valid_signs

    for signs in OWN_SIGNS.values():
        for sign in signs:
            assert sign in valid_signs

    for sign in MOOLATRIKONA_SIGNS.values():
        assert sign in valid_signs


# ============================================================
# Boolean helper behavior
# ============================================================


@pytest.mark.parametrize(
    "planet, sign",
    list(EXALTATION_SIGNS.items()),
)
def test_exalted_helper_matches_mapping(planet, sign):
    """is_exalted() must agree with EXALTATION_SIGNS."""

    assert is_exalted(planet, sign)


@pytest.mark.parametrize(
    "planet, sign",
    list(DEBILITATION_SIGNS.items()),
)
def test_debilitated_helper_matches_mapping(planet, sign):
    """is_debilitated() must agree with DEBILITATION_SIGNS."""

    assert is_debilitated(planet, sign)


@pytest.mark.parametrize(
    "planet, signs",
    list(OWN_SIGNS.items()),
)
def test_own_sign_helper_matches_mapping(planet, signs):
    """is_own_sign() must agree with OWN_SIGNS."""

    for sign in signs:
        assert is_own_sign(planet, sign)


@pytest.mark.parametrize(
    "planet, sign",
    list(MOOLATRIKONA_SIGNS.items()),
)
def test_moolatrikona_helper_matches_mapping(planet, sign):
    """is_moolatrikona() must agree with MOOLATRIKONA_SIGNS."""

    assert is_moolatrikona(planet, sign)


# ============================================================
# Unknown planet / sign validation
# ============================================================


def test_get_dignity_unknown_planet():
    """Unknown planets should raise ValueError."""

    with pytest.raises(ValueError, match="Unknown planet"):
        get_dignity("Rahu", "Aries")


def test_get_dignity_unknown_sign():
    """Unknown signs should raise ValueError."""

    with pytest.raises(ValueError, match="Unknown sign"):
        get_dignity("Sun", "Atlantis")


def test_unknown_planet_boolean_helpers_return_false():
    """
    Boolean helper functions should safely return False for an
    unknown planet.
    """

    assert not is_exalted("Rahu", "Aries")
    assert not is_debilitated("Rahu", "Aries")
    assert not is_own_sign("Rahu", "Aries")
    assert not is_moolatrikona("Rahu", "Aries")


# ============================================================
# Final consistency check
# ============================================================


def test_get_dignity_returns_valid_classification():
    """
    Every classical planet/sign combination must produce one of
    the seven supported dignity classifications.
    """

    valid_dignities = {
        "Exalted",
        "Debilitated",
        "Moolatrikona",
        "Own Sign",
        "Friendly Sign",
        "Enemy Sign",
        "Neutral Sign",
    }

    planets = set(EXALTATION_SIGNS)

    for planet in planets:
        for sign in SIGN_LORDS:
            assert get_dignity(planet, sign) in valid_dignities