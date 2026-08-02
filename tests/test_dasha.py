
"""
tests/test_dasha.py

Tests for the Vimshottari Dasha calculation engine.

Compatible with Python 3.9.
"""

from datetime import datetime

import pytest

from astrology.dasha import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    VIMSHOTTARI_TOTAL_YEARS,
    current_antardasha,
    current_mahadasha,
    first_mahadasha_balance,
    generate_antardashas,
    generate_mahadashas,
    moon_nakshatra_progress,
    nakshatra_index,
    nakshatra_lord,
    nakshatra_name,
    nakshatra_number,
    next_dasha_lord,
)


# ============================================================
# Constants
# ============================================================

EPSILON = 1e-9
NAKSHATRA_SPAN = 360.0 / 27.0


# ============================================================
# Vimshottari Constants
# ============================================================


def test_vimshottari_total_is_120_years():
    """The complete Vimshottari cycle must total 120 years."""
    assert VIMSHOTTARI_TOTAL_YEARS == 120.0


def test_dasha_sequence_contains_nine_planets():
    """The classical Vimshottari sequence contains nine lords."""
    assert len(DASHA_SEQUENCE) == 9
    assert DASHA_SEQUENCE == (
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    )


def test_dasha_years_total_120():
    """All nine Mahadasha durations must total 120 years."""
    assert sum(DASHA_YEARS.values()) == pytest.approx(120.0)


# ============================================================
# Nakshatra Tests
# ============================================================


def test_zero_longitude_is_ashwini():
    """0 degrees belongs to Ashwini."""
    assert nakshatra_index(0.0) == 0
    assert nakshatra_number(0.0) == 1
    assert nakshatra_name(0.0) == "Ashwini"
    assert nakshatra_lord(0.0) == "Ketu"


def test_bharani_is_second_nakshatra():
    """Bharani is the second Nakshatra and is ruled by Venus."""
    longitude = NAKSHATRA_SPAN + EPSILON

    assert nakshatra_index(longitude) == 1
    assert nakshatra_number(longitude) == 2
    assert nakshatra_name(longitude) == "Bharani"
    assert nakshatra_lord(longitude) == "Venus"


def test_pushya_is_saturn_ruled():
    """Pushya must be ruled by Saturn."""
    # Pushya begins at Nakshatra 8:
    # 7 * 13°20' = 93°20'.
    #
    # Add a tiny epsilon so the test point is safely inside
    # Pushya rather than sitting exactly on a floating-point
    # boundary.
    longitude = (7 * NAKSHATRA_SPAN) + EPSILON

    assert nakshatra_index(longitude) == 7
    assert nakshatra_number(longitude) == 8
    assert nakshatra_name(longitude) == "Pushya"
    assert nakshatra_lord(longitude) == "Saturn"


def test_mula_is_ketu_ruled():
    """Mula must be ruled by Ketu."""
    # Mula begins at Nakshatra 19:
    # 18 * 13°20' = 253°20'.
    longitude = (18 * NAKSHATRA_SPAN) + EPSILON

    assert nakshatra_index(longitude) == 18
    assert nakshatra_number(longitude) == 19
    assert nakshatra_name(longitude) == "Mula"
    assert nakshatra_lord(longitude) == "Ketu"


def test_revati_is_mercury_ruled():
    """Revati is the 27th Nakshatra and is ruled by Mercury."""
    longitude = (26 * NAKSHATRA_SPAN) + EPSILON

    assert nakshatra_index(longitude) == 26
    assert nakshatra_number(longitude) == 27
    assert nakshatra_name(longitude) == "Revati"
    assert nakshatra_lord(longitude) == "Mercury"


def test_nakshatra_boundaries():
    """Each Nakshatra begins at the expected zodiacal longitude."""
    for index in range(27):
        longitude = (index * NAKSHATRA_SPAN) + EPSILON

        assert nakshatra_index(longitude) == index


