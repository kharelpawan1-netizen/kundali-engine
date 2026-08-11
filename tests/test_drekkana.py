"""
tests/test_drekkana.py

Comprehensive tests for Parashari Drekkana (D3).

Classical Parashari Drekkana rules:

Each zodiac sign is divided into three equal parts of 10°.

For a sign numbered n:

    First Drekkana:
        The sign itself.

    Second Drekkana:
        The 5th sign from the sign.

    Third Drekkana:
        The 9th sign from the sign.

Therefore:

    Part 1 -> sign n
    Part 2 -> sign n + 4
    Part 3 -> sign n + 8

The resulting Drekkana sign is always one of the twelve
zodiac signs, with zodiacal wraparound.

The returned degree within the Drekkana sign is:

    local_degree = (degree_within_birth_sign % 10) * 3

because each 10° source division maps to a complete
30° zodiac sign.

The tests verify:

    - All twelve zodiac signs
    - All three Drekkana divisions
    - Exact 10° boundary
    - Exact 20° boundary
    - Exact sign boundaries
    - Final point of each Drekkana
    - Positive longitude wraparound
    - Negative longitude normalization
    - Large positive and negative longitudes
    - Floating-point boundary behavior
    - Degree mapping
    - Result structure
    - Classical sign mapping
    - Repeatability

Compatible with Python 3.9.
"""

import pytest

from astronomy.drekkana import drekkana
from models.varga_position import VargaPosition
from models.zodiac import ZodiacSign


# ============================================================
# SIGN DATA
# ============================================================

ALL_SIGNS = [
    (
        ZodiacSign.ARIES,
        0.0,
        ZodiacSign.ARIES,
        ZodiacSign.LEO,
        ZodiacSign.SAGITTARIUS,
    ),
    (
        ZodiacSign.TAURUS,
        30.0,
        ZodiacSign.TAURUS,
        ZodiacSign.VIRGO,
        ZodiacSign.CAPRICORN,
    ),
    (
        ZodiacSign.GEMINI,
        60.0,
        ZodiacSign.GEMINI,
        ZodiacSign.LIBRA,
        ZodiacSign.AQUARIUS,
    ),
    (
        ZodiacSign.CANCER,
        90.0,
        ZodiacSign.CANCER,
        ZodiacSign.SCORPIO,
        ZodiacSign.PISCES,
    ),
    (
        ZodiacSign.LEO,
        120.0,
        ZodiacSign.LEO,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.ARIES,
    ),
    (
        ZodiacSign.VIRGO,
        150.0,
        ZodiacSign.VIRGO,
        ZodiacSign.CAPRICORN,
        ZodiacSign.TAURUS,
    ),
    (
        ZodiacSign.LIBRA,
        180.0,
        ZodiacSign.LIBRA,
        ZodiacSign.AQUARIUS,
        ZodiacSign.GEMINI,
    ),
    (
        ZodiacSign.SCORPIO,
        210.0,
        ZodiacSign.SCORPIO,
        ZodiacSign.PISCES,
        ZodiacSign.CANCER,
    ),
    (
        ZodiacSign.SAGITTARIUS,
        240.0,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.ARIES,
        ZodiacSign.LEO,
    ),
    (
        ZodiacSign.CAPRICORN,
        270.0,
        ZodiacSign.CAPRICORN,
        ZodiacSign.TAURUS,
        ZodiacSign.VIRGO,
    ),
    (
        ZodiacSign.AQUARIUS,
        300.0,
        ZodiacSign.AQUARIUS,
        ZodiacSign.GEMINI,
        ZodiacSign.LIBRA,
    ),
    (
        ZodiacSign.PISCES,
        330.0,
        ZodiacSign.PISCES,
        ZodiacSign.CANCER,
        ZodiacSign.SCORPIO,
    ),
]


# ============================================================
# BASIC FIRST DREKKANA TESTS
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_first_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    The first 10° of every sign belongs to the sign itself.
    """

    result = drekkana(
        sign_start + 5.0
    )

    assert result.sign is first_sign
    assert result.degree_in_sign == 15.0


# ============================================================
# BASIC SECOND DREKKANA TESTS
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_second_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    The second 10° of a sign belongs to the 5th sign
    from the source sign.
    """

    result = drekkana(
        sign_start + 15.0
    )

    assert result.sign is second_sign
    assert result.degree_in_sign == 15.0


# ============================================================
# BASIC THIRD DREKKANA TESTS
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_third_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    The third 10° of a sign belongs to the 9th sign
    from the source sign.
    """

    result = drekkana(
        sign_start + 25.0
    )

    assert result.sign is third_sign
    assert result.degree_in_sign == 15.0


# ============================================================
# EXACT 10-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_exact_10_degree_starts_second_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    Exactly 10° belongs to the second Drekkana.
    """

    result = drekkana(
        sign_start + 10.0
    )

    assert result.sign is second_sign
    assert result.degree_in_sign == 0.0


