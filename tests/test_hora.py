"""
tests/test_hora.py

Comprehensive tests for the Parashari Hora (D2) calculation.

Hora rules:
    - Each zodiac sign is divided into two equal 15° Horas.
    - Odd signs:
        First Hora  -> Leo
        Second Hora -> Cancer
    - Even signs:
        First Hora  -> Cancer
        Second Hora -> Leo

The tests verify:
    - Every zodiac sign
    - Both Hora divisions
    - Exact 15° boundary
    - Exact sign boundaries
    - Zodiac wraparound
    - Negative longitude normalization
    - Floating-point boundary behavior
    - Result structure and repeatability

Compatible with Python 3.9.
"""

import pytest

from astronomy.hora import hora
from models.zodiac import ZodiacSign


# ============================================================
# SIGN DATA
# ============================================================

ODD_SIGNS = [
    (
        "Aries",
        0.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
    (
        "Gemini",
        60.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
    (
        "Leo",
        120.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
    (
        "Libra",
        180.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
    (
        "Sagittarius",
        240.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
    (
        "Aquarius",
        300.0,
        ZodiacSign.LEO,
        ZodiacSign.CANCER,
    ),
]


EVEN_SIGNS = [
    (
        "Taurus",
        30.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
    (
        "Cancer",
        90.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
    (
        "Virgo",
        150.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
    (
        "Scorpio",
        210.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
    (
        "Capricorn",
        270.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
    (
        "Pisces",
        330.0,
        ZodiacSign.CANCER,
        ZodiacSign.LEO,
    ),
]


# ============================================================
# BASIC ODD-SIGN TESTS
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    ODD_SIGNS,
)
def test_odd_sign_first_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Every odd zodiac sign must assign its first 15°
    to Leo.
    """

    result = hora(
        sign_start + 5.0
    )

    assert result.sign == first_sign
    assert result.division == 1


@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    ODD_SIGNS,
)
def test_odd_sign_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Every odd zodiac sign must assign its second 15°
    to Cancer.
    """

    result = hora(
        sign_start + 20.0
    )

    assert result.sign == second_sign
    assert result.division == 2


# ============================================================
# BASIC EVEN-SIGN TESTS
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    EVEN_SIGNS,
)
def test_even_sign_first_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Every even zodiac sign must assign its first 15°
    to Cancer.
    """

    result = hora(
        sign_start + 5.0
    )

    assert result.sign == first_sign
    assert result.division == 1


@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    EVEN_SIGNS,
)
def test_even_sign_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Every even zodiac sign must assign its second 15°
    to Leo.
    """

    result = hora(
        sign_start + 20.0
    )

    assert result.sign == second_sign
    assert result.division == 2


# ============================================================
# EXACT 15-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    ODD_SIGNS,
)
def test_odd_sign_exact_15_degree_starts_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Exactly 15° belongs to the second Hora.

    For odd signs the second Hora is Cancer.
    """

    result = hora(
        sign_start + 15.0
    )

    assert result.sign == second_sign
    assert result.division == 2


@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    EVEN_SIGNS,
)
def test_even_sign_exact_15_degree_starts_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    Exactly 15° belongs to the second Hora.

    For even signs the second Hora is Leo.
    """

    result = hora(
        sign_start + 15.0
    )

    assert result.sign == second_sign
    assert result.division == 2


# ============================================================
# JUST BEFORE 15-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    ODD_SIGNS,
)
def test_odd_sign_just_before_15_remains_first_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    A longitude infinitesimally below 15° remains
    in the first Hora.
    """

    result = hora(
        sign_start + 14.999999
    )

    assert result.sign == first_sign
    assert result.division == 1


@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    EVEN_SIGNS,
)
def test_even_sign_just_before_15_remains_first_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    A longitude infinitesimally below 15° remains
    in the first Hora.
    """

    result = hora(
        sign_start + 14.999999
    )

    assert result.sign == first_sign
    assert result.division == 1


# ============================================================
# JUST AFTER 15-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    ODD_SIGNS,
)
def test_odd_sign_just_after_15_is_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    A longitude infinitesimally above 15° belongs
    to the second Hora.
    """

    result = hora(
        sign_start + 15.000001
    )

    assert result.sign == second_sign
    assert result.division == 2


@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign",
    EVEN_SIGNS,
)
def test_even_sign_just_after_15_is_second_hora(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
):
    """
    A longitude infinitesimally above 15° belongs
    to the second Hora.
    """

    result = hora(
        sign_start + 15.000001
    )

    assert result.sign == second_sign
    assert result.division == 2


# ============================================================
# SIGN BOUNDARIES
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.LEO),
        (30.0, ZodiacSign.CANCER),
        (60.0, ZodiacSign.LEO),
        (90.0, ZodiacSign.CANCER),
        (120.0, ZodiacSign.LEO),
        (150.0, ZodiacSign.CANCER),
        (180.0, ZodiacSign.LEO),
        (210.0, ZodiacSign.CANCER),
        (240.0, ZodiacSign.LEO),
        (270.0, ZodiacSign.CANCER),
        (300.0, ZodiacSign.LEO),
        (330.0, ZodiacSign.CANCER),
    ],
)
def test_exact_sign_boundary_starts_first_hora(
    sign_start,
    expected_sign,
):
    """
    Every exact 30° sign boundary begins the first Hora
    of the new sign.
    """

    result = hora(
        sign_start
    )

    assert result.sign == expected_sign
    assert result.division == 1


# ============================================================
# LAST POINT OF EACH SIGN
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.CANCER),
        (30.0, ZodiacSign.LEO),
        (60.0, ZodiacSign.CANCER),
        (90.0, ZodiacSign.LEO),
        (120.0, ZodiacSign.CANCER),
        (150.0, ZodiacSign.LEO),
        (180.0, ZodiacSign.CANCER),
        (210.0, ZodiacSign.LEO),
        (240.0, ZodiacSign.CANCER),
        (270.0, ZodiacSign.LEO),
        (300.0, ZodiacSign.CANCER),
        (330.0, ZodiacSign.LEO),
    ],
)
def test_near_end_of_each_sign_is_second_hora(
    sign_start,
    expected_sign,
):
    """
    A longitude immediately below the next sign boundary
    must remain in the second Hora of the current sign.
    """

    result = hora(
        sign_start + 29.999999
    )

    assert result.sign == expected_sign
    assert result.division == 2


# ============================================================
# CLASSICAL RULE COVERAGE
# ============================================================

def test_all_odd_signs_follow_leo_then_cancer():
    """
    Explicitly verify the complete odd-sign rule.
    """

    for _, sign_start, first_sign, second_sign in ODD_SIGNS:

        first = hora(
            sign_start + 1.0
        )

        second = hora(
            sign_start + 16.0
        )

        assert first.sign == ZodiacSign.LEO
        assert first.division == 1

        assert second.sign == ZodiacSign.CANCER
        assert second.division == 2

        assert first.sign == first_sign
        assert second.sign == second_sign


def test_all_even_signs_follow_cancer_then_leo():
    """
    Explicitly verify the complete even-sign rule.
    """

    for _, sign_start, first_sign, second_sign in EVEN_SIGNS:

        first = hora(
            sign_start + 1.0
        )

        second = hora(
            sign_start + 16.0
        )

        assert first.sign == ZodiacSign.CANCER
        assert first.division == 1

        assert second.sign == ZodiacSign.LEO
        assert second.division == 2

        assert first.sign == first_sign
        assert second.sign == second_sign


# ============================================================
# ZERO DEGREE
# ============================================================

def test_zero_degree_aries():
    """
    0° Aries is the beginning of the first Hora
    of an odd sign and therefore maps to Leo.
    """

    result = hora(
        0.0
    )

    assert result.sign == ZodiacSign.LEO
    assert result.division == 1


# ============================================================
# FINAL LONGITUDE
# ============================================================

def test_last_valid_longitude():
    """
    A longitude just below 360° is still inside Pisces
    and therefore belongs to its second Hora, Leo.
    """

    result = hora(
        359.999999
    )

    assert result.sign == ZodiacSign.LEO
    assert result.division == 2


# ============================================================
# POSITIVE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_sign,expected_division",
    [
        (
            360.0,
            ZodiacSign.LEO,
            1,
        ),
        (
            365.0,
            ZodiacSign.LEO,
            1,
        ),
        (
            390.0,
            ZodiacSign.CANCER,
            1,
        ),
        (
            420.0,
            ZodiacSign.LEO,
            1,
        ),
        (
            725.0,
            ZodiacSign.LEO,
            1,
        ),
    ],
)
def test_positive_longitude_wraparound(
    longitude,
    expected_sign,
    expected_division,
):
    """
    Longitudes above 360° must be normalized modulo 360°.
    """

    result = hora(
        longitude
    )

    assert result.sign == expected_sign
    assert result.division == expected_division


# ============================================================
# NEGATIVE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_sign,expected_division",
    [
        (
            -1.0,
            ZodiacSign.LEO,
            2,
        ),
        (
            -5.0,
            ZodiacSign.LEO,
            2,
        ),
        (
            -15.0,
            ZodiacSign.LEO,
            2,
        ),
        (
            -30.0,
            ZodiacSign.CANCER,
            1,
        ),
        (
            -45.0,
            ZodiacSign.CANCER,
            2,
        ),
        (
            -60.0,
            ZodiacSign.LEO,
            1,
        ),
    ],
)
def test_negative_longitude_wraparound(
    longitude,
    expected_sign,
    expected_division,
):
    """
    Negative longitudes are normalized modulo 360° before
    applying the Parashari Hora rules.

    Examples:

        -15° -> 345° -> Pisces -> second Hora -> Leo
        -30° -> 330° -> Pisces -> first Hora -> Cancer
        -45° -> 315° -> Aquarius -> second Hora -> Cancer
        -60° -> 300° -> Aquarius -> first Hora -> Leo
    """

    result = hora(
        longitude
    )

    assert result.sign == expected_sign
    assert result.division == expected_division


# ============================================================
# RESULT STRUCTURE
# ============================================================

def test_result_always_contains_valid_hora_division():
    """
    Hora division must always be either 1 or 2.
    """

    longitudes = [
        0.0,
        1.0,
        14.999999,
        15.0,
        15.000001,
        29.999999,
        30.0,
        45.0,
        90.0,
        180.0,
        270.0,
        359.999999,
        360.0,
        -1.0,
        -90.0,
        720.0,
    ]

    for longitude in longitudes:

        result = hora(
            longitude
        )

        assert result.division in {
            1,
            2,
        }


def test_result_hora_sign_is_always_leo_or_cancer():
    """
    Classical Parashari Hora uses only Leo and Cancer
    as the D2 signs.
    """

    longitudes = [
        -720.0,
        -359.999,
        -30.0,
        -1.0,
        0.0,
        14.999999,
        15.0,
        29.999999,
        30.0,
        44.999999,
        45.0,
        59.999999,
        60.0,
        90.0,
        150.0,
        210.0,
        270.0,
        330.0,
        359.999999,
        360.0,
        720.0,
    ]

    for longitude in longitudes:

        result = hora(
            longitude
        )

        assert result.sign in {
            ZodiacSign.LEO,
            ZodiacSign.CANCER,
        }


# ============================================================
# REPEATABILITY
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        0.0,
        5.0,
        15.0,
        20.0,
        30.0,
        45.0,
        90.0,
        135.0,
        180.0,
        225.0,
        270.0,
        315.0,
        359.999999,
        -5.0,
        365.0,
    ],
)
def test_hora_is_repeatable(longitude):
    """
    Hora calculation must be deterministic.
    """

    first = hora(
        longitude
    )

    second = hora(
        longitude
    )

    assert first == second