def test_nakshatra_progress_at_start_is_zero():
    """The start of a Nakshatra has zero progress."""
    assert moon_nakshatra_progress(0.0) == pytest.approx(0.0)


def test_nakshatra_progress_is_between_zero_and_one():
    """Nakshatra progress must remain in [0, 1)."""
    longitudes = (
        0.0,
        10.0,
        50.0,
        100.0,
        180.0,
        253.5,
        359.999999,
    )

    for longitude in longitudes:
        progress = moon_nakshatra_progress(longitude)

        assert 0.0 <= progress < 1.0


def test_nakshatra_progress_at_middle_is_half():
    """The middle of a Nakshatra should give approximately 0.5."""
    longitude = NAKSHATRA_SPAN / 2.0

    assert moon_nakshatra_progress(longitude) == pytest.approx(0.5)


# ============================================================
# First Mahadasha Balance
# ============================================================


def test_first_mahadasha_balance_at_ashwini_start_is_full_ketu():
    """At Ashwini start, the full Ketu period remains."""
    assert first_mahadasha_balance(0.0) == pytest.approx(7.0)


def test_first_mahadasha_balance_decreases_as_nakshatra_progresses():
    """The remaining Mahadasha balance decreases as Moon progresses."""
    beginning = first_mahadasha_balance(0.0)

    middle = first_mahadasha_balance(
        NAKSHATRA_SPAN / 2.0
    )

    near_end = first_mahadasha_balance(
        NAKSHATRA_SPAN - EPSILON
    )

    assert beginning > middle > near_end
    assert near_end > 0.0


# ============================================================
# Dasha Sequence
# ============================================================


def test_next_dasha_lord():
    """next_dasha_lord must follow the classical sequence."""
    assert next_dasha_lord("Ketu") == "Venus"
    assert next_dasha_lord("Venus") == "Sun"
    assert next_dasha_lord("Sun") == "Moon"
    assert next_dasha_lord("Moon") == "Mars"
    assert next_dasha_lord("Mars") == "Rahu"
    assert next_dasha_lord("Rahu") == "Jupiter"
    assert next_dasha_lord("Jupiter") == "Saturn"
    assert next_dasha_lord("Saturn") == "Mercury"
    assert next_dasha_lord("Mercury") == "Ketu"


def test_next_dasha_lord_rejects_invalid_planet():
    """Invalid Dasha lords must raise ValueError."""
    with pytest.raises(ValueError):
        next_dasha_lord("Earth")


# ============================================================
# Mahadasha Generation
# ============================================================


def test_generate_mahadashas_starts_with_correct_lord():
    """Moon in Ashwini must start with Ketu Mahadasha."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    periods = generate_mahadashas(
        birth,
        0.0,
        count=3,
    )

    assert periods[0].planet == "Ketu"
    assert periods[1].planet == "Venus"
    assert periods[2].planet == "Sun"


def test_generate_mahadashas_first_period_has_balance():
    """The first Mahadasha must use the calculated balance."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    periods = generate_mahadashas(
        birth,
        0.0,
        count=1,
    )

    assert periods[0].duration_years == pytest.approx(7.0)


def test_generate_mahadashas_first_period_can_be_partial():
    """Moon partway through Ashwini produces a partial Ketu period."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    moon_longitude = NAKSHATRA_SPAN / 2.0

    periods = generate_mahadashas(
        birth,
        moon_longitude,
        count=2,
    )

    assert periods[0].planet == "Ketu"
    assert periods[0].duration_years == pytest.approx(3.5)

    assert periods[1].planet == "Venus"
    assert periods[1].duration_years == pytest.approx(20.0)


def test_mahadasha_periods_are_contiguous():
    """Each Mahadasha must begin exactly when the previous one ends."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    periods = generate_mahadashas(
        birth,
        0.0,
        count=9,
    )

    for previous, current in zip(periods, periods[1:]):
        assert previous.end == current.start


