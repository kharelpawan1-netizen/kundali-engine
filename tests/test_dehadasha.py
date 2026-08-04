
"""
tests/test_dehadasha.py

Tests for Vimshottari Deha Dasha calculation.

Compatible with Python 3.9.
"""

from datetime import datetime, timedelta

import pytest

from astrology.dehadasha import (
    DehaDasha,
    current_dehadasha,
    deha_duration_years,
    deha_sequence,
    generate_all_dehadashas,
    generate_dehadashas,
)

from astrology.dasha import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    VIMSHOTTARI_TOTAL_YEARS,
)

from astrology.pranadasha import (
    PranaDasha,
)


# ============================================================
# Test Helpers
# ============================================================

def make_pranadasha(
    prana_lord="Saturn",
    start=None,
    end=None,
):
    """Create a deterministic PranaDasha for testing."""

    if start is None:
        start = datetime(
            2026,
            8,
            2,
        )

    if end is None:
        end = start + timedelta(
            days=9
        )

    return PranaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord=prana_lord,
        start=start,
        end=end,
    )


# ============================================================
# Model Tests
# ============================================================

def test_dehadasha_model():
    """DehaDasha should store all hierarchy fields."""

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

    period = DehaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord="Saturn",
        deha_lord="Saturn",
        start=start,
        end=end,
    )

    assert period.mahadasha_lord == "Saturn"
    assert period.antardasha_lord == "Ketu"
    assert period.pratyantardasha_lord == "Sun"
    assert period.sookshma_lord == "Saturn"
    assert period.prana_lord == "Saturn"
    assert period.deha_lord == "Saturn"
    assert period.start == start
    assert period.end == end


def test_dehadasha_contains():
    """contains() should use an inclusive start and exclusive end."""

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

    period = DehaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord="Saturn",
        deha_lord="Saturn",
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
# Sequence Tests
# ============================================================

def test_saturn_sequence():
    """Saturn sequence should begin from Saturn."""

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

    assert deha_sequence(
        "Saturn"
    ) == expected


def test_ketu_sequence():
    """Ketu sequence should begin from Ketu."""

    expected = [
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

    assert deha_sequence(
        "Ketu"
    ) == expected


def test_invalid_sequence_planet():
    """Unknown planets should raise ValueError."""

    with pytest.raises(
        ValueError
    ):
        deha_sequence(
            "Pluto"
        )


# ============================================================
# Generation Tests
# ============================================================

def test_generate_nine_dehadashas():
    """A Prana Dasha should contain exactly nine Deha periods."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    assert len(periods) == 9


def test_first_deha_is_same_as_prana_lord():
    """The first Deha lord must equal the parent Prana lord."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    periods = generate_dehadashas(
        pranadasha
    )

    assert periods[0].deha_lord == "Saturn"


def test_deha_sequence():
    """Generated Deha lords should follow Vimshottari order."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    periods = generate_dehadashas(
        pranadasha
    )

    actual = [
        period.deha_lord
        for period in periods
    ]

    expected = deha_sequence(
        "Saturn"
    )

    assert actual == expected


def test_deha_parent_relationship():
    """Every Deha must preserve the complete parent hierarchy."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    periods = generate_dehadashas(
        pranadasha
    )

    for period in periods:

        assert (
            period.mahadasha_lord
            == pranadasha.mahadasha_lord
        )

        assert (
            period.antardasha_lord
            == pranadasha.antardasha_lord
        )

        assert (
            period.pratyantardasha_lord
            == pranadasha.pratyantardasha_lord
        )

        assert (
            period.sookshma_lord
            == pranadasha.sookshma_lord
        )

        assert (
            period.prana_lord
            == pranadasha.prana_lord
        )


# ============================================================
# Boundary Tests
# ============================================================

def test_first_deha_starts_at_prana_start():
    """First Deha must begin exactly at Prana start."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    assert (
        periods[0].start
        == pranadasha.start
    )


def test_last_deha_ends_at_prana_end():
    """Last Deha must end exactly at Prana end."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    assert (
        periods[-1].end
        == pranadasha.end
    )


def test_deha_periods_are_contiguous():
    """There must be no gaps or overlaps."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    for index in range(
        len(periods) - 1
    ):

        assert (
            periods[index].end
            == periods[index + 1].start
        )


def test_deha_periods_cover_entire_prana():
    """Deha periods must completely cover the parent Prana period."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    assert (
        periods[0].start
        == pranadasha.start
    )

    assert (
        periods[-1].end
        == pranadasha.end
    )