# ============================================================
# EXACT 20-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_exact_20_degree_starts_third_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    Exactly 20° belongs to the third Drekkana.
    """

    result = drekkana(
        sign_start + 20.0
    )

    assert result.sign is third_sign
    assert result.degree_in_sign == 0.0


# ============================================================
# JUST BEFORE 10-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_just_before_10_degree_remains_first_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    A longitude immediately below 10° remains in the
    first Drekkana.
    """

    result = drekkana(
        sign_start + 9.999999
    )

    assert result.sign is first_sign
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


# ============================================================
# JUST AFTER 10-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_just_after_10_degree_is_second_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    A longitude immediately above 10° belongs to the
    second Drekkana.
    """

    result = drekkana(
        sign_start + 10.000001
    )

    assert result.sign is second_sign
    assert result.degree_in_sign == pytest.approx(
        0.000003,
        abs=1e-9,
    )


# ============================================================
# JUST BEFORE 20-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_just_before_20_degree_remains_second_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    A longitude immediately below 20° remains in the
    second Drekkana.
    """

    result = drekkana(
        sign_start + 19.999999
    )

    assert result.sign is second_sign
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


# ============================================================
# JUST AFTER 20-DEGREE BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_name,sign_start,first_sign,second_sign,third_sign",
    ALL_SIGNS,
)
def test_just_after_20_degree_is_third_drekkana(
    sign_name,
    sign_start,
    first_sign,
    second_sign,
    third_sign,
):
    """
    A longitude immediately above 20° belongs to the
    third Drekkana.
    """

    result = drekkana(
        sign_start + 20.000001
    )

    assert result.sign is third_sign
    assert result.degree_in_sign == pytest.approx(
        0.000003,
        abs=1e-9,
    )


# ============================================================
# EXACT SIGN BOUNDARIES
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.ARIES),
        (30.0, ZodiacSign.TAURUS),
        (60.0, ZodiacSign.GEMINI),
        (90.0, ZodiacSign.CANCER),
        (120.0, ZodiacSign.LEO),
        (150.0, ZodiacSign.VIRGO),
        (180.0, ZodiacSign.LIBRA),
        (210.0, ZodiacSign.SCORPIO),
        (240.0, ZodiacSign.SAGITTARIUS),
        (270.0, ZodiacSign.CAPRICORN),
        (300.0, ZodiacSign.AQUARIUS),
        (330.0, ZodiacSign.PISCES),
    ],
)
def test_exact_sign_boundary_starts_first_drekkana(
    sign_start,
    expected_sign,
):
    """
    Every exact 30° sign boundary begins the first
    Drekkana of the new zodiac sign.
    """

    result = drekkana(
        sign_start
    )

    assert result.sign is expected_sign
    assert result.degree_in_sign == 0.0


# ============================================================
# LAST POINT OF EACH SIGN
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.SAGITTARIUS),
        (30.0, ZodiacSign.CAPRICORN),
        (60.0, ZodiacSign.AQUARIUS),
        (90.0, ZodiacSign.PISCES),
        (120.0, ZodiacSign.ARIES),
        (150.0, ZodiacSign.TAURUS),
        (180.0, ZodiacSign.GEMINI),
        (210.0, ZodiacSign.CANCER),
        (240.0, ZodiacSign.LEO),
        (270.0, ZodiacSign.VIRGO),
        (300.0, ZodiacSign.LIBRA),
        (330.0, ZodiacSign.SCORPIO),
    ],
)
def test_near_end_of_each_sign_is_third_drekkana(
    sign_start,
    expected_sign,
):
    """
    A longitude immediately below the next sign boundary
    must remain in the third Drekkana of the current sign.
    """

    result = drekkana(
        sign_start + 29.999999
    )

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


# ============================================================
# DEGREE MAPPING
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_degree",
    [
        (0.0, 0.0),
        (1.0, 3.0),
        (2.5, 7.5),
        (5.0, 15.0),
        (7.5, 22.5),
        (9.999999, 29.999997),
        (10.0, 0.0),
        (12.5, 7.5),
        (15.0, 15.0),
        (17.5, 22.5),
        (19.999999, 29.999997),
        (20.0, 0.0),
        (22.5, 7.5),
        (25.0, 15.0),
        (27.5, 22.5),
        (29.999999, 29.999997),
    ],
)
def test_degree_mapping(
    longitude,
    expected_degree,
):
    """
    Verify that each 10° source Drekkana maps linearly
    to 30° of the destination sign.
    """

    result = drekkana(
        longitude
    )

    assert result.degree_in_sign == pytest.approx(
        expected_degree,
        abs=1e-9,
    )