def test_generate_mahadashas_has_requested_count():
    """The requested number of periods must be generated."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    periods = generate_mahadashas(
        birth,
        0.0,
        count=5,
    )

    assert len(periods) == 5


def test_generate_mahadashas_rejects_zero_count():
    """Zero Mahadashas must be rejected."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    with pytest.raises(ValueError):
        generate_mahadashas(
            birth,
            0.0,
            count=0,
        )


# ============================================================
# Antardasha
# ============================================================


def test_antardasha_has_nine_periods():
    """Every Mahadasha must contain nine Antardashas."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    mahadasha = generate_mahadashas(
        birth,
        0.0,
        count=1,
    )[0]

    antardashas = generate_antardashas(mahadasha)

    assert len(antardashas) == 9


def test_ketu_mahadasha_starts_with_ketu_antardasha():
    """Ketu/Ketu must be the first Antardasha of Ketu Mahadasha."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    mahadasha = generate_mahadashas(
        birth,
        0.0,
        count=1,
    )[0]

    antardashas = generate_antardashas(mahadasha)

    assert antardashas[0].mahadasha_lord == "Ketu"
    assert antardashas[0].antardasha_lord == "Ketu"


def test_venus_mahadasha_starts_with_venus_antardasha():
    """Venus/Venus must begin the Venus Mahadasha."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    # Venus is the Nakshatra lord of Bharani.
    # Use a longitude safely inside Bharani.
    moon_longitude = NAKSHATRA_SPAN + EPSILON

    mahadasha = generate_mahadashas(
        birth,
        moon_longitude,
        count=2,
    )[0]

    assert mahadasha.planet == "Venus"

    antardashas = generate_antardashas(mahadasha)

    assert antardashas[0].mahadasha_lord == "Venus"
    assert antardashas[0].antardasha_lord == "Venus"


def test_antardashas_are_contiguous():
    """Antardasha periods must be contiguous."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    mahadasha = generate_mahadashas(
        birth,
        0.0,
        count=1,
    )[0]

    antardashas = generate_antardashas(mahadasha)

    for previous, current in zip(
        antardashas,
        antardashas[1:],
    ):
        assert previous.end == current.start


def test_antardasha_ends_at_mahadasha_end():
    """The final Antardasha must end exactly with its Mahadasha."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    mahadasha = generate_mahadashas(
        birth,
        0.0,
        count=1,
    )[0]

    antardashas = generate_antardashas(mahadasha)

    assert antardashas[-1].end == mahadasha.end


# ============================================================
# Current Dasha
# ============================================================


def test_current_mahadasha_at_birth():
    """At the birth moment, the starting Mahadasha is active."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    mahadasha = current_mahadasha(
        birth,
        0.0,
        birth,
    )

    assert mahadasha.planet == "Ketu"
    assert mahadasha.start == birth


def test_current_antardasha_at_birth():
    """At birth, the starting Antardasha is active."""
    birth = datetime(2000, 1, 1, 12, 0, 0)

    antardasha = current_antardasha(
        birth,
        0.0,
        birth,
    )

    assert antardasha.mahadasha_lord == "Ketu"
    assert antardasha.antardasha_lord == "Ketu"
    assert antardasha.start == birth


# ============================================================
# Validation
# ============================================================


def test_invalid_moon_longitude_type():
    """Non-numeric Moon longitude must raise TypeError."""
    with pytest.raises(TypeError):
        nakshatra_index("not-a-number")


def test_invalid_moon_longitude_above_360():
    """Longitude above 360 degrees must raise ValueError."""
    with pytest.raises(ValueError):
        nakshatra_index(361.0)


def test_invalid_moon_longitude_below_zero():
    """Negative longitude must raise ValueError."""
    with pytest.raises(ValueError):
        nakshatra_index(-1.0)


def test_360_degrees_wraps_to_zero():
    """Exactly 360 degrees must be treated as 0 degrees."""
    assert nakshatra_index(360.0) == 0
    assert nakshatra_name(360.0) == "Ashwini"
    assert nakshatra_lord(360.0) == "Ketu"

