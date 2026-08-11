"""
tests/test_navamsa.py

Comprehensive tests for the Parashari Navamsa (D9) calculation.

Classical Parashari Navamsa rules:

    - Each zodiac sign is divided into 9 equal Navamsas.
    - Each Navamsa is 3°20′ (10/3 degrees).
    - Movable signs begin their Navamsa sequence from themselves.
    - Fixed signs begin from the 9th sign from themselves.
    - Dual signs begin from the 5th sign from themselves.
    - The nine Navamsas then proceed sequentially through the zodiac.

The tests verify:

    - All 12 zodiac signs
    - All 9 Navamsa divisions
    - Classical starting-sign rules
    - Exact 3°20′ boundaries
    - Just-before and just-after boundaries
    - Exact zodiac sign boundaries
    - Final Navamsa of every sign
    - Positive longitude wraparound
    - Negative longitude normalization
    - Large positive and negative longitudes
    - Degree-in-sign range
    - Result structure
    - Classical sequence continuity
    - Floating-point boundary behavior
    - Repeatability

Compatible with Python 3.9.
"""

import pytest

from astronomy.navamsa import navamsa
from models.zodiac import ZodiacSign


# ============================================================
# CONSTANTS
# ============================================================

NAVAMSA_SIZE = 30.0 / 9.0
EPSILON = 1e-7


# ============================================================
# SIGN GROUPS
# ============================================================

MOVABLE_SIGNS = [
    (
        0.0,
        ZodiacSign.ARIES,
        ZodiacSign.ARIES,
    ),
    (
        90.0,
        ZodiacSign.CANCER,
        ZodiacSign.CANCER,
    ),
    (
        180.0,
        ZodiacSign.LIBRA,
        ZodiacSign.LIBRA,
    ),
    (
        270.0,
        ZodiacSign.CAPRICORN,
        ZodiacSign.CAPRICORN,
    ),
]


FIXED_SIGNS = [
    (
        30.0,
        ZodiacSign.TAURUS,
        ZodiacSign.CAPRICORN,
    ),
    (
        120.0,
        ZodiacSign.LEO,
        ZodiacSign.ARIES,
    ),
    (
        210.0,
        ZodiacSign.SCORPIO,
        ZodiacSign.CANCER,
    ),
    (
        300.0,
        ZodiacSign.AQUARIUS,
        ZodiacSign.LIBRA,
    ),
]


DUAL_SIGNS = [
    (
        60.0,
        ZodiacSign.GEMINI,
        ZodiacSign.LIBRA,
    ),
    (
        150.0,
        ZodiacSign.VIRGO,
        ZodiacSign.CAPRICORN,
    ),
    (
        240.0,
        ZodiacSign.SAGITTARIUS,
        ZodiacSign.ARIES,
    ),
    (
        330.0,
        ZodiacSign.PISCES,
        ZodiacSign.CANCER,
    ),
]


ALL_SIGN_STARTS = [
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
]


# ============================================================
# EXPECTED CLASSICAL NAVAMSA STARTING SIGNS
# ============================================================

@pytest.mark.parametrize(
    "sign_start,sign,expected_start",
    MOVABLE_SIGNS,
)
def test_movable_sign_starts_from_itself(
    sign_start,
    sign,
    expected_start,
):
    """
    Movable signs begin their Navamsa sequence from themselves.
    """

    result = navamsa(sign_start + 1.0)

    assert result.sign is expected_start


@pytest.mark.parametrize(
    "sign_start,sign,expected_start",
    FIXED_SIGNS,
)
def test_fixed_sign_starts_from_ninth_sign(
    sign_start,
    sign,
    expected_start,
):
    """
    Fixed signs begin their Navamsa sequence from the 9th sign
    from themselves.
    """

    result = navamsa(sign_start + 1.0)

    assert result.sign is expected_start


