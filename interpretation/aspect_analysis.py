"""
interpretation/aspect_analysis.py

Parashari planetary aspect interpretation layer.

This module consumes normalized chart data and determines
planetary aspects according to the configured Parashari rules.

It does NOT calculate:
    - planetary positions
    - houses
    - Vargas
    - Dashas
    - planetary dignity
    - yogas
    - predictive outcomes

Default aspect rules:

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
    Rahu/Ketu aspect treatment differs between traditional
    schools. Therefore their rules are explicitly represented
    in ASPECT_RULES rather than being hidden inside the logic.

The interpretation layer does not decide which tradition is
"correct". It applies the configured rule set consistently.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


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

    if not text:
        raise ValueError(
            "Planet cannot be empty."
        )

    for candidate in PLANETS:

        if text.lower() == candidate.lower():
            return candidate

    # Handle enum-like representations such as:
    # Planet.Mars
    # SomePlanet.Mars
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
    Validate a whole-sign house number.
    """

    if not isinstance(house, int):
        raise TypeError(
            "House must be an integer."
        )

    if not 1 <= house <= 12:
        raise ValueError(
            "House must be between 1 and 12."
        )


def _validate_aspect_number(
    aspect_number: int,
) -> None:
    """
    Validate a relative aspect number.

    In the Parashari whole-sign system, aspect positions
    are counted from the source house as position 1.
    """

    if not isinstance(
        aspect_number,
        int,
    ):
        raise TypeError(
            "Aspect number must be an integer."
        )

    if not 1 <= aspect_number <= 12:
        raise ValueError(
            "Aspect number must be between 1 and 12."
        )


def _validate_aspect_rules() -> None:
    """
    Validate the configured aspect rule table.

    This protects the interpretation engine from malformed
    rule definitions.
    """

    for planet in PLANETS:

        if planet not in ASPECT_RULES:
            raise ValueError(
                f"Missing aspect rule for planet: {planet}"
            )

        aspect_numbers = ASPECT_RULES[
            planet
        ]

        if not isinstance(
            aspect_numbers,
            list,
        ):
            raise TypeError(
                f"Aspect rules for {planet} "
                f"must be a list."
            )

        if not aspect_numbers:
            raise ValueError(
                f"Aspect rules for {planet} "
                f"cannot be empty."
            )

        seen = set()

        for aspect_number in aspect_numbers:

            _validate_aspect_number(
                aspect_number
            )

            if aspect_number in seen:
                raise ValueError(
                    f"Duplicate aspect number "
                    f"{aspect_number} for {planet}."
                )

            seen.add(
                aspect_number
            )


# Validate the static configuration when the module loads.
_validate_aspect_rules()


# ============================================================
# ASPECT HOUSE CALCULATION
# ============================================================

def aspect_houses_from_house(
    source_house: int,
    aspect_numbers: List[int],
) -> List[int]:
    """
    Convert relative aspect positions into absolute
    target houses.

    The source house itself is counted as position 1.

    Formula:

        target =
            ((source_house - 1)
             + (aspect_number - 1))
            % 12 + 1

    Examples
    --------
    Mars in house 1:

        4th -> house 4
        7th -> house 7
        8th -> house 8

    Jupiter in house 10:

        5th -> house 2
        7th -> house 4
        9th -> house 6
    """

    _validate_house(
        source_house
    )

    if aspect_numbers is None:
        raise ValueError(
            "aspect_numbers cannot be None."
        )

    if not isinstance(
        aspect_numbers,
        list,
    ):
        raise TypeError(
            "aspect_numbers must be a list."
        )

    targets = []

    for aspect_number in aspect_numbers:

        _validate_aspect_number(
            aspect_number
        )

        target_house = (
            (
                source_house
                - 1
                + aspect_number
                - 1
            )
            % 12
        ) + 1

        targets.append(
            target_house
        )

    return targets