# ============================================================
# POSITIVE LONGITUDE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_sign,expected_degree",
    [
        (
            360.0,
            ZodiacSign.ARIES,
            0.0,
        ),
        (
            365.0,
            ZodiacSign.ARIES,
            15.0,
        ),
        (
            390.0,
            ZodiacSign.TAURUS,
            0.0,
        ),
        (
            420.0,
            ZodiacSign.GEMINI,
            0.0,
        ),
        (
            725.0,
            ZodiacSign.ARIES,
            15.0,
        ),
        (
            750.0,
            ZodiacSign.TAURUS,
            0.0,
        ),
    ],
)
def test_positive_longitude_wraparound(
    longitude,
    expected_sign,
    expected_degree,
):
    """
    Longitudes above 360° must be normalized modulo 360°.
    """

    result = drekkana(
        longitude
    )

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(
        expected_degree,
        abs=1e-9,
    )


# ============================================================
# NEGATIVE LONGITUDE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_sign,expected_degree",
    [
        (
            -1.0,
            ZodiacSign.SCORPIO,
            27.0,
        ),
        (
            -5.0,
            ZodiacSign.SCORPIO,
            15.0,
        ),
        (
            -10.0,
            ZodiacSign.SCORPIO,
            0.0,
        ),
        (
            -15.0,
            ZodiacSign.CANCER,
            15.0,
        ),
        (
            -20.0,
            ZodiacSign.CANCER,
            0.0,
        ),
        (
            -30.0,
            ZodiacSign.PISCES,
            0.0,
        ),
        (
            -45.0,
            ZodiacSign.GEMINI,
            15.0,
        ),
        (
            -60.0,
            ZodiacSign.AQUARIUS,
            0.0,
        ),
    ],
)
def test_negative_longitude_wraparound(
    longitude,
    expected_sign,
    expected_degree,
):
    """
    Negative longitudes must be normalized modulo 360°.

    Examples:

        -1°  -> 359° Pisces
             -> third Drekkana
             -> Scorpio 27°

        -30° -> 330° Pisces
             -> first Drekkana
             -> Pisces 0°

        -60° -> 300° Aquarius
             -> first Drekkana
             -> Aquarius 0°
    """

    result = drekkana(
        longitude
    )

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(
        expected_degree,
        abs=1e-9,
    )


# ============================================================
# LARGE POSITIVE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        720.0,
        1080.0,
        1440.0,
        1800.0,
        3600.0,
    ],
)
def test_large_positive_longitude_wraparound(
    longitude,
):
    """
    Multiple complete zodiac cycles must normalize correctly.
    """

    result = drekkana(
        longitude
    )

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == 0.0


# ============================================================
# LARGE NEGATIVE WRAPAROUND
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        -360.0,
        -720.0,
        -1080.0,
        -1440.0,
        -3600.0,
    ],
)
def test_large_negative_longitude_wraparound(
    longitude,
):
    """
    Multiple negative zodiac cycles must normalize correctly.
    """

    result = drekkana(
        longitude
    )

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == 0.0


# ============================================================
# CLASSICAL RULE COVERAGE
# ============================================================

def test_all_signs_follow_classical_drekkana_rule():
    """
    Explicitly verify the complete classical rule:

        First  Drekkana -> same sign
        Second Drekkana -> 5th sign
        Third  Drekkana -> 9th sign
    """

    for (
        sign_name,
        sign_start,
        first_sign,
        second_sign,
        third_sign,
    ) in ALL_SIGNS:

        first = drekkana(
            sign_start + 1.0
        )

        second = drekkana(
            sign_start + 11.0
        )

        third = drekkana(
            sign_start + 21.0
        )

        assert first.sign is first_sign
        assert second.sign is second_sign
        assert third.sign is third_sign


# ============================================================
# ZERO DEGREE
# ============================================================

def test_zero_degree_aries():
    """
    0° Aries begins the first Drekkana and therefore maps
    to Aries 0°.
    """

    result = drekkana(
        0.0
    )

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == 0.0


# ============================================================
# FINAL VALID LONGITUDE
# ============================================================

def test_last_valid_longitude():
    """
    A longitude immediately below 360° belongs to the
    third Drekkana of Pisces and maps to Scorpio.
    """

    result = drekkana(
        359.999999
    )

    assert result.sign is ZodiacSign.SCORPIO
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


# ============================================================
# RESULT STRUCTURE
# ============================================================

def test_result_is_varga_position():
    """
    Drekkana must return a VargaPosition instance.
    """

    result = drekkana(
        25.0
    )

    assert isinstance(
        result,
        VargaPosition,
    )


