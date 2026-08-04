
"""
Tests for Vimshottari Pratyantardasha calculations.
"""

from datetime import datetime

import pytest

from astrology.dasha import (
    Antardasha,
    DASHA_SEQUENCE,
    Mahadasha,
)
from astrology.pratyantardasha import (
    Pratyantardasha,
    current_pratyantardasha,
    generate_all_pratyantardashas,
    generate_pratyantardashas,
    pratyantardasha_duration_years,
    pratyantardasha_sequence,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def saturn_mahadasha():
    return Mahadasha(
        planet="Saturn",
        duration_years=19.0,
        start=datetime(2020, 8, 10),
        end=datetime(2039, 8, 11),
    )


@pytest.fixture
def saturn_ketu_antardasha():
    return Antardasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        start=datetime(2026, 4, 23),
        end=datetime(2027, 6, 2),
    )


# ============================================================
# Data Model
# ============================================================

def test_pratyantardasha_model():
    period = Pratyantardasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Ketu",
        start=datetime(2026, 4, 23),
        end=datetime(2026, 5, 1),
    )

    assert period.mahadasha_lord == "Saturn"
    assert period.antardasha_lord == "Ketu"
    assert period.pratyantardasha_lord == "Ketu"
    assert period.start < period.end


def test_pratyantardasha_contains():
    period = Pratyantardasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Ketu",
        start=datetime(2026, 4, 23),
        end=datetime(2026, 5, 1),
    )

    assert period.contains(datetime(2026, 4, 25))
    assert not period.contains(datetime(2026, 5, 1))


# ============================================================
# Sequence
# ============================================================

def test_ketu_sequence():
    sequence = pratyantardasha_sequence("Ketu")

    assert sequence == list(DASHA_SEQUENCE)


def test_saturn_sequence():
    sequence = pratyantardasha_sequence("Saturn")

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


def test_invalid_sequence_planet():
    with pytest.raises(ValueError):
        pratyantardasha_sequence("Pluto")


# ============================================================
# Generation
# ============================================================

def test_generate_nine_pratyantardashas(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    assert len(periods) == 9


def test_first_pd_is_same_as_antardasha_lord(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    assert (
        periods[0].pratyantardasha_lord
        == "Ketu"
    )


def test_pd_sequence(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    assert [
        period.pratyantardasha_lord
        for period in periods
    ] == [
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


def test_pd_parent_relationship(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    for period in periods:
        assert period.mahadasha_lord == "Saturn"
        assert period.antardasha_lord == "Ketu"


# ============================================================
# Boundary Integrity
# ============================================================

def test_first_pd_starts_at_ad_start(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    assert (
        periods[0].start
        == saturn_ketu_antardasha.start
    )


def test_last_pd_ends_at_ad_end(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    assert (
        periods[-1].end
        == saturn_ketu_antardasha.end
    )


def test_pd_periods_are_contiguous(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    for first, second in zip(
        periods,
        periods[1:],
    ):
        assert first.end == second.start


def test_pd_periods_cover_entire_ad(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    total_days = sum(
        period.duration_days
        for period in periods
    )

    expected_days = (
        saturn_ketu_antardasha.end
        - saturn_ketu_antardasha.start
    ).total_seconds() / 86400.0

    assert total_days == pytest.approx(
        expected_days,
        abs=1e-9,
    )


# ============================================================
# Duration
# ============================================================

def test_pd_duration_is_positive(
    saturn_ketu_antardasha,
):
    periods = generate_pratyantardashas(
        saturn_ketu_antardasha
    )

    for period in periods:
        assert period.duration_days > 0


def test_pd_duration_formula(
    saturn_ketu_antardasha,
):
    duration = pratyantardasha_duration_years(
        saturn_ketu_antardasha,
        "Ketu",
    )

    expected = (
        saturn_ketu_antardasha.duration_days
        / 365.25
        * 7.0
        / 120.0
    )

    assert duration == pytest.approx(
        expected,
        abs=1e-12,
    )


# ============================================================
# Current Period
# ============================================================

def test_current_pratyantardasha(
    saturn_ketu_antardasha,
):
    moment = datetime(
        2026,
        5,
        1,
    )

    current = current_pratyantardasha(
        saturn_ketu_antardasha,
        moment,
    )

    assert isinstance(
        current,
        Pratyantardasha,
    )

    assert current.mahadasha_lord == "Saturn"
    assert current.antardasha_lord == "Ketu"


def test_current_pd_outside_parent_period(
    saturn_ketu_antardasha,
):
    moment = datetime(
        2028,
        1,
        1,
    )

    with pytest.raises(ValueError):
        current_pratyantardasha(
            saturn_ketu_antardasha,
            moment,
        )


# ============================================================
# Complete Mahadasha Expansion
# ============================================================

def test_generate_all_pratyantardashas(
    saturn_mahadasha,
):
    periods = generate_all_pratyantardashas(
        saturn_mahadasha
    )

    assert len(periods) == 81


def test_all_pd_periods_belong_to_saturn(
    saturn_mahadasha,
):
    periods = generate_all_pratyantardashas(
        saturn_mahadasha
    )

    assert all(
        period.mahadasha_lord == "Saturn"
        for period in periods
    )
