"""
astrology/dasha.py

Vimshottari Dasha calculation engine.

Implements the classical 120-year Vimshottari Dasha system:

    Ketu       7 years
    Venus     20 years
    Sun        6 years
    Moon      10 years
    Mars       7 years
    Rahu      18 years
    Jupiter   16 years
    Saturn    19 years
    Mercury   17 years

The starting Mahadasha is determined by the Moon's Nakshatra.
The balance of the first Mahadasha is calculated from the Moon's
exact position within that Nakshatra.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


# ============================================================
# Constants
# ============================================================

NAKSHATRA_SPAN = 360.0 / 27.0
VIMSHOTTARI_TOTAL_YEARS = 120.0

NAKSHATRA_NAMES: Tuple[str, ...] = (
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
)

# Classical Vimshottari sequence.
DASHA_SEQUENCE: Tuple[str, ...] = (
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

DASHA_YEARS = {
    "Ketu": 7.0,
    "Venus": 20.0,
    "Sun": 6.0,
    "Moon": 10.0,
    "Mars": 7.0,
    "Rahu": 18.0,
    "Jupiter": 16.0,
    "Saturn": 19.0,
    "Mercury": 17.0,
}

# Nakshatra lords in zodiacal order.
NAKSHATRA_LORDS: Tuple[str, ...] = (
    "Ketu",       # Ashwini
    "Venus",      # Bharani
    "Sun",        # Krittika
    "Moon",       # Rohini
    "Mars",       # Mrigashira
    "Rahu",       # Ardra
    "Jupiter",    # Punarvasu
    "Saturn",     # Pushya
    "Mercury",    # Ashlesha
    "Ketu",       # Magha
    "Venus",      # Purva Phalguni
    "Sun",        # Uttara Phalguni
    "Moon",       # Hasta
    "Mars",       # Chitra
    "Rahu",       # Swati
    "Jupiter",    # Vishakha
    "Saturn",     # Anuradha
    "Mercury",    # Jyeshtha
    "Ketu",       # Mula
    "Venus",      # Purva Ashadha
    "Sun",        # Uttara Ashadha
    "Moon",       # Shravana
    "Mars",       # Dhanishta
    "Rahu",       # Shatabhisha
    "Jupiter",    # Purva Bhadrapada
    "Saturn",     # Uttara Bhadrapada
    "Mercury",    # Revati
)


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class Mahadasha:
    """One Vimshottari Mahadasha period."""

    planet: str
    duration_years: float
    start: datetime
    end: datetime

    @property
    def duration_days(self) -> float:
        """Return duration in days."""
        return (self.end - self.start).total_seconds() / 86400.0

    def contains(self, moment: datetime) -> bool:
        """Return True when moment falls inside this period."""
        return self.start <= moment < self.end


@dataclass(frozen=True)
class Antardasha:
    """One Antardasha period within a Mahadasha."""

    mahadasha_lord: str
    antardasha_lord: str
    start: datetime
    end: datetime

    @property
    def duration_days(self) -> float:
        """Return duration in days."""
        return (self.end - self.start).total_seconds() / 86400.0

    def contains(self, moment: datetime) -> bool:
        """Return True when moment falls inside this period."""
        return self.start <= moment < self.end


# ============================================================
# Validation
# ============================================================

def normalize_longitude(longitude: float) -> float:
    """Normalize longitude to the range [0, 360)."""
    return longitude % 360.0


def validate_moon_longitude(moon_longitude: float) -> float:
    """
    Validate and normalize Moon longitude.

    Valid input:
        0 <= longitude <= 360

    Exactly 360 degrees is treated as 0 degrees.
    """
    if not isinstance(moon_longitude, (int, float)):
        raise TypeError("Moon longitude must be numeric.")

    if not 0.0 <= moon_longitude <= 360.0:
        raise ValueError(
            "Moon longitude must be between 0 and 360 degrees."
        )

    if moon_longitude == 360.0:
        return 0.0

    return normalize_longitude(float(moon_longitude))


# ============================================================
# Nakshatra
# ============================================================

def nakshatra_index(moon_longitude: float) -> int:
    """
    Return the zero-based Nakshatra index.

    Ashwini = 0
    Bharani = 1
    ...
    Revati = 26
    """
    longitude = validate_moon_longitude(moon_longitude)

    index = int(longitude / NAKSHATRA_SPAN)

    return min(index, 26)


def nakshatra_number(moon_longitude: float) -> int:
    """Return Nakshatra number from 1 to 27."""
    return nakshatra_index(moon_longitude) + 1


def nakshatra_name(moon_longitude: float) -> str:
    """Return the traditional Nakshatra name."""
    return NAKSHATRA_NAMES[nakshatra_index(moon_longitude)]


def nakshatra_lord(moon_longitude: float) -> str:
    """Return the Vimshottari lord of the Moon's Nakshatra."""
    return NAKSHATRA_LORDS[nakshatra_index(moon_longitude)]


# ============================================================
# Mahadasha Calculations
# ============================================================

def dasha_years(planet: str) -> float:
    """Return the classical Vimshottari duration of a planet."""
    try:
        return DASHA_YEARS[planet]
    except KeyError as exc:
        raise ValueError(
            f"Unknown Vimshottari planet: {planet}"
        ) from exc


def next_dasha_lord(planet: str) -> str:
    """Return the next planet in the Vimshottari sequence."""
    try:
        index = DASHA_SEQUENCE.index(planet)
    except ValueError as exc:
        raise ValueError(
            f"Unknown Vimshottari planet: {planet}"
        ) from exc

    return DASHA_SEQUENCE[
        (index + 1) % len(DASHA_SEQUENCE)
    ]


