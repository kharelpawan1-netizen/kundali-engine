"""
astrology/pratyantardasha.py

Vimshottari Pratyantardasha calculation engine.

Calculates the third-level Vimshottari Dasha periods:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha

The implementation uses the existing Mahadasha and Antardasha
models from astrology.dasha.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from astrology.dasha import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    VIMSHOTTARI_TOTAL_YEARS,
    Antardasha,
    Mahadasha,
)


# ============================================================
# Constants
# ============================================================

DAYS_PER_YEAR = 365.25


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class Pratyantardasha:
    """
    One Pratyantardasha period.

    A Pratyantardasha is the third Vimshottari Dasha level:

        Mahadasha → Antardasha → Pratyantardasha
    """

    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: str

    start: datetime
    end: datetime

    @property
    def duration_days(self) -> float:
        """Return the duration of the period in days."""

        return (
            self.end - self.start
        ).total_seconds() / 86400.0

    @property
    def duration_years(self) -> float:
        """Return the duration in Vimshottari years."""

        return self.duration_days / DAYS_PER_YEAR

    def contains(
        self,
        moment: datetime,
    ) -> bool:
        """
        Return True if the supplied moment falls
        inside this period.

        The start boundary is inclusive and the end
        boundary is exclusive.
        """

        return (
            self.start <= moment < self.end
        )


# ============================================================
# Validation
# ============================================================

def _validate_planet(
    planet: str,
) -> None:
    """Validate a Vimshottari planet."""

    if not isinstance(planet, str):
        raise TypeError(
            "Vimshottari planet must be a string."
        )

    if planet not in DASHA_YEARS:
        raise ValueError(
            f"Unknown Vimshottari planet: {planet}"
        )


def _validate_antardasha(
    antardasha: Antardasha,
) -> None:
    """
    Validate an Antardasha instance and its
    Vimshottari hierarchy.
    """

    if not isinstance(
        antardasha,
        Antardasha,
    ):
        raise TypeError(
            "antardasha must be an Antardasha instance."
        )

    _validate_planet(
        antardasha.mahadasha_lord
    )

    _validate_planet(
        antardasha.antardasha_lord
    )

    if not isinstance(
        antardasha.start,
        datetime,
    ):
        raise TypeError(
            "antardasha.start must be a datetime."
        )

    if not isinstance(
        antardasha.end,
        datetime,
    ):
        raise TypeError(
            "antardasha.end must be a datetime."
        )

    if antardasha.end <= antardasha.start:
        raise ValueError(
            "Antardasha end must be later than "
            "Antardasha start."
        )

    if (
        antardasha.start.tzinfo is None
        and antardasha.end.tzinfo is not None
    ) or (
        antardasha.start.tzinfo is not None
        and antardasha.end.tzinfo is None
    ):
        raise ValueError(
            "Antardasha start and end must both be "
            "timezone-naive or both be timezone-aware."
        )


def _validate_moment_against_period(
    moment: datetime,
    start: datetime,
    end: datetime,
) -> None:
    """
    Validate that a datetime can safely be compared
    with the supplied period.
    """

    if not isinstance(moment, datetime):
        raise TypeError(
            "moment must be a datetime."
        )

    if (
        moment.tzinfo is None
        and start.tzinfo is not None
    ) or (
        moment.tzinfo is not None
        and start.tzinfo is None
    ):
        raise ValueError(
            "moment timezone-awareness must match "
            "the parent Dasha period."
        )

    if (
        moment.tzinfo is None
        and end.tzinfo is not None
    ) or (
        moment.tzinfo is not None
        and end.tzinfo is None
    ):
        raise ValueError(
            "moment timezone-awareness must match "
            "the parent Dasha period."
        )


# ============================================================
# Date Utilities
# ============================================================

def years_to_days(
    years: float,
) -> float:
    """
    Convert Vimshottari years to days.

    Uses the same 365.25-day year convention as
    astrology.dasha.
    """

    if not isinstance(
        years,
        (int, float),
    ):
        raise TypeError(
            "years must be numeric."
        )

    if years < 0:
        raise ValueError(
            "years cannot be negative."
        )

    return float(years) * DAYS_PER_YEAR


def add_years_fraction(
    moment: datetime,
    years: float,
) -> datetime:
    """Add fractional Vimshottari years to a datetime."""

    if not isinstance(
        moment,
        datetime,
    ):
        raise TypeError(
            "moment must be a datetime."
        )

    return moment + timedelta(
        days=years_to_days(years)
    )


# ============================================================
# Pratyantardasha Duration
# ============================================================

def pratyantardasha_duration_years(
    antardasha: Antardasha,
    pratyantardasha_lord: str,
) -> float:
    """
    Calculate the duration of one Pratyantardasha.

    Formula:

        PD duration =
            AD duration
            ×
            PD lord years
            /
            120

    Parameters
    ----------
    antardasha:
        Parent Antardasha.

    pratyantardasha_lord:
        Lord of the Pratyantardasha.

    Returns
    -------
    float
        Duration in Vimshottari years.
    """

    _validate_antardasha(
        antardasha
    )

    _validate_planet(
        pratyantardasha_lord
    )

    antardasha_duration_years = (
        antardasha.duration_days
        / DAYS_PER_YEAR
    )

    return (
        antardasha_duration_years
        * DASHA_YEARS[
            pratyantardasha_lord
        ]
        / VIMSHOTTARI_TOTAL_YEARS
    )


# ============================================================
# Pratyantardasha Sequence
# ============================================================

def pratyantardasha_sequence(
    antardasha_lord: str,
) -> List[str]:
    """
    Return the nine Pratyantardasha lords.

    The sequence begins with the Antardasha lord and
    follows the standard Vimshottari order.

    Example:

        Saturn Antardasha:

        Saturn → Mercury → Ketu → Venus → Sun
        → Moon → Mars → Rahu → Jupiter
    """

    _validate_planet(
        antardasha_lord
    )

    starting_index = DASHA_SEQUENCE.index(
        antardasha_lord
    )

    return [
        DASHA_SEQUENCE[
            (
                starting_index + index
            ) % len(DASHA_SEQUENCE)
        ]
        for index in range(
            len(DASHA_SEQUENCE)
        )
    ]


# ============================================================
# Generate Pratyantardashas
# ============================================================

def generate_pratyantardashas(
    antardasha: Antardasha,
) -> List[Pratyantardasha]:
    """
    Generate all nine Pratyantardashas within
    an Antardasha.

    The first Pratyantardasha is ruled by the
    Antardasha lord.

    The generated periods are contiguous and
    partition the complete parent Antardasha.
    """

    _validate_antardasha(
        antardasha
    )

    sequence = pratyantardasha_sequence(
        antardasha.antardasha_lord
    )

    periods: List[Pratyantardasha] = []

    current_start = antardasha.start

    parent_duration_days = (
        antardasha.end
        - antardasha.start
    ).total_seconds() / 86400.0

    for index, lord in enumerate(
        sequence
    ):

        fraction = (
            DASHA_YEARS[lord]
            / VIMSHOTTARI_TOTAL_YEARS
        )

        duration_days = (
            parent_duration_days
            * fraction
        )

        if index == len(sequence) - 1:
            current_end = antardasha.end
        else:
            current_end = (
                current_start
                + timedelta(
                    days=duration_days
                )
            )

        periods.append(
            Pratyantardasha(
                mahadasha_lord=(
                    antardasha.mahadasha_lord
                ),
                antardasha_lord=(
                    antardasha.antardasha_lord
                ),
                pratyantardasha_lord=lord,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


# ============================================================
# Current Pratyantardasha
# ============================================================

def current_pratyantardasha(
    antardasha: Antardasha,
    moment: Optional[datetime] = None,
) -> Pratyantardasha:
    """
    Return the Pratyantardasha active at a given moment.

    Parameters
    ----------
    antardasha:
        Parent Antardasha.

    moment:
        Datetime to evaluate.

        If omitted, the current system time is used
        with the timezone attached to the Antardasha
        start datetime.

    Returns
    -------
    Pratyantardasha
        Active Pratyantardasha.
    """

    _validate_antardasha(
        antardasha
    )

    if moment is None:
        moment = datetime.now(
            tz=antardasha.start.tzinfo
        )

    _validate_moment_against_period(
        moment,
        antardasha.start,
        antardasha.end,
    )

    if not (
        antardasha.start
        <= moment
        < antardasha.end
    ):
        raise ValueError(
            "Requested moment falls outside "
            "the Antardasha period."
        )

    periods = generate_pratyantardashas(
        antardasha
    )

    for period in periods:
        if period.contains(moment):
            return period

    raise ValueError(
        "Could not determine the active "
        "Pratyantardasha."
    )


# ============================================================
# Convenience: Generate from Mahadasha
# ============================================================

def generate_all_pratyantardashas(
    mahadasha: Mahadasha,
) -> List[Pratyantardasha]:
    """
    Generate Pratyantardashas for every Antardasha
    belonging to a Mahadasha.

    This is useful when constructing a complete
    Dasha timeline for reporting.
    """

    if not isinstance(
        mahadasha,
        Mahadasha,
    ):
        raise TypeError(
            "mahadasha must be a Mahadasha instance."
        )

    from astrology.dasha import generate_antardashas

    antardashas = generate_antardashas(
        mahadasha
    )

    result: List[Pratyantardasha] = []

    for antardasha in antardashas:
        result.extend(
            generate_pratyantardashas(
                antardasha
            )
        )

    return result


# ============================================================
# Public API
# ============================================================

__all__ = [
    "Pratyantardasha",
    "years_to_days",
    "add_years_fraction",
    "pratyantardasha_duration_years",
    "pratyantardasha_sequence",
    "generate_pratyantardashas",
    "current_pratyantardasha",
    "generate_all_pratyantardashas",
]