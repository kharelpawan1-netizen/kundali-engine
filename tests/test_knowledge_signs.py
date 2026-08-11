"""
tests/test_knowledge_signs.py

Tests for the permanent Rashi (zodiac-sign) knowledge database.

Compatible with Python 3.9.
"""

from knowledge.signs import (
    SIGNS,
    SignFacts,
    all_signs,
    get_sign,
)
from models.sign import Sign


# =========================================================
# Database structure
# =========================================================


def test_signs_dictionary_exists():
    """The sign knowledge database must exist."""

    assert isinstance(SIGNS, dict)


def test_contains_twelve_signs():
    """The database must contain exactly the twelve Rashis."""

    assert len(SIGNS) == 12


def test_every_key_is_sign():
    """Every database key must be a Sign enum member."""

    assert all(isinstance(key, Sign) for key in SIGNS)


def test_every_value_is_signfacts():
    """Every database value must be a SignFacts instance."""

    assert all(isinstance(value, SignFacts) for value in SIGNS.values())


def test_dictionary_contains_all_signs():
    """The database must contain every Sign enum member."""

    assert set(SIGNS.keys()) == set(Sign)


# =========================================================
# get_sign()
# =========================================================


def test_get_sign_returns_signfacts():
    """get_sign() must return a SignFacts object."""

    assert isinstance(get_sign(Sign.ARIES), SignFacts)


def test_get_sign_for_aries():
    """Aries knowledge must be retrievable correctly."""

    aries = get_sign(Sign.ARIES)

    assert aries.sign is Sign.ARIES
    assert aries.sanskrit_name == "Mesha"
    assert aries.lord == "Mars"


def test_get_sign_for_taurus():
    """Taurus knowledge must be retrievable correctly."""

    taurus = get_sign(Sign.TAURUS)

    assert taurus.sign is Sign.TAURUS
    assert taurus.sanskrit_name == "Vrishabha"
    assert taurus.lord == "Venus"


def test_get_sign_for_gemini():
    """Gemini knowledge must be retrievable correctly."""

    gemini = get_sign(Sign.GEMINI)

    assert gemini.sign is Sign.GEMINI
    assert gemini.sanskrit_name == "Mithuna"
    assert gemini.lord == "Mercury"


def test_get_sign_for_cancer():
    """Cancer knowledge must be retrievable correctly."""

    cancer = get_sign(Sign.CANCER)

    assert cancer.sign is Sign.CANCER
    assert cancer.sanskrit_name == "Karka"
    assert cancer.lord == "Moon"


def test_get_sign_for_leo():
    """Leo knowledge must be retrievable correctly."""

    leo = get_sign(Sign.LEO)

    assert leo.sign is Sign.LEO
    assert leo.sanskrit_name == "Simha"
    assert leo.lord == "Sun"


def test_get_sign_for_virgo():
    """Virgo knowledge must be retrievable correctly."""

    virgo = get_sign(Sign.VIRGO)

    assert virgo.sign is Sign.VIRGO
    assert virgo.sanskrit_name == "Kanya"
    assert virgo.lord == "Mercury"


def test_get_sign_for_libra():
    """Libra knowledge must be retrievable correctly."""

    libra = get_sign(Sign.LIBRA)

    assert libra.sign is Sign.LIBRA
    assert libra.sanskrit_name == "Tula"
    assert libra.lord == "Venus"


def test_get_sign_for_scorpio():
    """Scorpio knowledge must be retrievable correctly."""

    scorpio = get_sign(Sign.SCORPIO)

    assert scorpio.sign is Sign.SCORPIO
    assert scorpio.sanskrit_name == "Vrishchika"
    assert scorpio.lord == "Mars"


def test_get_sign_for_sagittarius():
    """Sagittarius knowledge must be retrievable correctly."""

    sagittarius = get_sign(Sign.SAGITTARIUS)

    assert sagittarius.sign is Sign.SAGITTARIUS
    assert sagittarius.sanskrit_name == "Dhanu"
    assert sagittarius.lord == "Jupiter"


def test_get_sign_for_capricorn():
    """Capricorn knowledge must be retrievable correctly."""

    capricorn = get_sign(Sign.CAPRICORN)

    assert capricorn.sign is Sign.CAPRICORN
    assert capricorn.sanskrit_name == "Makara"
    assert capricorn.lord == "Saturn"


def test_get_sign_for_aquarius():
    """Aquarius knowledge must be retrievable correctly."""

    aquarius = get_sign(Sign.AQUARIUS)

    assert aquarius.sign is Sign.AQUARIUS
    assert aquarius.sanskrit_name == "Kumbha"
    assert aquarius.lord == "Saturn"


