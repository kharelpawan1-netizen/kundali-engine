"""
interpretation/aspect_analysis.py

Parashari planetary aspect interpretation layer.

This module consumes chart data and determines planetary
aspects according to the selected Parashari aspect rules.

It does NOT calculate planetary positions, houses, Vargas,
Dashas, or planetary dignity.

Aspect rules used in this module:

    Sun      -> 7th aspect
    Moon     -> 7th aspect
    Mars     -> 4th, 7th, 8th aspects
    Mercury  -> 7th aspect
    Jupiter  -> 5th, 7th, 9th aspects
    Venus    -> 7th aspect
    Saturn   -> 3rd, 7th, 10th aspects
    Rahu     -> 7th aspect
    Ketu     -> 7th aspect

Important:
    The Rahu/Ketu rule is explicitly defined here so that
    the interpretation engine is deterministic. It can later
    be made configurable if a different traditional school
    is required.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


# ============================================================
# ASPECT RULES
# ============================================================

ASPECT_RULES = {
    "Sun": [7],
    "Moon": [7],
    "Mars": [4, 7, 8],
    "Mercury": [7],
    "Jupiter": [5, 7, 9],
    "Venus": [7],
    "Saturn": [3, 7, 10],
    "Rahu": [7],
    "Ketu": [7],
}


PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class AspectInterpretation:
    """
    Structured representation of one planetary aspect.
    """

    planet: str

    source_house: int

    target_house: int

    aspect_number: int

    evidence: List[str]


# ============================================================
# PLANET NORMALIZATION
# ============================================================

def _normalize_planet(
    planet: Any,
) -> str:
    """
    Convert a planet representation into its canonical name.
    """

    if planet is None:
        raise ValueError(
            "Planet cannot be None."
        )

    text = str(planet).strip()

    for candidate in PLANETS:

        if text.lower() == candidate.lower():
            return candidate

    for candidate in PLANETS:

        if candidate.lower() in text.lower():
            return candidate

    raise ValueError(
        f"Unknown planet representation: {planet!r}"
    )


# ============================================================
# VALIDATION
# ============================================================

def _validate_house(
    house: int,
) -> None:
    """
    Validate a house number.
    """

    if not 1 <= house <= 12:
        raise ValueError(
            "House must be between 1 and 12."
        )


# ============================================================
# ASPECT HOUSE CALCULATION
# ============================================================

def aspect_houses_from_house(
    source_house: int,
    aspect_numbers: List[int],
) -> List[int]:
    """
    Convert relative aspect numbers into absolute target houses.

    Example:

        source house = 1
        aspects = [4, 7, 8]

        returns:

        [4, 7, 8]

    Example:

        source house = 10
        aspects = [5, 7, 9]

        returns:

        [2, 4, 6]

    Parameters
    ----------
    source_house:
        House occupied by the aspecting planet.

    aspect_numbers:
        Relative Parashari aspect positions.
    """

    _validate_house(
        source_house
    )

    targets = []

    for aspect_number in aspect_numbers:

        if not 1 <= aspect_number <= 12:
            raise ValueError(
                "Aspect number must be between 1 and 12."
            )

        # Houses are represented as 1–12.
        #
        # The source house is counted as position 1,
        # therefore the relative aspect position must
        # be offset by aspect_number - 1.
        #
        # The modulo calculation itself is zero-based,
        # so the complete conversion becomes:
        #
        # ((source_house - 1)
        #  + (aspect_number - 1)) % 12 + 1
        #
        # which simplifies to:
        #
        # (source_house + aspect_number - 2) % 12 + 1

        target_house = (
            source_house
            + aspect_number
            - 2
        ) % 12 + 1

        targets.append(
            target_house
        )

    return targets


# ============================================================
# PLANET ASPECTS
# ============================================================

def planet_aspects(
    planet: str,
    source_house: int,
) -> List[int]:
    """
    Return target houses aspected by a planet.

    The aspect rules are relative to the planet's
    current house.

    Example:

        Mars in house 1

        -> houses 4, 7, 8
    """

    planet = _normalize_planet(
        planet
    )

    _validate_house(
        source_house
    )

    aspect_numbers = ASPECT_RULES[
        planet
    ]

    return aspect_houses_from_house(
        source_house,
        aspect_numbers,
    )


# ============================================================
# ASPECT INTERPRETATION
# ============================================================

def interpret_aspect(
    planet: str,
    source_house: int,
    target_house: int,
) -> AspectInterpretation:
    """
    Build structured evidence for one planetary aspect.

    The target house must be one of the houses naturally
    aspected by the planet from the source house.
    """

    planet = _normalize_planet(
        planet
    )

    _validate_house(
        source_house
    )

    _validate_house(
        target_house
    )

    targets = planet_aspects(
        planet,
        source_house,
    )

    if target_house not in targets:

        raise ValueError(
            f"{planet} from house {source_house} "
            f"does not aspect house {target_house}."
        )

    aspect_numbers = ASPECT_RULES[
        planet
    ]

    index = targets.index(
        target_house
    )

    aspect_number = aspect_numbers[
        index
    ]

    evidence = [
        f"{planet} is placed in house {source_house}.",
        (
            f"{planet} casts its {aspect_number}th "
            f"aspect toward house {target_house}."
        ),
    ]

    return AspectInterpretation(
        planet=planet,
        source_house=source_house,
        target_house=target_house,
        aspect_number=aspect_number,
        evidence=evidence,
    )


# ============================================================
# CHART PLANET EXTRACTION
# ============================================================

def _chart_planets(
    chart: Any,
) -> Dict[str, Any]:
    """
    Safely retrieve planets from a chart.
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