def moon_nakshatra_progress(moon_longitude: float) -> float:
    """
    Return the fraction of the Moon's Nakshatra already traversed.

    Returns:
        0.0 <= progress < 1.0
    """
    longitude = validate_moon_longitude(moon_longitude)

    position_in_nakshatra = longitude % NAKSHATRA_SPAN

    return position_in_nakshatra / NAKSHATRA_SPAN


def first_mahadasha_balance(moon_longitude: float) -> float:
    """
    Calculate remaining years of the starting Mahadasha.

    Formula:

        balance =
            Mahadasha years *
            remaining Nakshatra fraction
    """
    lord = nakshatra_lord(moon_longitude)

    elapsed_fraction = moon_nakshatra_progress(
        moon_longitude
    )

    remaining_fraction = 1.0 - elapsed_fraction

    return dasha_years(lord) * remaining_fraction


# ============================================================
# Date Utilities
# ============================================================

def years_to_days(years: float) -> float:
    """
    Convert Vimshottari years to days.

    This implementation uses 365.25 days per year for
    astronomical date projection.
    """
    if not isinstance(years, (int, float)):
        raise TypeError("Years must be numeric.")

    if years < 0:
        raise ValueError("Years cannot be negative.")

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
# Mahadasha Timeline
# ============================================================

def generate_mahadashas(
    birth_datetime: datetime,
    moon_longitude: float,
    count: int = 9,
) -> List[Mahadasha]:
    """
    Generate Vimshottari Mahadasha periods beginning at birth.

    The first Mahadasha is the lord of the Moon's Nakshatra.
    Its duration is only the remaining balance at birth.

    Later Mahadashas use their full classical durations.
    """
    if not isinstance(birth_datetime, datetime):
        raise TypeError(
            "birth_datetime must be a datetime."
        )

    if count <= 0:
        raise ValueError(
            "count must be greater than zero."
        )

    starting_lord = nakshatra_lord(moon_longitude)
    starting_index = DASHA_SEQUENCE.index(
        starting_lord
    )

    balance = first_mahadasha_balance(
        moon_longitude
    )

    periods: List[Mahadasha] = []

    current_start = birth_datetime

    for index in range(count):
        lord = DASHA_SEQUENCE[
            (starting_index + index)
            % len(DASHA_SEQUENCE)
        ]

        if index == 0:
            duration = balance
        else:
            duration = dasha_years(lord)

        current_end = add_years_fraction(
            current_start,
            duration,
        )

        periods.append(
            Mahadasha(
                planet=lord,
                duration_years=duration,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


def current_mahadasha(
    birth_datetime: datetime,
    moon_longitude: float,
    moment: Optional[datetime] = None,
) -> Mahadasha:
    """Return the Mahadasha active at the requested moment."""
    if moment is None:
        moment = datetime.now(
            tz=birth_datetime.tzinfo
        )

    periods = generate_mahadashas(
        birth_datetime,
        moon_longitude,
        count=18,
    )

    for period in periods:
        if period.contains(moment):
            return period

    raise ValueError(
        "Requested moment falls outside the "
        "generated Mahadasha timeline."
    )


# ============================================================
# Antardasha
# ============================================================

def generate_antardashas(
    mahadasha: Mahadasha,
) -> List[Antardasha]:
    """
    Generate all nine Antardashas inside a Mahadasha.

    The sequence starts with the Mahadasha lord and follows
    the normal Vimshottari order.

    Formula:

        AD duration =
            MD duration *
            AD lord years / 120
    """
    if not isinstance(mahadasha, Mahadasha):
        raise TypeError(
            "mahadasha must be a Mahadasha instance."
        )

    starting_index = DASHA_SEQUENCE.index(
        mahadasha.planet
    )

    periods: List[Antardasha] = []

    current_start = mahadasha.start

    for index in range(len(DASHA_SEQUENCE)):
        lord = DASHA_SEQUENCE[
            (starting_index + index)
            % len(DASHA_SEQUENCE)
        ]

        duration_years = (
            mahadasha.duration_years
            * dasha_years(lord)
            / VIMSHOTTARI_TOTAL_YEARS
        )

        current_end = add_years_fraction(
            current_start,
            duration_years,
        )

        periods.append(
            Antardasha(
                mahadasha_lord=mahadasha.planet,
                antardasha_lord=lord,
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


def current_antardasha(
    birth_datetime: datetime,
    moon_longitude: float,
    moment: Optional[datetime] = None,
) -> Antardasha:
    """Return the Antardasha active at the requested moment."""
    if moment is None:
        moment = datetime.now(
            tz=birth_datetime.tzinfo
        )

    mahadasha = current_mahadasha(
        birth_datetime,
        moon_longitude,
        moment,
    )

    antardashas = generate_antardashas(
        mahadasha
    )

    for period in antardashas:
        if period.contains(moment):
            return period

    raise ValueError(
        "Requested moment falls outside the "
        "generated Antardasha timeline."
    )


# ============================================================
# Public API
# ============================================================

__all__ = [
    "NAKSHATRA_SPAN",
    "VIMSHOTTARI_TOTAL_YEARS",
    "NAKSHATRA_NAMES",
    "DASHA_SEQUENCE",
    "DASHA_YEARS",
    "NAKSHATRA_LORDS",
    "Mahadasha",
    "Antardasha",
    "normalize_longitude",
    "validate_moon_longitude",
    "nakshatra_index",
    "nakshatra_number",
    "nakshatra_name",
    "nakshatra_lord",
    "dasha_years",
    "next_dasha_lord",
    "moon_nakshatra_progress",
    "first_mahadasha_balance",
    "years_to_days",
    "add_years_fraction",
    "generate_mahadashas",
    "current_mahadasha",
    "generate_antardashas",
    "current_antardasha",
]