@pytest.mark.parametrize(
    "sign_start,sign,expected_start",
    DUAL_SIGNS,
)
def test_dual_sign_starts_from_fifth_sign(
    sign_start,
    sign,
    expected_start,
):
    """
    Dual signs begin their Navamsa sequence from the 5th sign
    from themselves.
    """

    result = navamsa(sign_start + 1.0)

    assert result.sign is expected_start


# ============================================================
# COMPLETE CLASSICAL NAVAMSA SEQUENCES
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sequence",
    [
        (
            0.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            30.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
        (
            60.0,
            [
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
            ],
        ),
        (
            90.0,
            [
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
            ],
        ),
        (
            120.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            150.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
        (
            180.0,
            [
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
            ],
        ),
        (
            210.0,
            [
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
            ],
        ),
        (
            240.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            270.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
        (
            300.0,
            [
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
            ],
        ),
        (
            330.0,
            [
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
            ],
        ),
    ],
)
def test_complete_navamsa_sequence(
    sign_start,
    expected_sequence,
):
    """
    Every zodiac sign must follow the complete classical
    nine-Navamsa sequence.
    """

    for index, expected_sign in enumerate(expected_sequence):

        longitude = (
            sign_start
            + (index * NAVAMSA_SIZE)
            + (NAVAMSA_SIZE / 2.0)
        )

        result = navamsa(longitude)

        assert result.sign is expected_sign


# ============================================================
# FIRST NAVAMSA OF EVERY SIGN
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.ARIES),
        (30.0, ZodiacSign.CAPRICORN),
        (60.0, ZodiacSign.LIBRA),
        (90.0, ZodiacSign.CANCER),
        (120.0, ZodiacSign.ARIES),
        (150.0, ZodiacSign.CAPRICORN),
        (180.0, ZodiacSign.LIBRA),
        (210.0, ZodiacSign.CANCER),
        (240.0, ZodiacSign.ARIES),
        (270.0, ZodiacSign.CAPRICORN),
        (300.0, ZodiacSign.LIBRA),
        (330.0, ZodiacSign.CANCER),
    ],
)
def test_first_navamsa_of_every_sign(
    sign_start,
    expected_sign,
):
    """
    The first Navamsa of every zodiac sign must have the
    correct classical starting sign.
    """

    result = navamsa(sign_start + 1.0)

    assert result.sign is expected_sign


# ============================================================
# LAST NAVAMSA OF EVERY SIGN
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.SAGITTARIUS),
        (30.0, ZodiacSign.VIRGO),
        (60.0, ZodiacSign.GEMINI),
        (90.0, ZodiacSign.PISCES),
        (120.0, ZodiacSign.SAGITTARIUS),
        (150.0, ZodiacSign.VIRGO),
        (180.0, ZodiacSign.GEMINI),
        (210.0, ZodiacSign.PISCES),
        (240.0, ZodiacSign.SAGITTARIUS),
        (270.0, ZodiacSign.VIRGO),
        (300.0, ZodiacSign.GEMINI),
        (330.0, ZodiacSign.PISCES),
    ],
)
def test_last_navamsa_of_every_sign(
    sign_start,
    expected_sign,
):
    """
    The ninth Navamsa of every zodiac sign must have the
    correct final sign.
    """

    result = navamsa(
        sign_start
        + (8.0 * NAVAMSA_SIZE)
        + 1.0
    )

    assert result.sign is expected_sign


# ============================================================
# EXACT 3°20′ BOUNDARIES
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sequence",
    [
        (
            0.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            30.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
        (
            60.0,
            [
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
            ],
        ),
        (
            90.0,
            [
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
            ],
        ),
    ],
)
def test_exact_navamsa_boundaries(
    sign_start,
    expected_sequence,
):
    """
    Exactly 3°20′ begins the next Navamsa.

    The first boundary remains the first Navamsa and every
    subsequent exact boundary begins the corresponding
    next Navamsa.
    """

    first = navamsa(sign_start)

    assert first.sign is expected_sequence[0]

    for index in range(1, 9):

        longitude = sign_start + (
            index * NAVAMSA_SIZE
        )

        result = navamsa(longitude)

        assert result.sign is expected_sequence[index]


