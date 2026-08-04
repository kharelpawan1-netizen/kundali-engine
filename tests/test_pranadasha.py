"""
tests/test_pranadasha.py

Tests for Vimshottari Prana Dasha calculation engine.

Compatible with Python 3.9.
"""

from datetime import datetime, timedelta

import pytest

from astrology.pranadasha import (
    PranaDasha,
    current_pranadasha,
    generate_all_pranadashas,
    generate_pranadashas,
    prana_duration_years,
    prana_sequence,
)

from astrology.pratyantardasha import (
    Pratyantardasha,
)

from astrology.sookshmadasha import (
    SookshmaDasha,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def sample_sookshmadasha():
    """
    Saturn MD / Ketu AD / Sun PD / Saturn SD.

    Example period:
        2026-08-02 -> 2026-08-05
    """

    start = datetime(
        2026,
        8,
        2,
    )

    end = datetime(
        2026,
        8,
        5,
    )

    return SookshmaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        start=start,
        end=end,
    )


# ============================================================
# Model
# ============================================================

def test_pranadasha_model():

    start = datetime(
        2026,
        8,
        2,
    )

    end = datetime(
        2026,
        8,
        3,
    )

    period = PranaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord="Saturn",
        start=start,
        end=end,
    )

    assert period.mahadasha_lord == "Saturn"
    assert period.antardasha_lord == "Ketu"
    assert period.pratyantardasha_lord == "Sun"
    assert period.sookshma_lord == "Saturn"
    assert period.prana_lord == "Saturn"

    assert period.start == start
    assert period.end == end


# ============================================================
# Contains
# ============================================================

def test_pranadasha_contains():

    start = datetime(
        2026,
        8,
        2,
    )

    end = datetime(
        2026,
        8,
        3,
    )

    period = PranaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord="Saturn",
        start=start,
        end=end,
    )

    assert period.contains(start)

    assert period.contains(
        datetime(
            2026,
            8,
            2,
            12,
        )
    )

    assert not period.contains(end)


# ============================================================
# Sequence
# ============================================================

def test_saturn_sequence():

    sequence = prana_sequence(
        "Saturn"
    )

    assert sequence == [
        "Saturn",
        "Mercury",
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
    ]


def test_ketu_sequence():

    sequence = prana_sequence(
        "Ketu"
    )

    assert sequence == [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ]


def test_invalid_sequence_planet():

    with pytest.raises(ValueError):

        prana_sequence(
            "Pluto"
        )


# ============================================================
# Generation
# ============================================================

def test_generate_nine_pranadashas(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    assert len(periods) == 9


def test_first_prana_is_same_as_sookshma_lord(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    assert (
        periods[0].prana_lord
        == sample_sookshmadasha.sookshma_lord
    )


def test_prana_sequence(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    actual = [
        period.prana_lord
        for period in periods
    ]

    expected = [
        "Saturn",
        "Mercury",
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
    ]

    assert actual == expected


# ============================================================
# Parent Relationship
# ============================================================

def test_prana_parent_relationship(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    for period in periods:

        assert (
            period.mahadasha_lord
            == sample_sookshmadasha.mahadasha_lord
        )

        assert (
            period.antardasha_lord
            == sample_sookshmadasha.antardasha_lord
        )

        assert (
            period.pratyantardasha_lord
            == sample_sookshmadasha
            .pratyantardasha_lord
        )

        assert (
            period.sookshma_lord
            == sample_sookshmadasha.sookshma_lord
        )


# ============================================================
# Boundary Tests
# ============================================================

def test_first_prana_starts_at_sd_start(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    assert (
        periods[0].start
        == sample_sookshmadasha.start
    )


def test_last_prana_ends_at_sd_end(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    assert (
        periods[-1].end
        == sample_sookshmadasha.end
    )


def test_prana_periods_are_contiguous(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    for first, second in zip(
        periods,
        periods[1:],
    ):

        assert (
            first.end
            == second.start
        )


def test_prana_periods_cover_entire_sd(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    assert (
        periods[0].start
        == sample_sookshmadasha.start
    )

    assert (
        periods[-1].end
        == sample_sookshmadasha.end
    )


# ============================================================
# Duration
# ============================================================

def test_prana_duration_is_positive(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    for period in periods:

        assert (
            period.duration_days
            > 0
        )

        assert (
            period.duration_years
            > 0
        )


def test_prana_duration_formula(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    first = periods[0]

    expected = (
        sample_sookshmadasha.duration_years
        * 19.0
        / 120.0
    )

    actual = prana_duration_years(
        sample_sookshmadasha,
        "Saturn",
    )

    assert actual == pytest.approx(
        expected,
        rel=1e-12,
    )

    assert (
        first.duration_years
        == pytest.approx(
            expected,
            rel=1e-12,
        )
    )


# ============================================================
# Current Prana
# ============================================================

def test_current_pranadasha(
    sample_sookshmadasha,
):

    periods = generate_pranadashas(
        sample_sookshmadasha
    )

    moment = (
        periods[0].start
        + timedelta(
            hours=1
        )
    )

    current = current_pranadasha(
        sample_sookshmadasha,
        moment,
    )

    assert (
        current.prana_lord
        == "Saturn"
    )

    assert (
        current.start
        == periods[0].start
    )


def test_current_prana_outside_parent_period(
    sample_sookshmadasha,
):

    moment = (
        sample_sookshmadasha.end
        + timedelta(
            seconds=1
        )
    )

    with pytest.raises(
        ValueError
    ):

        current_pranadasha(
            sample_sookshmadasha,
            moment,
        )


# ============================================================
# Bulk Generation
# ============================================================

def test_generate_all_pranadashas(
    sample_sookshmadasha,
):

    result = generate_all_pranadashas(
        [
            sample_sookshmadasha,
        ]
    )

    assert len(result) == 9


def test_all_prana_periods_belong_to_sd(
    sample_sookshmadasha,
):

    periods = generate_all_pranadashas(
        [
            sample_sookshmadasha,
        ]
    )

    for period in periods:

        assert (
            period.sookshma_lord
            == "Saturn"
        )

        assert (
            period.pratyantardasha_lord
            == "Sun"
        )

        assert (
            period.antardasha_lord
            == "Ketu"
        )

        assert (
            period.mahadasha_lord
            == "Saturn"
        )


# ============================================================
# Type Validation
# ============================================================

def test_invalid_sookshmadasha_type():

    with pytest.raises(
        TypeError
    ):

        generate_pranadashas(
            "invalid"
        )


def test_invalid_duration_parent():

    with pytest.raises(
        TypeError
    ):

        prana_duration_years(
            "invalid",
            "Saturn",
        )


def test_invalid_prana_planet(
    sample_sookshmadasha,
):

    with pytest.raises(
        ValueError
    ):

        prana_duration_years(
            sample_sookshmadasha,
            "Pluto",
        )