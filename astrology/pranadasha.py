"""
astrology/pranadasha.py

Vimshottari Prana Dasha calculation engine.

Hierarchy:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha
        ↓
    Sookshma Dasha
        ↓
    Prana Dasha

The Prana Dasha is calculated inside a single
Sookshma Dasha using the classical Vimshottari
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

from astrology.sookshmadasha import (
    SookshmaDasha,
)


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class PranaDasha:
    """
    One Vimshottari Prana Dasha period.

    A Prana Dasha belongs to exactly one
    Sookshma Dasha.
    """

    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: str
    sookshma_lord: str
    prana_lord: str

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
        inside this Prana Dasha.
        """

        return (
            self.start <= moment < self.end
        )


# ============================================================
# Validation
# ============================================================

def _validate_sookshmadasha(
    sookshmadasha: SookshmaDasha,
) -> None:
    """
    Validate that the supplied object is a
    SookshmaDasha instance.
    """

    if not isinstance(
        sookshmadasha,
        SookshmaDasha,
    ):
        raise TypeError(
            "sookshmadasha must be a "
            "SookshmaDasha instance."
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

def prana_sequence(
    sookshma_lord: str,
) -> List[str]:
    """
    Return the nine Prana Dasha lords.

    The sequence starts from the Sookshma Dasha
    lord and follows the classical Vimshottari order.

    Example:

        Saturn ->
        Saturn, Mercury, Ketu, Venus, Sun,
        Moon, Mars, Rahu, Jupiter
    """

    _validate_planet(
        sookshma_lord
    )

    starting_index = DASHA_SEQUENCE.index(
        sookshma_lord
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
# Prana Duration
# ============================================================

def prana_duration_years(
    sookshmadasha: SookshmaDasha,
    prana_lord: str,
) -> float:
    """
    Calculate the duration of one Prana Dasha.

    Formula:

        Prana duration =
            Sookshma duration
            ×
            Prana lord years / 120

    The Sookshma Dasha duration is measured
    in Vimshottari years.
    """

    _validate_sookshmadasha(
        sookshmadasha
    )

    _validate_planet(
        prana_lord
    )

    sd_duration_years = (
        sookshmadasha.duration_days
        / 365.25
    )

    return (
        sd_duration_years
        * DASHA_YEARS[prana_lord]
        / VIMSHOTTARI_TOTAL_YEARS
    )


# ============================================================
# Generate Prana Dashas
# ============================================================

def generate_pranadashas(
    sookshmadasha: SookshmaDasha,
) -> List[PranaDasha]:
    """
    Generate all nine Prana Dashas inside
    a single Sookshma Dasha.

    The first Prana Dasha lord is the same as
    the Sookshma Dasha lord.

    The nine periods are contiguous and together
    cover the complete Sookshma Dasha.
    """

    _validate_sookshmadasha(
        sookshmadasha
    )

    sequence = prana_sequence(
        sookshmadasha.sookshma_lord
    )

    periods: List[PranaDasha] = []

    current_start = (
        sookshmadasha.start
    )

    for index, lord in enumerate(
        sequence
    ):

        # ----------------------------------------------------
        # Calculate duration
        # ----------------------------------------------------

        duration_years = (
            prana_duration_years(
                sookshmadasha,
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
        # The final Prana Dasha must end exactly
        # at the parent Sookshma Dasha end.
        #

        if index == len(sequence) - 1:

            current_end = (
                sookshmadasha.end
            )

        else:

            current_end = (
                current_start
                + timedelta(
                    days=duration_days
                )
            )

        periods.append(
            PranaDasha(
                mahadasha_lord=(
                    sookshmadasha
                    .mahadasha_lord
                ),
                antardasha_lord=(
                    sookshmadasha
                    .antardasha_lord
                ),
                pratyantardasha_lord=(
                    sookshmadasha
                    .pratyantardasha_lord
                ),
                sookshma_lord=(
                    sookshmadasha
                    .sookshma_lord
                ),
                prana_lord=lord,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


# ============================================================
# Current Prana Dasha
# ============================================================

def current_pranadasha(
    sookshmadasha: SookshmaDasha,
    moment: Optional[datetime] = None,
) -> PranaDasha:
    """
    Return the Prana Dasha active inside the
    supplied Sookshma Dasha.

    Parameters
    ----------
    sookshmadasha:
        Parent Sookshma Dasha.

    moment:
        Moment to evaluate.

        If omitted, the current system time is used,
        preserving the timezone of the parent period.
    """

    _validate_sookshmadasha(
        sookshmadasha
    )

    if moment is None:

        moment = datetime.now(
            tz=sookshmadasha
            .start
            .tzinfo
        )

    # --------------------------------------------------------
    # Validate moment against parent SD
    # --------------------------------------------------------

    if not (
        sookshmadasha.start
        <= moment
        < sookshmadasha.end
    ):

        raise ValueError(
            "Requested moment falls outside "
            "the supplied Sookshma Dasha."
        )

    periods = (
        generate_pranadashas(
            sookshmadasha
        )
    )

    for period in periods:

        if period.contains(moment):

            return period

    raise ValueError(
        "Could not determine the current "
        "Prana Dasha."
    )


# ============================================================
# Generate All Prana Dashas for an SD List
# ============================================================

def generate_all_pranadashas(
    sookshmadashas: List[
        SookshmaDasha
    ],
) -> List[PranaDasha]:
    """
    Generate Prana Dashas for every supplied
    Sookshma Dasha.

    This is useful when building a complete
    nested Dasha timeline.
    """

    if not isinstance(
        sookshmadashas,
        list,
    ):
        raise TypeError(
            "sookshmadashas must be a list."
        )

    periods: List[PranaDasha] = []

    for sookshmadasha in (
        sookshmadashas
    ):

        periods.extend(
            generate_pranadashas(
                sookshmadasha
            )
        )

    return periods


# ============================================================
# Public API
# ============================================================

__all__ = [
    "PranaDasha",
    "prana_sequence",
    "prana_duration_years",
    "generate_pranadashas",
    "current_pranadasha",
    "generate_all_pranadashas",
]