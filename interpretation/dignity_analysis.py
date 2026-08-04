
"""
interpretation/dignity_analysis.py

Interpretation layer for planetary dignity.

This module consumes the classical dignity calculations
from astronomy.dignity and produces structured dignity
interpretations for the Kundali Engine.

It does NOT calculate planetary positions.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from astronomy.dignity import (
    is_debilitated,
    is_exalted,
    is_own_sign,
)
from models.graha import Graha
from models.zodiac import ZodiacSign


# ============================================================
# MOOLATRIKONA DEGREE RANGES
# ============================================================
#
# These ranges represent the commonly used classical
# Parashari dignity ranges.
#
# The upper boundary is exclusive.
#
# Example:
#
#     Sun in Leo 15°  -> Moolatrikona
#     Sun in Leo 25°  -> Own Sign
#
# The exact degree traditions can vary between sources.
# Keeping the ranges centralized makes this easy to audit
# or configure later.
# ============================================================

MOOLATRIKONA_RANGES = {
    Graha.SUN: (
        ZodiacSign.LEO,
        0.0,
        20.0,
    ),

    Graha.MOON: (
        ZodiacSign.TAURUS,
        4.0,
        30.0,
    ),

    Graha.MARS: (
        ZodiacSign.ARIES,
        0.0,
        12.0,
    ),

    Graha.MERCURY: (
        ZodiacSign.VIRGO,
        16.0,
        20.0,
    ),

    Graha.JUPITER: (
        ZodiacSign.SAGITTARIUS,
        0.0,
        10.0,
    ),

    Graha.VENUS: (
        ZodiacSign.LIBRA,
        0.0,
        15.0,
    ),

    Graha.SATURN: (
        ZodiacSign.AQUARIUS,
        0.0,
        20.0,
    ),
}


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class DignityInterpretation:
    """
    Structured interpretation of planetary dignity.
    """

    planet: str
    sign: str
    dignity: str
    exact_degree: float

    is_exalted: bool
    is_debilitated: bool
    is_own_sign: bool
    is_moolatrikona: bool

    evidence: list[str]


# ============================================================
# PLANET NORMALIZATION
# ============================================================

def _normalize_planet(
    planet: Any,
) -> Graha:
    """
    Convert a planet representation into Graha enum.
    """

    if isinstance(planet, Graha):
        return planet

    if planet is None:
        raise ValueError(
            "Planet cannot be None."
        )

    text = str(planet).strip()

    for graha in Graha:

        if text.lower() == graha.value.lower():
            return graha

        if text.lower() == graha.name.lower():
            return graha

    raise ValueError(
        f"Unknown planet representation: {planet!r}"
    )


# ============================================================
# SIGN NORMALIZATION
# ============================================================

def _normalize_sign(
    sign: Any,
) -> ZodiacSign:
    """
    Convert a sign representation into ZodiacSign enum.
    """

    if isinstance(sign, ZodiacSign):
        return sign

    if sign is None:
        raise ValueError(
            "Zodiac sign cannot be None."
        )

    text = str(sign).strip()

    for zodiac_sign in ZodiacSign:

        if (
            text.lower()
            == zodiac_sign.display_name.lower()
        ):
            return zodiac_sign

        if (
            text.lower()
            == zodiac_sign.name.lower()
        ):
            return zodiac_sign

    raise ValueError(
        f"Unknown zodiac sign representation: {sign!r}"
    )


# ============================================================
# DEGREE VALIDATION
# ============================================================

def _validate_degree(
    degree: float,
) -> float:
    """
    Validate and normalize a degree within a zodiac sign.

    Valid range:

        0 <= degree < 30
    """

    degree = float(degree)

    if not 0.0 <= degree < 30.0:
        raise ValueError(
            "Sign degree must be between 0 and less than 30."
        )

    return degree


# ============================================================
# MOOLATRIKONA CALCULATION
# ============================================================

def _is_moolatrikona_at_degree(
    graha: Graha,
    sign: ZodiacSign,
    degree: float,
) -> bool:
    """
    Determine whether a planet is in its Moolatrikona
    degree range.
    """

    rule = MOOLATRIKONA_RANGES.get(
        graha
    )

    if rule is None:
        return False

    mt_sign, lower, upper = rule

    return (
        sign == mt_sign
        and lower <= degree < upper
    )


# ============================================================
# DIGNITY CLASSIFICATION
# ============================================================

def _determine_dignity(
    exalted: bool,
    debilitated: bool,
    moolatrikona: bool,
    own_sign: bool,
) -> str:
    """
    Determine the primary dignity classification.

    Priority:

        Exalted
        Debilitated
        Moolatrikona
        Own Sign
        Neutral

    Friend/enemy classification is intentionally handled
    separately because it requires a planetary friendship
    system.
    """

    if exalted:
        return "Exalted"

    if debilitated:
        return "Debilitated"

    if moolatrikona:
        return "Moolatrikona"

    if own_sign:
        return "Own Sign"

    return "Neutral"


# ============================================================
# SINGLE PLANET ANALYSIS
# ============================================================

def interpret_dignity(
    planet: Any,
    sign: Any,
    exact_degree: float = 0.0,
) -> DignityInterpretation:
    """
    Interpret the dignity of a single planet.

    Parameters
    ----------
    planet:
        Planet name or Graha enum.

    sign:
        Zodiac sign name or ZodiacSign enum.

    exact_degree:
        Planetary degree within the sign.
    """

    graha = _normalize_planet(
        planet
    )

    zodiac_sign = _normalize_sign(
        sign
    )

    degree = _validate_degree(
        exact_degree
    )

    exalted = is_exalted(
        graha,
        zodiac_sign,
    )

    debilitated = is_debilitated(
        graha,
        zodiac_sign,
    )

    own_sign = is_own_sign(
        graha,
        zodiac_sign,
    )

    moolatrikona = _is_moolatrikona_at_degree(
        graha,
        zodiac_sign,
        degree,
    )

    dignity = _determine_dignity(
        exalted=exalted,
        debilitated=debilitated,
        moolatrikona=moolatrikona,
        own_sign=own_sign,
    )

    evidence = [
        (
            f"{graha.display_name} is placed in "
            f"{zodiac_sign.display_name} "
            f"at {degree:.2f}°."
        ),
        (
            f"Planetary dignity is classified as "
            f"{dignity}."
        ),
    ]

    if exalted:

        evidence.append(
            f"{graha.display_name} is exalted in "
            f"{zodiac_sign.display_name}."
        )

    elif debilitated:

        evidence.append(
            f"{graha.display_name} is debilitated in "
            f"{zodiac_sign.display_name}."
        )

    elif moolatrikona:

        evidence.append(
            f"{graha.display_name} occupies its "
            f"Moolatrikona degree range."
        )

    elif own_sign:

        evidence.append(
            f"{graha.display_name} occupies its own sign "
            f"outside its Moolatrikona degree range."
        )

    else:

        evidence.append(
            f"{graha.display_name} is not in an "
            f"exaltation, debilitation, Moolatrikona, "
            f"or own-sign position."
        )

    return DignityInterpretation(
        planet=graha.display_name,
        sign=zodiac_sign.display_name,
        dignity=dignity,
        exact_degree=degree,
        is_exalted=exalted,
        is_debilitated=debilitated,
        is_own_sign=own_sign,
        is_moolatrikona=moolatrikona,
        evidence=evidence,
    )


# ============================================================
# PLANET OBJECT ANALYSIS
# ============================================================

def interpret_planet_dignity(
    planet: Any,
) -> DignityInterpretation:
    """
    Interpret dignity directly from a Planet-like object.

    The object must expose:

        name
        sign
        sign_degree
    """

    name = getattr(
        planet,
        "name",
        None,
    )

    sign = getattr(
        planet,
        "sign",
        None,
    )

    degree = getattr(
        planet,
        "sign_degree",
        0.0,
    )

    if name is None:
        raise ValueError(
            "Planet object does not expose a name."
        )

    if sign is None:
        raise ValueError(
            "Planet object does not expose a sign."
        )

    return interpret_dignity(
        planet=name,
        sign=sign,
        exact_degree=degree,
    )


# ============================================================
# CHART ANALYSIS
# ============================================================

def _chart_planets(
    chart: Any,
) -> Dict[str, Any]:
    """
    Retrieve planets from a chart.
    """

    planets = getattr(
        chart,
        "planets",
        None,
    )

    if planets is None:
        raise ValueError(
            "Chart does not expose planets."
        )

    return planets


def analyze_dignities(
    chart: Any,
) -> Dict[str, DignityInterpretation]:
    """
    Analyze dignity for every planet in a chart.
    """

    planets = _chart_planets(
        chart
    )

    results = {}

    for planet in planets.values():

        interpretation = interpret_planet_dignity(
            planet
        )

        results[
            interpretation.planet
        ] = interpretation

    return results


# ============================================================
# REPORT
# ============================================================

def dignity_analysis_report(
    chart: Any,
) -> str:
    """
    Generate a human-readable dignity report.
    """

    results = analyze_dignities(
        chart
    )

    lines = [
        "PLANETARY DIGNITY ANALYSIS",
        "=" * 30,
    ]

    for planet_name, result in results.items():

        lines.append(
            f"{planet_name}: "
            f"{result.dignity} "
            f"({result.sign} "
            f"{result.exact_degree:.2f}°)"
        )

    return "\n".join(
        lines
    )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "MOOLATRIKONA_RANGES",
    "DignityInterpretation",
    "interpret_dignity",
    "interpret_planet_dignity",
    "analyze_dignities",
    "dignity_analysis_report",
]
