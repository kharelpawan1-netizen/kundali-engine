
"""
astrology/dehadasha.py

Vimshottari Deha Dasha calculation engine.

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
        ↓
    Deha Dasha

The Deha Dasha is calculated inside a single
Prana Dasha using the classical Vimshottari
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

from astrology.pranadasha import (
    PranaDasha,
)


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class DehaDasha:
    """
    One Vimshottari Deha Dasha period.

    A Deha Dasha belongs to exactly one
    Prana Dasha.
    """

    mahadasha_lord: str
    antardasha_lord: str
    pratyantardasha_lord: str
    sookshma_lord: str
    prana_lord: str
    deha_lord: str

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
        inside this Deha Dasha.
        """

        return (
            self.start <= moment < self.end
        )


# ============================================================
# Validation
# ============================================================

def _validate_pranadasha(
    pranadasha: PranaDasha,
) -> None:
    """
    Validate that the supplied object is a
    PranaDasha instance.
    """

    if not isinstance(
        pranadasha,
        PranaDasha,
    ):
        raise TypeError(
            "pranadasha must be a "
            "PranaDasha instance."
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

def deha_sequence(
    prana_lord: str,
) -> List[str]:
    """
    Return the nine Deha Dasha lords.

    The sequence starts from the Prana Dasha lord
    and follows the classical Vimshottari order.

    Example:

        Saturn -> Saturn, Mercury, Ketu, Venus,
                  Sun, Moon, Mars, Rahu, Jupiter
    """

    _validate_planet(
        prana_lord
    )

    starting_index = DASHA_SEQUENCE.index(
        prana_lord
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
# Deha Duration
# ============================================================

def deha_duration_years(
    pranadasha: PranaDasha,
    deha_lord: str,
) -> float:
    """
    Calculate the duration of one Deha Dasha.

    Formula:

        Deha duration =
            Prana duration
            ×
            Deha lord years / 120

    The Prana Dasha duration is measured
    in Vimshottari years.
    """

    _validate_pranadasha(
        pranadasha
    )

    _validate_planet(
        deha_lord
    )

    prana_duration_years = (
        pranadasha.duration_days
        / 365.25
    )

    return (
        prana_duration_years
        * DASHA_YEARS[deha_lord]
        / VIMSHOTTARI_TOTAL_YEARS
    )


# ============================================================
# Generate Deha Dashas
# ============================================================

def generate_dehadashas(
    pranadasha: PranaDasha,
) -> List[DehaDasha]:
    """
    Generate all nine Deha Dashas inside
    a single Prana Dasha.

    The first Deha Dasha lord is the same as
    the Prana Dasha lord.

    The nine periods are contiguous and together
    cover the complete Prana Dasha.
    """

    _validate_pranadasha(
        pranadasha
    )

    sequence = deha_sequence(
        pranadasha.prana_lord
    )

    periods: List[DehaDasha] = []

    current_start = (
        pranadasha.start
    )

    for index, lord in enumerate(
        sequence
    ):

        # ----------------------------------------------------
        # Calculate duration
        # ----------------------------------------------------

        duration_years = (
            deha_duration_years(
                pranadasha,
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
        # The final Deha Dasha must end exactly at
        # the parent Prana Dasha end.
        #

        if index == len(sequence) - 1:

            current_end = (
                pranadasha.end
            )

        else:

            current_end = (
                current_start
                + timedelta(
                    days=duration_days
                )
            )

        periods.append(
            DehaDasha(
                mahadasha_lord=(
                    pranadasha
                    .mahadasha_lord
                ),
                antardasha_lord=(
                    pranadasha
                    .antardasha_lord
                ),
                pratyantardasha_lord=(
                    pranadasha
                    .pratyantardasha_lord
                ),
                sookshma_lord=(
                    pranadasha
                    .sookshma_lord
                ),
                prana_lord=(
                    pranadasha
                    .prana_lord
                ),
                deha_lord=lord,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


# ============================================================
# Current Deha Dasha
# ============================================================

def current_dehadasha(
    pranadasha: PranaDasha,
    moment: Optional[datetime] = None,
) -> DehaDasha:
    """
    Return the Deha Dasha active inside the
    supplied Prana Dasha.

    Parameters
    ----------
    pranadasha:
        Parent Prana Dasha.

    moment:
        Moment to evaluate.

        If omitted, the current system time is used,
        preserving the timezone of the parent period.
    """

    _validate_pranadasha(
        pranadasha
    )

    if moment is None:

        moment = datetime.now(
            tz=pranadasha
            .start
            .tzinfo
        )

    # --------------------------------------------------------
    # Validate moment against parent Prana Dasha
    # --------------------------------------------------------

    if not (
        pranadasha.start
        <= moment
        < pranadasha.end
    ):

        raise ValueError(
            "Requested moment falls outside "
            "the supplied Prana Dasha."
        )

    periods = (
        generate_dehadashas(
            pranadasha
        )
    )

    for period in periods:

        if period.contains(moment):

            return period

    raise ValueError(
        "Could not determine the current "
        "Deha Dasha."
    )


# ============================================================
# Generate All Deha Dashas for a Prana List
# ============================================================

def generate_all_dehadashas(
    pranadashas: List[
        PranaDasha
    ],
) -> List[DehaDasha]:
    """
    Generate Deha Dashas for every supplied
    Prana Dasha.

    This is useful when building a complete nested
    Dasha timeline.
    """

    if not isinstance(
        pranadashas,
        list,
    ):
        raise TypeError(
            "pranadashas must be a list."
        )

    periods: List[DehaDasha] = []

    for pranadasha in (
        pranadashas
    ):

        periods.extend(
            generate_dehadashas(
                pranadasha
            )
        )

    return periods


# ============================================================
# Public API
# ============================================================

__all__ = [
    "DehaDasha",
    "deha_sequence",
    "deha_duration_years",
    "generate_dehadashas",
    "current_dehadasha",
    "generate_all_dehadashas",
]
