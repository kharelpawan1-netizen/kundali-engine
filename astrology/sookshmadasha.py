"""
astrology/sookshmadasha.py

Vimshottari Sookshma Dasha calculation engine.

Hierarchy:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha
        ↓
    Sookshma Dasha

The Sookshma Dasha is calculated inside a single
Pratyantardasha using the classical Vimshottari
planetary sequence.

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
)

from astrology.pratyantardasha import (
    Pratyantardasha,
)


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class SookshmaDasha:
    """
    One Vimshottari Sookshma Dasha period.

    A Sookshma Dasha belongs to exactly one
    Pratyantardasha.
    """

    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: str
    sookshma_lord: str

    start: datetime
    end: datetime

    @property
    def duration_days(self) -> float:
        """Return the duration in days."""
        return (
            self.end - self.start
        ).total_seconds() / 86400.0

    @property
    def duration_years(self) -> float:
        """Return the duration in Vimshottari years."""
        return self.duration_days / 365.25

    def contains(
        self,
        moment: datetime,
    ) -> bool:
        """
        Return True if the supplied moment falls
        inside this Sookshma Dasha.
        """

        return (
            self.start <= moment < self.end
        )


# ============================================================
# Validation
# ============================================================

def _validate_pratyantardasha(
    pratyantardasha: Pratyantardasha,
) -> None:
    """
    Validate that the supplied object is a
    Pratyantardasha instance.
    """

    if not isinstance(
        pratyantardasha,
        Pratyantardasha,
    ):
        raise TypeError(
            "pratyantardasha must be a "
            "Pratyantardasha instance."
        )


def _validate_planet(
    planet: str,
) -> None:
    """Validate a Vimshottari planet."""

    if planet not in DASHA_SEQUENCE:
        raise ValueError(
            f"Unknown Vimshottari planet: {planet}"
        )


# ============================================================
# Sequence
# ============================================================

def sookshma_sequence(
    pratyantardasha_lord: str,
) -> List[str]:
    """
    Return the nine Sookshma Dasha lords.

    The sequence starts from the Pratyantardasha lord
    and follows the classical Vimshottari order.

    Example:

        Ketu -> Ketu, Venus, Sun, Moon, Mars,
                Rahu, Jupiter, Saturn, Mercury
    """

    _validate_planet(
        pratyantardasha_lord
    )

    starting_index = DASHA_SEQUENCE.index(
        pratyantardasha_lord
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
# Date Utility
# ============================================================

def _years_to_days(
    years: float,
) -> float:
    """
    Convert Vimshottari years into days.

    The engine uses 365.25 days per year,
    matching the existing Dasha implementation.
    """

    return years * 365.25


# ============================================================
# Sookshma Duration
# ============================================================

def sookshma_duration_years(
    pratyantardasha: Pratyantardasha,
    sookshma_lord: str,
) -> float:
    """
    Calculate the duration of one Sookshma Dasha.

    Formula:

        SD duration =
            PD duration
            ×
            SD lord years / 120

    The Pratyantardasha duration is measured
    in Vimshottari years.
    """

    _validate_pratyantardasha(
        pratyantardasha
    )

    _validate_planet(
        sookshma_lord
    )

    pd_duration_years = (
        pratyantardasha.duration_days
        / 365.25
    )

    return (
        pd_duration_years
        * DASHA_YEARS[sookshma_lord]
        / VIMSHOTTARI_TOTAL_YEARS
    )


# ============================================================
# Generate Sookshma Dashas
# ============================================================

def generate_sookshmadashas(
    pratyantardasha: Pratyantardasha,
) -> List[SookshmaDasha]:
    """
    Generate all nine Sookshma Dashas inside
    a single Pratyantardasha.

    The first Sookshma Dasha lord is the same as
    the Pratyantardasha lord.

    The nine periods are contiguous and together
    cover the complete Pratyantardasha.
    """

    _validate_pratyantardasha(
        pratyantardasha
    )

    sequence = sookshma_sequence(
        pratyantardasha.pratyantardasha_lord
    )

    periods: List[SookshmaDasha] = []

    current_start = (
        pratyantardasha.start
    )

    for index, lord in enumerate(
        sequence
    ):

        # ----------------------------------------------------
        # Calculate duration
        # ----------------------------------------------------

        duration_years = (
            sookshma_duration_years(
                pratyantardasha,
                lord,
            )
        )

        duration_days = _years_to_days(
            duration_years
        )

        # ----------------------------------------------------
        # Last period correction
        # ----------------------------------------------------
        #
        # Floating-point date arithmetic can otherwise
        # produce a tiny gap or overlap at the boundary.
        #
        # The final Sookshma Dasha must end exactly at
        # the parent Pratyantardasha end.
        #

        if index == len(sequence) - 1:

            current_end = (
                pratyantardasha.end
            )

        else:

            current_end = (
                current_start
                + timedelta(
                    days=duration_days
                )
            )

        periods.append(
            SookshmaDasha(
                mahadasha_lord=(
                    pratyantardasha
                    .mahadasha_lord
                ),
                antardasha_lord=(
                    pratyantardasha
                    .antardasha_lord
                ),
                pratyantardasha_lord=(
                    pratyantardasha
                    .pratyantardasha_lord
                ),
                sookshma_lord=lord,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


# ============================================================
# Current Sookshma Dasha
# ============================================================

def current_sookshmadasha(
    pratyantardasha: Pratyantardasha,
    moment: Optional[datetime] = None,
) -> SookshmaDasha:
    """
    Return the Sookshma Dasha active inside the
    supplied Pratyantardasha.

    Parameters
    ----------
    pratyantardasha:
        Parent Pratyantardasha.

    moment:
        Moment to evaluate.

        If omitted, the current system time is used,
        preserving the timezone of the parent period.
    """

    _validate_pratyantardasha(
        pratyantardasha
    )

    if moment is None:

        moment = datetime.now(
            tz=pratyantardasha
            .start
            .tzinfo
        )

    # --------------------------------------------------------
    # Validate moment against parent PD
    # --------------------------------------------------------

    if not (
        pratyantardasha.start
        <= moment
        < pratyantardasha.end
    ):

        raise ValueError(
            "Requested moment falls outside "
            "the supplied Pratyantardasha."
        )

    periods = (
        generate_sookshmadashas(
            pratyantardasha
        )
    )

    for period in periods:

        if period.contains(moment):

            return period

    raise ValueError(
        "Could not determine the current "
        "Sookshma Dasha."
    )


# ============================================================
# Generate All Sookshma Dashas for a PD List
# ============================================================

def generate_all_sookshmadashas(
    pratyantardashas: List[
        Pratyantardasha
    ],
) -> List[SookshmaDasha]:
    """
    Generate Sookshma Dashas for every supplied
    Pratyantardasha.

    This is useful when building a complete nested
    Dasha timeline.
    """

    if not isinstance(
        pratyantardashas,
        list,
    ):
        raise TypeError(
            "pratyantardashas must be a list."
        )

    periods: List[SookshmaDasha] = []

    for pratyantardasha in (
        pratyantardashas
    ):

        periods.extend(
            generate_sookshmadashas(
                pratyantardasha
            )
        )

    return periods


# ============================================================
# Public API
# ============================================================

__all__ = [
    "SookshmaDasha",
    "sookshma_sequence",
    "sookshma_duration_years",
    "generate_sookshmadashas",
    "current_sookshmadasha",
    "generate_all_sookshmadashas",
]