# ============================================================
# Duration Tests
# ============================================================

def test_deha_duration_is_positive():
    """Every Deha duration must be positive."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
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


def test_deha_duration_formula():
    """Verify the Vimshottari duration formula."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    expected_parent_years = (
        pranadasha.duration_days
        / 365.25
    )

    expected = (
        expected_parent_years
        * DASHA_YEARS["Saturn"]
        / VIMSHOTTARI_TOTAL_YEARS
    )

    actual = deha_duration_years(
        pranadasha,
        "Saturn",
    )

    assert actual == pytest.approx(
        expected
    )


def test_deha_durations_sum_to_parent():
    """All Deha durations should sum to the Prana duration."""

    pranadasha = make_pranadasha()

    periods = generate_dehadashas(
        pranadasha
    )

    total_days = sum(
        period.duration_days
        for period in periods
    )

    assert total_days == pytest.approx(
        pranadasha.duration_days,
        abs=1e-9,
    )


# ============================================================
# Current Deha Tests
# ============================================================

def test_current_dehadasha():
    """Current Deha should be identified correctly."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    periods = generate_dehadashas(
        pranadasha
    )

    moment = (
        periods[3].start
        + (
            periods[3].end
            - periods[3].start
        ) / 2
    )

    current = current_dehadasha(
        pranadasha,
        moment=moment,
    )

    assert (
        current.deha_lord
        == periods[3].deha_lord
    )


def test_current_deha_outside_parent_period():
    """A moment outside Prana should raise ValueError."""

    pranadasha = make_pranadasha()

    outside = (
        pranadasha.end
        + timedelta(
            seconds=1
        )
    )

    with pytest.raises(
        ValueError
    ):
        current_dehadasha(
            pranadasha,
            moment=outside,
        )


# ============================================================
# Generate All Tests
# ============================================================

def test_generate_all_dehadashas():
    """All supplied Prana Dashas should be expanded."""

    first = make_pranadasha(
        prana_lord="Saturn"
    )

    second_start = (
        first.end
    )

    second = make_pranadasha(
        prana_lord="Mercury",
        start=second_start,
        end=second_start
        + timedelta(
            days=9
        ),
    )

    periods = generate_all_dehadashas(
        [
            first,
            second,
        ]
    )

    assert len(periods) == 18


def test_all_deha_periods_belong_to_prana():
    """Generated periods must preserve their parent Prana lord."""

    pranadasha = make_pranadasha(
        prana_lord="Saturn"
    )

    periods = generate_dehadashas(
        pranadasha
    )

    for period in periods:

        assert (
            period.prana_lord
            == "Saturn"
        )


# ============================================================
# Validation Tests
# ============================================================

def test_invalid_pranadasha_type():
    """Invalid parent objects should raise TypeError."""

    with pytest.raises(
        TypeError
    ):
        generate_dehadashas(
            "invalid"
        )


def test_invalid_duration_parent():
    """Invalid parent objects should raise TypeError."""

    with pytest.raises(
        TypeError
    ):
        deha_duration_years(
            "invalid",
            "Saturn",
        )


def test_invalid_deha_planet():
    """Invalid Deha lord should raise ValueError."""

    pranadasha = make_pranadasha()

    with pytest.raises(
        ValueError
    ):
        deha_duration_years(
            pranadasha,
            "Pluto",
        )


def test_invalid_current_deha_parent():
    """Invalid parent should raise TypeError."""

    with pytest.raises(
        TypeError
    ):
        current_dehadasha(
            "invalid"
        )


def test_invalid_generate_all_type():
    """generate_all_dehadashas requires a list."""

    with pytest.raises(
        TypeError
    ):
        generate_all_dehadashas(
            "invalid"
        )


def test_deha_model_is_frozen():
    """DehaDasha should be immutable."""

    period = DehaDasha(
        mahadasha_lord="Saturn",
        antardasha_lord="Ketu",
        pratyantardasha_lord="Sun",
        sookshma_lord="Saturn",
        prana_lord="Saturn",
        deha_lord="Saturn",
        start=datetime(
            2026,
            8,
            2,
        ),
        end=datetime(
            2026,
            8,
            3,
        ),
    )

    with pytest.raises(
        AttributeError
    ):
        period.deha_lord = "Sun"