def test_get_sign_for_pisces():
    """Pisces knowledge must be retrievable correctly."""

    pisces = get_sign(Sign.PISCES)

    assert pisces.sign is Sign.PISCES
    assert pisces.sanskrit_name == "Meena"
    assert pisces.lord == "Jupiter"


# =========================================================
# all_signs()
# =========================================================


def test_all_signs_returns_all_objects():
    """all_signs() must return all twelve SignFacts objects."""

    signs = all_signs()

    assert isinstance(signs, tuple)
    assert len(signs) == 12
    assert all(isinstance(sign, SignFacts) for sign in signs)


def test_all_signs_contains_every_sign():
    """all_signs() must contain knowledge for every Rashi."""

    signs = all_signs()

    assert {sign.sign for sign in signs} == set(Sign)


# =========================================================
# Sign identity consistency
# =========================================================


def test_sign_names_are_unique():
    """Every SignFacts object must represent a unique Sign."""

    signs = all_signs()

    names = [sign.sign for sign in signs]

    assert len(names) == len(set(names))


def test_sanskrit_names_are_unique():
    """Every Rashi must have a unique Sanskrit name."""

    signs = all_signs()

    names = [sign.sanskrit_name for sign in signs]

    assert len(names) == len(set(names))


# =========================================================
# Core sign classifications
# =========================================================


def test_sign_elements_are_valid():
    """All signs must use one of the four classical elements."""

    valid_elements = {
        "Fire",
        "Earth",
        "Air",
        "Water",
    }

    assert all(
        sign.element in valid_elements
        for sign in all_signs()
    )


def test_sign_modalities_are_valid():
    """All signs must use a valid modality."""

    valid_modalities = {
        "Movable",
        "Fixed",
        "Dual",
    }

    assert all(
        sign.modality in valid_modalities
        for sign in all_signs()
    )


def test_sign_genders_are_valid():
    """All signs must have a valid gender classification."""

    valid_genders = {
        "Male",
        "Female",
    }

    assert all(
        sign.gender in valid_genders
        for sign in all_signs()
    )


def test_sign_gunas_are_valid():
    """All signs must use one of the three gunas."""

    valid_gunas = {
        "Sattva",
        "Rajas",
        "Tamas",
    }

    assert all(
        sign.guna in valid_gunas
        for sign in all_signs()
    )


# =========================================================
# Sign lordship
# =========================================================


def test_all_signs_have_lords():
    """Every Rashi must have a planetary lord."""

    assert all(
        isinstance(sign.lord, str) and sign.lord
        for sign in all_signs()
    )


def test_sign_lords_are_valid_navagraha_names():
    """Sign lords must belong to the classical planetary set."""

    valid_lords = {
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
    }

    assert all(
        sign.lord in valid_lords
        for sign in all_signs()
    )


def test_expected_sign_lordships():
    """The twelve Rashis must have the expected traditional lords."""

    expected_lords = {
        Sign.ARIES: "Mars",
        Sign.TAURUS: "Venus",
        Sign.GEMINI: "Mercury",
        Sign.CANCER: "Moon",
        Sign.LEO: "Sun",
        Sign.VIRGO: "Mercury",
        Sign.LIBRA: "Venus",
        Sign.SCORPIO: "Mars",
        Sign.SAGITTARIUS: "Jupiter",
        Sign.CAPRICORN: "Saturn",
        Sign.AQUARIUS: "Saturn",
        Sign.PISCES: "Jupiter",
    }

    for sign, expected_lord in expected_lords.items():
        assert get_sign(sign).lord == expected_lord


# =========================================================
# Knowledge completeness
# =========================================================


def test_every_sign_has_keywords():
    """Every Rashi must have interpretive keywords."""

    assert all(
        isinstance(sign.keywords, tuple)
        and len(sign.keywords) > 0
        for sign in all_signs()
    )


def test_every_sign_has_significations():
    """Every Rashi must have natural significations."""

    assert all(
        isinstance(sign.significations, tuple)
        and len(sign.significations) > 0
        for sign in all_signs()
    )


def test_every_sign_has_body_part():
    """Every Rashi must have a body-part correspondence."""

    assert all(
        isinstance(sign.body_part, str)
        and sign.body_part
        for sign in all_signs()
    )


def test_every_sign_has_direction():
    """Every Rashi must have a directional correspondence."""

    assert all(
        isinstance(sign.direction, str)
        and sign.direction
        for sign in all_signs()
    )


# =========================================================
# Immutability
# =========================================================


def test_signfacts_are_immutable():
    """SignFacts must be immutable because it is frozen."""

    aries = get_sign(Sign.ARIES)

    try:
        aries.lord = "Jupiter"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "SignFacts must be immutable."
        )