# ============================================================
# ASPECTING PLANETS
# ============================================================

def aspecting_planets(
    chart: Any,
    target_house: int,
) -> List[str]:
    """
    Return planets that aspect a target house.
    """

    _validate_house(
        target_house
    )

    planets = _chart_planets(
        chart
    )

    result = []

    for planet in planets.values():

        name = _normalize_planet(
            getattr(
                planet,
                "name",
                planet,
            )
        )

        source_house = getattr(
            planet,
            "house",
            None,
        )

        if source_house is None:
            continue

        source_house = int(
            source_house
        )

        if not 1 <= source_house <= 12:
            continue

        targets = planet_aspects(
            name,
            source_house,
        )

        if target_house in targets:

            result.append(
                name
            )

    return result


# ============================================================
# COMPLETE ASPECT ANALYSIS
# ============================================================

def analyze_aspects(
    chart: Any,
) -> Dict[
    str,
    Dict[int, AspectInterpretation],
]:
    """
    Analyze all planetary aspects in a chart.

    Returns:

        {
            "Mars": {
                4: AspectInterpretation(...),
                7: AspectInterpretation(...),
                8: AspectInterpretation(...),
            },
            ...
        }

    The outer dictionary is indexed by planet.

    The inner dictionary is indexed by target house.
    """

    planets = _chart_planets(
        chart
    )

    results = {}

    for planet in planets.values():

        name = _normalize_planet(
            getattr(
                planet,
                "name",
                planet,
            )
        )

        source_house = getattr(
            planet,
            "house",
            None,
        )

        if source_house is None:
            continue

        source_house = int(
            source_house
        )

        if not 1 <= source_house <= 12:
            continue

        targets = planet_aspects(
            name,
            source_house,
        )

        planet_results = {}

        for target_house in targets:

            planet_results[
                target_house
            ] = interpret_aspect(
                name,
                source_house,
                target_house,
            )

        results[
            name
        ] = planet_results

    return results


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "ASPECT_RULES",
    "AspectInterpretation",
    "aspect_houses_from_house",
    "planet_aspects",
    "interpret_aspect",
    "aspecting_planets",
    "analyze_aspects",
]