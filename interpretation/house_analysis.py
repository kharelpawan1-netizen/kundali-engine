"""
interpretation/house_analysis.py

Parashari Vedic house interpretation layer.

This module consumes the normalized InterpretationContext and
does NOT calculate planetary positions, houses, Vargas, or Dashas.

Primary principles:
    - Whole-sign houses
    - House lordship
    - House occupants
    - Natural benefic/malefic nature
    - Functional lordship
    - House significations
    - Lord placement
    - Occupant placement
    - Evidence-first interpretation

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .context import (
    InterpretationContext,
    PlanetContext,
)

from .planet_analysis import (
    HOUSE_THEMES,
    house_lord,
    sign_for_house,
    natural_planet_type,
    functional_planet_type,
)


# ============================================================
# HOUSE SIGNIFICATIONS
# ============================================================

HOUSE_SIGNIFICATIONS = {
    1: [
        "body",
        "appearance",
        "personality",
        "identity",
        "vitality",
        "self-direction",
        "life orientation",
    ],

    2: [
        "wealth",
        "savings",
        "family",
        "speech",
        "food",
        "values",
        "accumulated resources",
    ],

    3: [
        "courage",
        "initiative",
        "communication",
        "skills",
        "writing",
        "siblings",
        "short journeys",
        "self-effort",
    ],

    4: [
        "mother",
        "home",
        "property",
        "vehicles",
        "education",
        "emotional security",
        "inner peace",
        "land",
    ],

    5: [
        "intelligence",
        "education",
        "creativity",
        "children",
        "romance",
        "mantra",
        "speculation",
        "purva punya",
    ],

    6: [
        "service",
        "employment",
        "competition",
        "debts",
        "disease",
        "enemies",
        "obstacles",
        "daily work",
    ],

    7: [
        "marriage",
        "spouse",
        "partnerships",
        "contracts",
        "business relationships",
        "public dealings",
        "foreign interaction",
    ],

    8: [
        "longevity",
        "transformation",
        "research",
        "secrets",
        "inheritance",
        "sudden events",
        "occult subjects",
        "joint resources",
    ],

    9: [
        "dharma",
        "fortune",
        "higher education",
        "guru",
        "father",
        "long journeys",
        "religion",
        "ethics",
        "blessings",
    ],

    10: [
        "career",
        "profession",
        "authority",
        "status",
        "reputation",
        "leadership",
        "government",
        "public contribution",
    ],

    11: [
        "income",
        "gains",
        "networks",
        "friends",
        "elder siblings",
        "ambitions",
        "fulfillment",
        "large organizations",
    ],

    12: [
        "expenses",
        "foreign lands",
        "sleep",
        "isolation",
        "retreat",
        "hospitals",
        "spiritual liberation",
        "loss",
        "private life",
    ],
}


# ============================================================
# HOUSE CATEGORIES
# ============================================================

KENDRA_HOUSES = {1, 4, 7, 10}

TRIKONA_HOUSES = {1, 5, 9}

DUSTHANA_HOUSES = {6, 8, 12}

UPACHAYA_HOUSES = {3, 6, 10, 11}

MARAKA_HOUSES = {2, 7}

ARTHA_HOUSES = {2, 6, 10}

KAMA_HOUSES = {3, 7, 11}

MOKSHA_HOUSES = {4, 8, 12}


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class HouseInterpretation:
    """Structured interpretation of one house."""

    house: int
    sign: str
    lord: str

    significations: List[str]

    occupants: List[str]

    lord_planet: Optional[str]
    lord_sign: Optional[str]
    lord_house: Optional[int]

    categories: List[str]

    natural_occupant_types: Dict[str, str]
    functional_occupant_types: Dict[str, str]

    themes: List[str]
    evidence: List[str]


# ============================================================
# HOUSE CATEGORY
# ============================================================

def house_categories(
    house: int,
) -> List[str]:
    """
    Return classical structural categories applicable
    to a house.
    """

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    categories = []

    if house in KENDRA_HOUSES:
        categories.append("kendra")

    if house in TRIKONA_HOUSES:
        categories.append("trikona")

    if house in DUSTHANA_HOUSES:
        categories.append("dusthana")

    if house in UPACHAYA_HOUSES:
        categories.append("upachaya")

    if house in MARAKA_HOUSES:
        categories.append("maraka")

    if house in ARTHA_HOUSES:
        categories.append("artha")

    if house in KAMA_HOUSES:
        categories.append("kama")

    if house in MOKSHA_HOUSES:
        categories.append("moksha")

    return categories


# ============================================================
# HOUSE LORD LOCATION
# ============================================================

def find_house_lord_planet(
    context: InterpretationContext,
    house: int,
) -> Optional[PlanetContext]:
    """
    Find the planet that owns the sign of a house.

    Rahu/Ketu are not assigned classical Parashari
    sign ownership here.
    """

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    lord = house_lord(
        context.ascendant_sign,
        house,
    )

    for planet in context.planets.values():

        if planet.name.lower() == lord.lower():
            return planet

    return None


# ============================================================
# HOUSE OCCUPANTS
# ============================================================

def occupants_of_house(
    context: InterpretationContext,
    house: int,
) -> List[PlanetContext]:
    """Return planets occupying a house."""

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    return [
        planet
        for planet in context.planets.values()
        if planet.house == house
    ]


# ============================================================
# HOUSE INTERPRETATION
# ============================================================

def interpret_house(
    context: InterpretationContext,
    house: int,
) -> HouseInterpretation:
    """
    Build an evidence-oriented Parashari interpretation
    of one house.

    This function does not make deterministic predictions.

    It identifies:
        - house sign
        - house lord
        - house categories
        - occupants
        - lord placement
        - natural nature
        - functional nature
        - interpretive themes
        - evidence
    """

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    sign = sign_for_house(
        context.ascendant_sign,
        house,
    )

    lord = house_lord(
        context.ascendant_sign,
        house,
    )

    significations = list(
        HOUSE_SIGNIFICATIONS[house]
    )

    occupants = occupants_of_house(
        context,
        house,
    )

    lord_planet = find_house_lord_planet(
        context,
        house,
    )

    categories = house_categories(
        house
    )

    natural_types = {}
    functional_types = {}

    for planet in occupants:

        natural_types[
            planet.name
        ] = natural_planet_type(
            planet.name
        )

        functional_types[
            planet.name
        ] = functional_planet_type(
            context.ascendant_sign,
            planet.name,
        )

    themes = []

    themes.append(
        HOUSE_THEMES[house]
    )

    if "kendra" in categories:
        themes.append(
            "major pillar of practical life"
        )

    if "trikona" in categories:
        themes.append(
            "dharma and supportive life potential"
        )

    if "dusthana" in categories:
        themes.append(
            "challenge, transformation and problem-solving"
        )

    if "upachaya" in categories:
        themes.append(
            "growth through effort, time and experience"
        )

    if "artha" in categories:
        themes.append(
            "material development and practical achievement"
        )

    if "kama" in categories:
        themes.append(
            "desire, interaction and fulfillment"
        )

    if "moksha" in categories:
        themes.append(
            "emotional depth, release and inner development"
        )

    evidence = []

    evidence.append(
        f"House {house} falls in {sign}."
    )

    evidence.append(
        f"House {house} is ruled by {lord}."
    )

    if categories:
        evidence.append(
            "House classification: "
            + ", ".join(categories)
            + "."
        )

    if occupants:

        names = ", ".join(
            planet.name
            for planet in occupants
        )

        evidence.append(
            f"Occupying planets: {names}."
        )

        for planet in occupants:

            evidence.append(
                f"{planet.name} occupies house {house} "
                f"from {planet.sign}."
            )

            evidence.append(
                f"{planet.name} is naturally "
                f"{natural_types[planet.name]}."
            )

            evidence.append(
                f"{planet.name} has "
                f"{functional_types[planet.name]} "
                f"functional classification."
            )

    else:

        evidence.append(
            "No classical planet occupies this house."
        )

    if lord_planet is not None:

        evidence.append(
            f"The house lord {lord_planet.name} "
            f"is placed in house {lord_planet.house} "
            f"in {lord_planet.sign}."
        )

    else:

        evidence.append(
            f"The house lord {lord} "
            f"is not available in the normalized planet set."
        )

    return HouseInterpretation(
        house=house,
        sign=sign,
        lord=lord,
        significations=significations,
        occupants=[
            planet.name
            for planet in occupants
        ],
        lord_planet=(
            lord_planet.name
            if lord_planet is not None
            else None
        ),
        lord_sign=(
            lord_planet.sign
            if lord_planet is not None
            else None
        ),
        lord_house=(
            lord_planet.house
            if lord_planet is not None
            else None
        ),
        categories=categories,
        natural_occupant_types=natural_types,
        functional_occupant_types=functional_types,
        themes=themes,
        evidence=evidence,
    )


# ============================================================
# COMPLETE HOUSE ANALYSIS
# ============================================================

def analyze_houses(
    context: InterpretationContext,
) -> Dict[int, HouseInterpretation]:
    """
    Analyze all twelve houses.
    """

    results = {}

    for house in range(1, 13):

        results[house] = interpret_house(
            context,
            house,
        )

    return results


# ============================================================
# EMPTY / OCCUPIED HOUSE HELPERS
# ============================================================

def occupied_houses(
    context: InterpretationContext,
) -> List[int]:
    """Return houses containing one or more planets."""

    return sorted(
        {
            planet.house
            for planet in context.planets.values()
            if 1 <= planet.house <= 12
        }
    )


def empty_houses(
    context: InterpretationContext,
) -> List[int]:
    """Return houses without classical planetary occupants."""

    occupied = set(
        occupied_houses(context)
    )

    return [
        house
        for house in range(1, 13)
        if house not in occupied
    ]


# ============================================================
# HOUSE LORD PLACEMENT SUMMARY
# ============================================================

def house_lord_placements(
    context: InterpretationContext,
) -> Dict[int, Optional[int]]:
    """
    Return:

        house -> house where its lord is placed
    """

    placements = {}

    for house in range(1, 13):

        lord_planet = find_house_lord_planet(
            context,
            house,
        )

        placements[house] = (
            lord_planet.house
            if lord_planet is not None
            else None
        )

    return placements


# ============================================================
# REPORT
# ============================================================

def house_analysis_report(
    context: InterpretationContext,
) -> List[str]:
    """
    Produce a concise textual house analysis.

    This is evidence-oriented and intentionally avoids
    deterministic future prediction.
    """

    analyses = analyze_houses(
        context
    )

    report = []

    for house in range(1, 13):

        analysis = analyses[house]

        occupant_text = (
            ", ".join(
                analysis.occupants
            )
            if analysis.occupants
            else "none"
        )

        lord_location = (
            f"House {analysis.lord_house}"
            if analysis.lord_house is not None
            else "not available"
        )

        report.append(
            f"House {house}: "
            f"{analysis.sign}; "
            f"lord={analysis.lord}; "
            f"lord placed={lord_location}; "
            f"occupants={occupant_text}."
        )

    return report


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "HOUSE_SIGNIFICATIONS",
    "KENDRA_HOUSES",
    "TRIKONA_HOUSES",
    "DUSTHANA_HOUSES",
    "UPACHAYA_HOUSES",
    "MARAKA_HOUSES",
    "ARTHA_HOUSES",
    "KAMA_HOUSES",
    "MOKSHA_HOUSES",
    "HouseInterpretation",
    "house_categories",
    "find_house_lord_planet",
    "occupants_of_house",
    "interpret_house",
    "analyze_houses",
    "occupied_houses",
    "empty_houses",
    "house_lord_placements",
    "house_analysis_report",
]