# ============================================================
# JUST BEFORE NAVAMSA BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sequence",
    [
        (
            0.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            30.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
    ],
)
def test_just_before_navamsa_boundary_remains_previous(
    sign_start,
    expected_sequence,
):
    """
    A longitude infinitesimally below a Navamsa boundary
    remains in the preceding Navamsa.
    """

    for index in range(1, 9):

        longitude = (
            sign_start
            + (index * NAVAMSA_SIZE)
            - EPSILON
        )

        result = navamsa(longitude)

        assert result.sign is expected_sequence[index - 1]


# ============================================================
# JUST AFTER NAVAMSA BOUNDARY
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sequence",
    [
        (
            0.0,
            [
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
                ZodiacSign.LIBRA,
                ZodiacSign.SCORPIO,
                ZodiacSign.SAGITTARIUS,
            ],
        ),
        (
            30.0,
            [
                ZodiacSign.CAPRICORN,
                ZodiacSign.AQUARIUS,
                ZodiacSign.PISCES,
                ZodiacSign.ARIES,
                ZodiacSign.TAURUS,
                ZodiacSign.GEMINI,
                ZodiacSign.CANCER,
                ZodiacSign.LEO,
                ZodiacSign.VIRGO,
            ],
        ),
    ],
)
def test_just_after_navamsa_boundary_enters_next(
    sign_start,
    expected_sequence,
):
    """
    A longitude infinitesimally above a Navamsa boundary
    belongs to the next Navamsa.
    """

    for index in range(1, 9):

        longitude = (
            sign_start
            + (index * NAVAMSA_SIZE)
            + EPSILON
        )

        result = navamsa(longitude)

        assert result.sign is expected_sequence[index]


# ============================================================
# EXACT ZODIAC SIGN BOUNDARIES
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.ARIES),
        (30.0, ZodiacSign.CAPRICORN),
        (60.0, ZodiacSign.LIBRA),
        (90.0, ZodiacSign.CANCER),
        (120.0, ZodiacSign.ARIES),
        (150.0, ZodiacSign.CAPRICORN),
        (180.0, ZodiacSign.LIBRA),
        (210.0, ZodiacSign.CANCER),
        (240.0, ZodiacSign.ARIES),
        (270.0, ZodiacSign.CAPRICORN),
        (300.0, ZodiacSign.LIBRA),
        (330.0, ZodiacSign.CANCER),
    ],
)
def test_exact_zodiac_sign_boundary_starts_first_navamsa(
    sign_start,
    expected_sign,
):
    """
    Every exact 30° boundary begins the first Navamsa
    of the new zodiac sign.
    """

    result = navamsa(sign_start)

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(0.0)


# ============================================================
# FINAL POINT OF EVERY ZODIAC SIGN
# ============================================================

@pytest.mark.parametrize(
    "sign_start,expected_sign",
    [
        (0.0, ZodiacSign.SAGITTARIUS),
        (30.0, ZodiacSign.VIRGO),
        (60.0, ZodiacSign.GEMINI),
        (90.0, ZodiacSign.PISCES),
        (120.0, ZodiacSign.SAGITTARIUS),
        (150.0, ZodiacSign.VIRGO),
        (180.0, ZodiacSign.GEMINI),
        (210.0, ZodiacSign.PISCES),
        (240.0, ZodiacSign.SAGITTARIUS),
        (270.0, ZodiacSign.VIRGO),
        (300.0, ZodiacSign.GEMINI),
        (330.0, ZodiacSign.PISCES),
    ],
)
def test_near_end_of_every_zodiac_sign(
    sign_start,
    expected_sign,
):
    """
    A longitude immediately below the next zodiac sign
    boundary must remain in the ninth Navamsa.
    """

    result = navamsa(
        sign_start
        + 29.999999
    )

    assert result.sign is expected_sign


