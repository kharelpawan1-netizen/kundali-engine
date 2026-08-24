"""
astrology/sade_sati.py

Shani Sade Sati calculation engine.

Classical structural definition:

    Sade Sati begins when transiting Saturn enters the sign
    twelfth from the natal Moon, continues while Saturn transits
    the Moon's own sign, and completes while Saturn transits the
    sign second from the natal Moon.

    Three classical phases:

        Rising Phase   Saturn in the 12th house from Moon
        Peak Phase     Saturn in the Moon's own sign (1st house)
        Setting Phase  Saturn in the 2nd house from Moon

    Saturn transits one zodiac sign in approximately two and a
    half years. Three such transits give the complete cycle its
    classical name -- "Sade Sati" means "seven and a half"
    (years).

This module evaluates the structural sign relationship between
transiting Saturn and the natal Moon, consistent with the
whole-sign approach used elsewhere in this engine.

It does NOT evaluate:
    - exact Saturn ingress/egress dates from an ephemeris
    - retrogression loops (Saturn can re-enter or re-exit a
      sign more than once near a sign boundary)
    - planetary strength, dignity, or combustion
    - aspects
    - individual house lordships
    - sub-period (Antardasha-style) timing refinements
    - manifestation / results

Those concerns belong to later ephemeris and interpretation
layers. The ~2.5 year phase length used by the timeline
generators in this module is the classical approximation, not a
substitute for actual Saturn ephemeris longitudes.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Constants
# ============================================================

SADE_SATI_NAME = "Shani Sade Sati"

MOON = "Moon"
SATURN = "Saturn"

ZODIAC_SIGNS: Tuple[str, ...] = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)

RISING_PHASE = "Rising Phase"
PEAK_PHASE = "Peak Phase"
SETTING_PHASE = "Setting Phase"

# Classical phase order, starting from the sign 12th from Moon.
SADE_SATI_PHASES: Tuple[str, ...] = (
    RISING_PHASE,
    PEAK_PHASE,
    SETTING_PHASE,
)

# Classical approximate duration of one Saturn sign transit.
SATURN_PHASE_YEARS = 2.5

# Classical total duration of the complete Sade Sati cycle.
SADE_SATI_TOTAL_YEARS = 7.5

DAYS_PER_YEAR = 365.25


# ============================================================
# Validation
# ============================================================

def _validate_sign(
    sign: str,
    label: str = "sign",
) -> str:
    """Validate a zodiac sign name."""

    if not isinstance(sign, str):
        raise TypeError(
            f"{label} must be a string."
        )

    if sign not in ZODIAC_SIGNS:
        raise ValueError(
            f"Unknown zodiac sign for {label}: {sign!r}"
        )

    return sign


def sign_index(sign: str) -> int:
    """Return the zero-based zodiac sign index."""

    _validate_sign(sign)

    return ZODIAC_SIGNS.index(sign)


def sign_from_index(index: int) -> str:
    """Return the zodiac sign name for a (possibly unbounded) index."""

    return ZODIAC_SIGNS[index % 12]


# ============================================================
# House From Moon
# ============================================================

def house_from_moon(
    moon_sign: str,
    saturn_sign: str,
) -> int:
    """
    Return the whole-sign house distance of Saturn's sign,
    counted from the Moon's sign.

    The Moon's own sign is house 1.
    """

    _validate_sign(moon_sign, "moon_sign")
    _validate_sign(saturn_sign, "saturn_sign")

    return (
        (
            sign_index(saturn_sign)
            - sign_index(moon_sign)
        )
        % 12
    ) + 1


# ============================================================
# Sade Sati Signs
# ============================================================

def sade_sati_signs(
    moon_sign: str,
) -> List[str]:
    """
    Return the three Sade Sati signs for a Moon sign, in
    classical phase order.

    [12th-from-Moon, Moon's own sign, 2nd-from-Moon]
    """

    _validate_sign(moon_sign, "moon_sign")

    index = sign_index(moon_sign)

    return [
        sign_from_index(index - 1),
        sign_from_index(index),
        sign_from_index(index + 1),
    ]


# ============================================================
# Phase Detection
# ============================================================

def sade_sati_phase_name(
    moon_sign: str,
    saturn_sign: str,
) -> Optional[str]:
    """
    Return the Sade Sati phase name for the supplied Moon and
    Saturn signs.

    Returns None when Saturn is not structurally within a Sade
    Sati phase.
    """

    house = house_from_moon(
        moon_sign,
        saturn_sign,
    )

    if house == 12:
        return RISING_PHASE

    if house == 1:
        return PEAK_PHASE

    if house == 2:
        return SETTING_PHASE

    return None


def is_sade_sati_active(
    moon_sign: str,
    saturn_sign: str,
) -> bool:
    """Return True when Sade Sati is structurally active."""

    return (
        sade_sati_phase_name(
            moon_sign,
            saturn_sign,
        )
        is not None
    )


# ============================================================
# Evidence
# ============================================================

def sade_sati_evidence(
    moon_sign: str,
    saturn_sign: str,
) -> List[Dict[str, Any]]:
    """
    Return structural evidence for Sade Sati.

    When Saturn structurally occupies a Sade Sati phase relative
    to the Moon, one evidence dictionary is returned.

    Otherwise an empty list is returned.
    """

    phase = sade_sati_phase_name(
        moon_sign,
        saturn_sign,
    )

    if phase is None:
        return []

    return [
        {
            "phase": phase,
            "moon_sign": moon_sign,
            "saturn_sign": saturn_sign,
            "house_from_moon": house_from_moon(
                moon_sign,
                saturn_sign,
            ),
        }
    ]


# ============================================================
# Context Helpers
# ============================================================
#
# These mirror the small context helpers used by the Yoga
# engine (yogas/context.py), kept local so this module has no
# dependency on the yogas package.
#

def _context_planet_sign(
    context: Any,
    planet_name: str,
) -> Optional[str]:
    """Return a planet's sign from an InterpretationContext-like object."""

    planets = getattr(
        context,
        "planets",
        None,
    )

    if not planets:
        return None

    value = planets.get(planet_name)

    if value is None:
        return None

    sign = getattr(
        value,
        "sign",
        None,
    )

    if sign is None:
        return None

    return str(sign)


def moon_and_saturn_signs_from_context(
    context: Any,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Return (moon_sign, saturn_sign) from a context object.

    Either value is None when unavailable.
    """

    return (
        _context_planet_sign(context, MOON),
        _context_planet_sign(context, SATURN),
    )


def detect_sade_sati_from_context(
    context: Any,
) -> Optional[str]:
    """
    Return the active Sade Sati phase name from a context
    object, or None when Sade Sati is not structurally active
    or the required sign data is unavailable.
    """

    moon_sign, saturn_sign = (
        moon_and_saturn_signs_from_context(
            context
        )
    )

    if moon_sign is None or saturn_sign is None:
        return None

    return sade_sati_phase_name(
        moon_sign,
        saturn_sign,
    )


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class SadeSatiPeriod:
    """One classical Sade Sati phase period."""

    phase: str
    saturn_sign: str
    moon_sign: str
    house_from_moon: int

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
        """Return the duration in years (365.25 day years)."""

        return self.duration_days / DAYS_PER_YEAR

    def contains(
        self,
        moment: datetime,
    ) -> bool:
        """Return True when moment falls inside this period."""

        return self.start <= moment < self.end


# ============================================================
# Timeline Generation
# ============================================================

def _years_to_days(years: float) -> float:
    """Convert years into days using the engine's 365.25 day year."""

    return years * DAYS_PER_YEAR


def generate_sade_sati_periods(
    moon_sign: str,
    cycle_start: datetime,
    phase_years: float = SATURN_PHASE_YEARS,
) -> List[SadeSatiPeriod]:
    """
    Generate the three classical Sade Sati periods for one Moon
    sign, starting at `cycle_start`.

    Parameters
    ----------
    moon_sign:
        The natal Moon sign.

    cycle_start:
        The moment Saturn is taken to enter the sign 12th from
        the Moon (the start of the Rising Phase).

    phase_years:
        Classical approximate duration of one phase, in years.
        Defaults to 2.5 years, matching the traditional "seven
        and a half year" cycle. Callers with real Saturn
        ephemeris ingress dates may build periods directly
        instead of relying on this approximation.

    Returns
    -------
    List[SadeSatiPeriod]
        Three contiguous periods: Rising, Peak, Setting.
    """

    _validate_sign(moon_sign, "moon_sign")

    if not isinstance(cycle_start, datetime):
        raise TypeError(
            "cycle_start must be a datetime."
        )

    if phase_years <= 0:
        raise ValueError(
            "phase_years must be positive."
        )

    signs = sade_sati_signs(moon_sign)

    duration_days = _years_to_days(phase_years)

    periods: List[SadeSatiPeriod] = []

    current_start = cycle_start

    for phase_name, saturn_sign in zip(
        SADE_SATI_PHASES,
        signs,
    ):

        current_end = (
            current_start
            + timedelta(days=duration_days)
        )

        periods.append(
            SadeSatiPeriod(
                phase=phase_name,
                saturn_sign=saturn_sign,
                moon_sign=moon_sign,
                house_from_moon=house_from_moon(
                    moon_sign,
                    saturn_sign,
                ),
                start=current_start,
                end=current_end,
            )
        )

        current_start = current_end

    return periods


def current_sade_sati_period(
    periods: List[SadeSatiPeriod],
    moment: Optional[datetime] = None,
) -> Optional[SadeSatiPeriod]:
    """
    Return the period from `periods` that contains `moment`.

    Returns None when no period contains the moment (Sade Sati
    is not active at that moment) or when `periods` is empty.
    """

    if not periods:
        return None

    if moment is None:

        moment = datetime.now(
            tz=periods[0].start.tzinfo
        )

    for period in periods:

        if period.contains(moment):

            return period

    return None


# ============================================================
# Public API
# ============================================================

__all__ = [
    "SADE_SATI_NAME",
    "MOON",
    "SATURN",
    "ZODIAC_SIGNS",
    "RISING_PHASE",
    "PEAK_PHASE",
    "SETTING_PHASE",
    "SADE_SATI_PHASES",
    "SATURN_PHASE_YEARS",
    "SADE_SATI_TOTAL_YEARS",
    "sign_index",
    "sign_from_index",
    "house_from_moon",
    "sade_sati_signs",
    "sade_sati_phase_name",
    "is_sade_sati_active",
    "sade_sati_evidence",
    "moon_and_saturn_signs_from_context",
    "detect_sade_sati_from_context",
    "SadeSatiPeriod",
    "generate_sade_sati_periods",
    "current_sade_sati_period",
]
