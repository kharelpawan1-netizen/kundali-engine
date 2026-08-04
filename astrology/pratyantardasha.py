
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

    def contains(self, moment: datetime) -> bool:
        """Return True if moment falls inside this period."""

        return self.start <= moment < self.end


# ============================================================
# Validation
# ============================================================

def _validate_planet(planet: str) -> None:
    """Validate a Vimshottari planet."""

    if planet not in DASHA_YEARS:
        raise ValueError(
            f"Unknown Vimshottari planet: {planet}"
        )


def _validate_antardasha(
    antardasha: Antardasha,
) -> None:
    """Validate an Antardasha instance."""

    if not isinstance(antardasha, Antardasha):
        raise TypeError(
            "antardasha must be an Antardasha instance."
        )

    _validate_planet(antardasha.mahadasha_lord)
    _validate_planet(antardasha.antardasha_lord)


# ============================================================
# Date Utilities
# ============================================================

def years_to_days(years: float) -> float:
    """
    Convert Vimshottari years to days.

    Uses the same 365.25-day year convention as dasha.py.
    """

    if not isinstance(years, (int, float)):
        raise TypeError(
            "years must be numeric."
        )

    if years < 0:
        raise ValueError(
            "years cannot be negative."
        )

    return float(years) * 365.25


def add_years_fraction(
    moment: datetime,
    years: float,
) -> datetime:
    """Add fractional Vimshottari years to a datetime."""

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

    _validate_antardasha(antardasha)
    _validate_planet(pratyantardasha_lord)

    return (
        antardasha.duration_days
        / 365.25
        * DASHA_YEARS[pratyantardasha_lord]
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

    The sequence begins with the Antardasha lord and then
    follows the standard Vimshottari order.

    Example:

        Saturn Antardasha:

        Saturn → Mercury → Ketu → Venus → Sun
        → Moon → Mars → Rahu → Jupiter
    """

    _validate_planet(antardasha_lord)

    starting_index = DASHA_SEQUENCE.index(
        antardasha_lord
    )

    return [
        DASHA_SEQUENCE[
            (starting_index + index)
            % len(DASHA_SEQUENCE)
        ]
        for index in range(len(DASHA_SEQUENCE))
    ]


# ============================================================
# Generate Pratyantardashas
# ============================================================

def generate_pratyantardashas(
    antardasha: Antardasha,
) -> List[Pratyantardasha]:
    """
    Generate all nine Pratyantardashas within an Antardasha.

    The first Pratyantardasha is ruled by the Antardasha lord.

    The sequence then follows:

        Ketu
        Venus
        Sun
        Moon
        Mars
        Rahu
        Jupiter
        Saturn
        Mercury

    rotated so that the Antardasha lord comes first.
    """

    _validate_antardasha(antardasha)

    sequence = pratyantardasha_sequence(
        antardasha.antardasha_lord
    )

    periods: List[Pratyantardasha] = []

    current_start = antardasha.start

    # Use the actual Antardasha duration rather than
    # independently reconstructing it from the parent
    # Mahadasha. This guarantees that the generated
    # Pratyantardashas exactly partition the AD.
    antardasha_duration_days = (
        antardasha.end - antardasha.start
    ).total_seconds() / 86400.0

    for lord in sequence:

        fraction = (
            DASHA_YEARS[lord]
            / VIMSHOTTARI_TOTAL_YEARS
        )

        duration_days = (
            antardasha_duration_days
            * fraction
        )

        current_end = current_start + timedelta(
            days=duration_days
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

    # Avoid floating-point accumulation leaving a tiny
    # gap between the final PD and the parent AD.
    if periods:
        final_period = periods[-1]

        periods[-1] = Pratyantardasha(
            mahadasha_lord=(
                final_period.mahadasha_lord
            ),
            antardasha_lord=(
                final_period.antardasha_lord
            ),
            pratyantardasha_lord=(
                final_period.pratyantardasha_lord
            ),
            start=final_period.start,
            end=antardasha.end,
        )

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

        If omitted, the current time is used using the
        timezone attached to the Antardasha start datetime.

    Returns
    -------
    Pratyantardasha
        Currently active Pratyantardasha.
    """

    _validate_antardasha(antardasha)

    if moment is None:
        moment = datetime.now(
            tz=antardasha.start.tzinfo
        )

    periods = generate_pratyantardashas(
        antardasha
    )

    for period in periods:
        if period.contains(moment):
            return period

    raise ValueError(
        "Requested moment falls outside the "
        "Antardasha period."
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

    from astrology.dasha import generate_antardashas

    if not isinstance(mahadasha, Mahadasha):
        raise TypeError(
            "mahadasha must be a Mahadasha instance."
        )

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