# ============================================================
# DEGREE-IN-NAVAMSA TRANSFORMATION
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_degree",
    [
        (0.0, 0.0),
        (1.0, 9.0),
        (2.0, 18.0),
        (3.0, 27.0),
        (10.0, 0.0),
        (11.0, 9.0),
        (12.0, 18.0),
        (13.0, 27.0),
        (30.0, 0.0),
        (31.0, 9.0),
        (32.0, 18.0),
        (33.0, 27.0),
    ],
)
def test_degree_in_navamsa_transformation(
    longitude,
    expected_degree,
):
    """
    One Navamsa spans 10/3° of the natal sign and maps to
    0°–30° in the resulting Navamsa sign.
    """

    result = navamsa(longitude)

    assert result.degree_in_sign == pytest.approx(
        expected_degree
    )


# ============================================================
# DEGREE RANGE
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        0.0,
        1.0,
        3.333333,
        3.333334,
        5.0,
        10.0,
        14.999999,
        15.0,
        17.8,
        20.0,
        23.333333,
        26.666666,
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
    ],
)
def test_degree_in_sign_always_within_valid_range(
    longitude,
):
    """
    The resulting Navamsa degree must always be in
    the interval [0, 30).
    """

    result = navamsa(longitude)

    assert 0.0 <= result.degree_in_sign < 30.0


# ============================================================
# RESULT SIGN IS ALWAYS VALID
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        -720.0,
        -360.0,
        -359.999999,
        -180.0,
        -90.0,
        -60.0,
        -30.0,
        -1.0,
        0.0,
        1.0,
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
    ],
)
def test_result_sign_is_valid_zodiac_sign(
    longitude,
):
    """
    Every valid calculation must return a ZodiacSign.
    """

    result = navamsa(longitude)

    assert isinstance(result.sign, ZodiacSign)


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
            361.0,
            ZodiacSign.ARIES,
            9.0,
        ),
        (
            365.0,
            ZodiacSign.TAURUS,
            15.0,
        ),
        (
            390.0,
            ZodiacSign.CAPRICORN,
            0.0,
        ),
        (
            420.0,
            ZodiacSign.LIBRA,
            0.0,
        ),
        (
            725.0,
            ZodiacSign.TAURUS,
            15.0,
        ),
    ],
)
def test_positive_longitude_wraparound(
    longitude,
    expected_sign,
    expected_degree,
):
    """
    Positive longitudes above 360° must be normalized
    modulo 360°.
    """

    result = navamsa(longitude)

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(
        expected_degree
    )


# ============================================================
# NEGATIVE LONGITUDE NORMALIZATION
# ============================================================