def test_result_always_contains_valid_zodiac_sign():
    """
    Every result must contain a valid ZodiacSign.
    """

    longitudes = [
        -720.0,
        -360.0,
        -359.999999,
        -90.0,
        -30.0,
        -1.0,
        0.0,
        10.0,
        20.0,
        29.999999,
        30.0,
        60.0,
        90.0,
        120.0,
        150.0,
        180.0,
        210.0,
        240.0,
        270.0,
        300.0,
        330.0,
        359.999999,
        360.0,
        720.0,
    ]

    for longitude in longitudes:

        result = drekkana(
            longitude
        )

        assert isinstance(
            result.sign,
            ZodiacSign,
        )


def test_result_degree_is_within_0_to_30():
    """
    Degree within the destination Varga sign must always
    satisfy:

        0 <= degree < 30
    """

    longitudes = [
        -720.0,
        -359.999999,
        -30.0,
        -1.0,
        0.0,
        1.0,
        9.999999,
        10.0,
        19.999999,
        20.0,
        29.999999,
        30.0,
        45.0,
        90.0,
        180.0,
        270.0,
        359.999999,
        360.0,
        720.0,
    ]

    for longitude in longitudes:

        result = drekkana(
            longitude
        )

        assert 0.0 <= result.degree_in_sign < 30.0


# ============================================================
# RESULT DETERMINISM
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        0.0,
        1.0,
        5.0,
        9.999999,
        10.0,
        15.0,
        19.999999,
        20.0,
        25.0,
        29.999999,
        30.0,
        45.0,
        90.0,
        135.0,
        180.0,
        225.0,
        270.0,
        315.0,
        359.999999,
        360.0,
        365.0,
        390.0,
        420.0,
        725.0,
        -1.0,
        -15.0,
        -30.0,
        -45.0,
        -60.0,
        -360.0,
        -720.0,
    ],
)
def test_drekkana_is_repeatable(
    longitude,
):
    """
    Drekkana calculation must be deterministic.
    """

    first = drekkana(
        longitude
    )

    second = drekkana(
        longitude
    )

    assert first == second


# ============================================================
# EQUIVALENT LONGITUDES
# ============================================================

@pytest.mark.parametrize(
    "longitude_a,longitude_b",
    [
        (0.0, 360.0),
        (5.0, 365.0),
        (30.0, 390.0),
        (60.0, 420.0),
        (90.0, 450.0),
        (180.0, 540.0),
        (359.0, 719.0),
        (0.0, -360.0),
        (5.0, -355.0),
        (30.0, -330.0),
        (60.0, -300.0),
        (90.0, -270.0),
        (180.0, -180.0),
    ],
)
def test_equivalent_longitudes_produce_same_result(
    longitude_a,
    longitude_b,
):
    """
    Longitudes separated by complete 360° cycles must
    produce identical Drekkana results.
    """

    first = drekkana(
        longitude_a
    )

    second = drekkana(
        longitude_b
    )

    assert first == second


# ============================================================
# FLOATING-POINT BOUNDARY TESTS
# ============================================================

def test_floating_point_just_below_10_degree():
    """
    9.999999° must remain in the first Drekkana.
    """

    result = drekkana(
        9.999999
    )

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


def test_floating_point_exactly_10_degree():
    """
    10° must begin the second Drekkana.
    """

    result = drekkana(
        10.0
    )

    assert result.sign is ZodiacSign.LEO
    assert result.degree_in_sign == 0.0


def test_floating_point_just_above_10_degree():
    """
    10.000001° must belong to the second Drekkana.
    """

    result = drekkana(
        10.000001
    )

    assert result.sign is ZodiacSign.LEO
    assert result.degree_in_sign == pytest.approx(
        0.000003,
        abs=1e-9,
    )


def test_floating_point_just_below_20_degree():
    """
    19.999999° must remain in the second Drekkana.
    """

    result = drekkana(
        19.999999
    )

    assert result.sign is ZodiacSign.LEO
    assert result.degree_in_sign == pytest.approx(
        29.999997,
        abs=1e-9,
    )


def test_floating_point_exactly_20_degree():
    """
    20° must begin the third Drekkana.
    """

    result = drekkana(
        20.0
    )

    assert result.sign is ZodiacSign.SAGITTARIUS
    assert result.degree_in_sign == 0.0


def test_floating_point_just_above_20_degree():
    """
    20.000001° must belong to the third Drekkana.
    """

    result = drekkana(
        20.000001
    )

    assert result.sign is ZodiacSign.SAGITTARIUS
    assert result.degree_in_sign == pytest.approx(
        0.000003,
        abs=1e-9,
    )