# ============================================================
# PLANET ASPECT RULES
# ============================================================

def planet_aspect_numbers(
    planet: str,
) -> List[int]:
    """
    Return the relative aspect numbers applicable
    to a planet.

    Examples:

        planet_aspect_numbers("Mars")
        -> [4, 7, 8]

        planet_aspect_numbers("Jupiter")
        -> [5, 7, 9]
    """

    planet = _normalize_planet(
        planet
    )

    return list(
        ASPECT_RULES[planet]
    )


# ============================================================
# PLANET ASPECTS
# ============================================================

def planet_aspects(
    planet: str,
    source_house: int,
) -> List[int]:
    """
    Return absolute target houses aspected by a planet.

    Example:

        Mars in house 1
        -> [4, 7, 8]
    """

    planet = _normalize_planet(
        planet
    )

    _validate_house(
        source_house
    )

    return aspect_houses_from_house(
        source_house,
        planet_aspect_numbers(
            planet
        ),
    )


# ============================================================
# ASPECT NUMBER BETWEEN HOUSES
# ============================================================

def aspect_number_between_houses(
    source_house: int,
    target_house: int,
) -> int:
    """
    Return the relative aspect number from source house
    to target house.

    Examples:

        1 -> 7 = 7th aspect
        1 -> 4 = 4th aspect
        10 -> 2 = 5th aspect
        12 -> 6 = 7th aspect

    The source house is counted as position 1.
    """

    _validate_house(
        source_house
    )

    _validate_house(
        target_house
    )

    return (
        (
            target_house
            - source_house
        )
        % 12
    ) + 1


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

    aspect_number = (
        aspect_number_between_houses(
            source_house,
            target_house,
        )
    )

    allowed_aspects = planet_aspect_numbers(
        planet
    )

    if aspect_number not in allowed_aspects:

        raise ValueError(
            f"{planet} from house {source_house} "
            f"does not aspect house {target_house}."
        )

    evidence = [
        (
            f"{planet} is placed in house "
            f"{source_house}."
        ),
        (
            f"{planet} casts its "
            f"{aspect_number}{_ordinal_suffix(aspect_number)} "
            f"aspect toward house "
            f"{target_house}."
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
# ORDINAL FORMATTING
# ============================================================

def _ordinal_suffix(
    number: int,
) -> str:
    """
    Return the English ordinal suffix for a positive integer.

    Examples:
        1 -> st
        2 -> nd
        3 -> rd
        4 -> th
        11 -> th
        12 -> th
        13 -> th
    """

    if 10 <= number % 100 <= 20:
        return "th"

    remainder = number % 10

    if remainder == 1:
        return "st"

    if remainder == 2:
        return "nd"

    if remainder == 3:
        return "rd"

    return "th"


# ============================================================
# CHART PLANET EXTRACTION
# ============================================================

def _chart_planets(
    chart: Any,
) -> Dict[str, Any]:
    """
    Safely retrieve planets from a chart.

    The chart is expected to expose a mapping-like
    ``planets`` attribute with a values() method.
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

    if not hasattr(
        planets,
        "values",
    ):
        raise TypeError(
            "Chart planets must expose a values() method."
        )

    return planets


# ============================================================
# PLANET SOURCE HOUSE
# ============================================================

def _planet_house(
    planet: Any,
) -> Optional[int]:
    """
    Extract and validate a planet's house.

    Invalid or unavailable houses return None.

    Python 3.9 compatible.
    """

    house = getattr(
        planet,
        "house",
        None,
    )

    if house is None:
        return None

    try:
        house = int(
            house
        )
    except (
        TypeError,
        ValueError,
    ) as exc:

        raise ValueError(
            f"Invalid planetary house: {house!r}"
        ) from exc

    if not 1 <= house <= 12:
        return None

    return house


# ============================================================
# ASPECTING PLANETS
# ============================================================

def aspecting_planets(
    chart: Any,
    target_house: int,
) -> List[str]:
    """
    Return planets that aspect a target house.

    The returned order follows the chart's planetary
    iteration order.
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

        source_house = _planet_house(
            planet
        )

        if source_house is None:
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
# PLANETS ASPECTING PLANET
# ============================================================

def aspecting_planets_of_planet(
    chart: Any,
    target_planet: str,
) -> List[str]:
    """
    Return planets that aspect the house occupied by
    the target planet.

    The target planet itself is not returned because
    no configured planet has a 1st aspect.
    """

    target_planet = _normalize_planet(
        target_planet
    )

    planets = _chart_planets(
        chart
    )

    target_object = None

    for planet in planets.values():

        name = _normalize_planet(
            getattr(
                planet,
                "name",
                planet,
            )
        )

        if name == target_planet:
            target_object = planet
            break

    if target_object is None:
        return []

    target_house = _planet_house(
        target_object
    )

    if target_house is None:
        return []

    return [
        planet
        for planet in aspecting_planets(
            chart,
            target_house,
        )
        if planet != target_planet
    ]


# ============================================================
# PLANETS ASPECTED BY PLANET
# ============================================================

def planets_aspected_by_planet(
    chart: Any,
    source_planet: str,
) -> List[str]:
    """
    Return planets occupying houses aspected by
    the source planet.

    The source planet itself is never returned.
    """

    source_planet = _normalize_planet(
        source_planet
    )

    planets = _chart_planets(
        chart
    )

    source_object = None

    for planet in planets.values():

        name = _normalize_planet(
            getattr(
                planet,
                "name",
                planet,
            )
        )

        if name == source_planet:
            source_object = planet
            break

    if source_object is None:
        return []

    source_house = _planet_house(
        source_object
    )

    if source_house is None:
        return []

    target_houses = set(
        planet_aspects(
            source_planet,
            source_house,
        )
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

        if name == source_planet:
            continue

        house = _planet_house(
            planet
        )

        if house is None:
            continue

        if house in target_houses:
            result.append(
                name
            )

    return result


# ============================================================
# MUTUAL ASPECT
# ============================================================

def planets_mutually_aspect(
    chart: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Determine whether two planets mutually aspect
    each other under the configured aspect rules.

    Returns False if:
        - either planet is unavailable
        - either planet lacks a valid house
        - both names refer to the same planet
        - the aspect is only one-way
    """

    planet_a = _normalize_planet(
        planet_a
    )

    planet_b = _normalize_planet(
        planet_b
    )

    if planet_a == planet_b:
        return False

    planets = _chart_planets(
        chart
    )

    objects = {}

    for planet in planets.values():

        name = _normalize_planet(
            getattr(
                planet,
                "name",
                planet,
            )
        )

        if name in {
            planet_a,
            planet_b,
        }:

            objects[name] = planet

    if (
        planet_a not in objects
        or planet_b not in objects
    ):
        return False

    house_a = _planet_house(
        objects[planet_a]
    )

    house_b = _planet_house(
        objects[planet_b]
    )

    if (
        house_a is None
        or house_b is None
    ):
        return False

    a_targets = set(
        planet_aspects(
            planet_a,
            house_a,
        )
    )

    b_targets = set(
        planet_aspects(
            planet_b,
            house_b,
        )
    )

    return (
        house_b in a_targets
        and house_a in b_targets
    )


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

    The outer dictionary is indexed by source planet.

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

        source_house = _planet_house(
            planet
        )

        if source_house is None:
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
    "PLANETS",
    "AspectInterpretation",
    "aspect_houses_from_house",
    "planet_aspect_numbers",
    "planet_aspects",
    "aspect_number_between_houses",
    "interpret_aspect",
    "aspecting_planets",
    "aspecting_planets_of_planet",
    "planets_aspected_by_planet",
    "planets_mutually_aspect",
    "analyze_aspects",
]