@pytest.mark.parametrize(
    "longitude,expected_sign,expected_degree",
    [
        (
            -1.0,
            ZodiacSign.PISCES,
            21.0,
        ),
        (
            -5.0,
            ZodiacSign.AQUARIUS,
            15.0,
        ),
        (
            -10.0,
            ZodiacSign.CAPRICORN,
            0.0,
        ),
        (
            -15.0,
            ZodiacSign.SCORPIO,
            15.0,
        ),
        (
            -20.0,
            ZodiacSign.LIBRA,
            0.0,
        ),
        (
            -30.0,
            ZodiacSign.CANCER,
            0.0,
        ),
        (
            -45.0,
            ZodiacSign.AQUARIUS,
            15.0,
        ),
        (
            -60.0,
            ZodiacSign.LIBRA,
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
    """

    result = navamsa(longitude)

    assert result.sign is expected_sign
    assert result.degree_in_sign == pytest.approx(
        expected_degree
    )

# ============================================================
# FULL NEGATIVE-EQUIVALENCE TEST
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        -1.0,
        -5.0,
        -10.0,
        -15.0,
        -20.0,
        -30.0,
        -45.0,
        -60.0,
        -90.0,
        -120.0,
        -150.0,
        -180.0,
        -210.0,
        -240.0,
        -270.0,
        -300.0,
        -330.0,
    ],
)
def test_negative_longitude_matches_modulo_360_equivalent(
    longitude,
):
    """
    A negative longitude must produce the same result as
    its equivalent normalized longitude in [0, 360).
    """

    negative_result = navamsa(longitude)
    normalized_result = navamsa(longitude % 360.0)

    assert negative_result == normalized_result


# ============================================================
# FULL POSITIVE WRAPAROUND EQUIVALENCE
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        360.0,
        361.0,
        365.0,
        390.0,
        420.0,
        450.0,
        720.0,
        725.0,
        1080.0,
    ],
)
def test_positive_longitude_matches_modulo_360_equivalent(
    longitude,
):
    """
    A longitude above 360° must produce the same result as
    its normalized modulo-360 equivalent.
    """

    wrapped_result = navamsa(longitude)
    normalized_result = navamsa(longitude % 360.0)

    assert wrapped_result == normalized_result


# ============================================================
# FLOATING-POINT BOUNDARIES
# ============================================================

def test_floating_point_first_boundary():
    """
    The exact first Navamsa boundary must enter the second
    Navamsa.
    """

    boundary = 30.0 / 9.0

    result = navamsa(boundary)

    assert result.sign is ZodiacSign.TAURUS
    assert result.degree_in_sign == pytest.approx(0.0)


def test_floating_point_second_boundary():
    """
    The exact second Navamsa boundary must enter the third
    Navamsa.
    """

    boundary = 2.0 * (30.0 / 9.0)

    result = navamsa(boundary)

    assert result.sign is ZodiacSign.GEMINI
    assert result.degree_in_sign == pytest.approx(0.0)


def test_just_before_first_boundary():
    """
    A longitude infinitesimally below 3°20′ remains in the
    first Navamsa.
    """

    boundary = 30.0 / 9.0

    result = navamsa(
        boundary - EPSILON
    )

    assert result.sign is ZodiacSign.ARIES


def test_just_after_first_boundary():
    """
    A longitude infinitesimally above 3°20′ enters the
    second Navamsa.
    """

    boundary = 30.0 / 9.0

    result = navamsa(
        boundary + EPSILON
    )

    assert result.sign is ZodiacSign.TAURUS


# ============================================================
# ZERO DEGREE
# ============================================================

def test_zero_degree_aries():
    """
    0° Aries begins Aries Navamsa.
    """

    result = navamsa(0.0)

    assert result.sign is ZodiacSign.ARIES
    assert result.degree_in_sign == pytest.approx(0.0)


# ============================================================
# LAST VALID LONGITUDE
# ============================================================

def test_last_valid_longitude():
    """
    A longitude immediately below 360° belongs to the ninth
    Navamsa of Pisces, which is Pisces itself.
    """

    result = navamsa(359.999999)

    assert result.sign is ZodiacSign.PISCES
    assert 0.0 <= result.degree_in_sign < 30.0


# ============================================================
# RESULT STRUCTURE
# ============================================================

def test_result_contains_sign_and_degree():
    """
    Navamsa result must contain both sign and degree_in_sign.
    """

    result = navamsa(17.8)

    assert hasattr(result, "sign")
    assert hasattr(result, "degree_in_sign")


def test_result_sign_is_zodiac_sign():
    """
    Result sign must be an instance of ZodiacSign.
    """

    result = navamsa(17.8)

    assert isinstance(result.sign, ZodiacSign)


def test_result_degree_is_float():
    """
    Result degree must be numeric and represent the degree
    within the Navamsa sign.
    """

    result = navamsa(17.8)

    assert isinstance(
        result.degree_in_sign,
        float,
    )


# ============================================================
# REPEATABILITY
# ============================================================

@pytest.mark.parametrize(
    "longitude",
    [
        0.0,
        1.0,
        3.333333,
        10.0,
        15.0,
        17.8,
        20.0,
        29.999999,
        30.0,
        45.0,
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
        -1.0,
        -30.0,
        -90.0,
        -180.0,
        -360.0,
        725.0,
    ],
)
def test_navamsa_is_repeatable(longitude):
    """
    Navamsa calculation must be deterministic.
    """

    first = navamsa(longitude)
    second = navamsa(longitude)

    assert first == second