"""
interpretation/planet_analysis.py

First Vedic interpretation layer.

This module interprets planetary placement using:
    - Ascendant
    - Sign
    - House
    - Natural planetary nature
    - Functional lordship
    - House ownership
    - Dignity where available
    - Nakshatra where available

Design principle:
    Calculation engine -> factual chart data
    Interpretation layer -> Vedic meaning

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


# ============================================================
# CONSTANTS
# ============================================================

SIGNS = [
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
]


# Classical Parashari sign ownership.
SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}


NATURAL_BENEFICS = {
    "Jupiter",
    "Venus",
    "Mercury",
    "Moon",
}


NATURAL_MALEFICS = {
    "Sun",
    "Mars",
    "Saturn",
    "Rahu",
    "Ketu",
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
class PlanetInterpretation:
    """Structured interpretation context for one planet."""

    planet: str
    sign: str
    house: int
    sign_degree: float

    house_lordships: List[int]
    is_lagna_lord: bool

    natural_type: str
    functional_type: str

    nakshatra: Optional[str]
    pada: Optional[int]

    dignity: Optional[str]

    keywords: List[str]
    themes: List[str]

    evidence: List[str]


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize_sign(sign: Any) -> str:
    """
    Convert sign enum/string representations into a canonical
    sign name.
    """

    if sign is None:
        raise ValueError("Planet sign cannot be None.")

    text = str(sign).strip()

    for sign_name in SIGNS:
        if text.lower() == sign_name.lower():
            return sign_name

        if text.lower() == sign_name.lower().replace(" ", "_"):
            return sign_name

    # Handle enum-style representations.
    for sign_name in SIGNS:
        if sign_name.lower() in text.lower():
            return sign_name

    raise ValueError(
        f"Unknown zodiac sign representation: {sign!r}"
    )


def _planet_name(planet: Any) -> str:
    """Extract a canonical planet name."""

    name = getattr(planet, "name", planet)

    text = str(name).strip()

    for candidate in PLANETS:
        if text.lower() == candidate.lower():
            return candidate

    for candidate in PLANETS:
        if candidate.lower() in text.lower():
            return candidate

    raise ValueError(
        f"Unknown planet representation: {name!r}"
    )


# ============================================================
# SIGN / HOUSE UTILITIES
# ============================================================

def sign_index(sign: str) -> int:
    """Return zero-based zodiac index."""

    sign = _normalize_sign(sign)

    return SIGNS.index(sign)


def house_from_sign(
    ascendant_sign: str,
    planet_sign: str,
) -> int:
    """
    Determine whole-sign house.

    House 1 is the Ascendant sign.
    """

    asc_index = sign_index(
        ascendant_sign
    )

    planet_index = sign_index(
        planet_sign
    )

    return (
        planet_index
        - asc_index
    ) % 12 + 1


def sign_for_house(
    ascendant_sign: str,
    house: int,
) -> str:
    """Return the zodiac sign occupying a whole-sign house."""

    if not 1 <= house <= 12:
        raise ValueError(
            "House must be between 1 and 12."
        )

    asc_index = sign_index(
        ascendant_sign
    )

    return SIGNS[
        (
            asc_index
            + house
            - 1
        ) % 12
    ]


def house_lord(
    ascendant_sign: str,
    house: int,
) -> str:
    """Return the lord of a whole-sign house."""

    sign = sign_for_house(
        ascendant_sign,
        house,
    )

    return SIGN_LORDS[sign]


def planetary_lordships(
    ascendant_sign: str,
    planet: str,
) -> List[int]:
    """
    Return houses owned by a planet.

    Rahu/Ketu have no classical sign ownership in this
    basic Parashari layer.
    """

    planet = _planet_name(planet)

    if planet in {"Rahu", "Ketu"}:
        return []

    houses = []

    for house in range(1, 13):

        if house_lord(
            ascendant_sign,
            house,
        ) == planet:

            houses.append(house)

    return houses


# ============================================================
# NATURAL NATURE
# ============================================================

def natural_planet_type(
    planet: str,
) -> str:
    """Return natural benefic/malefic classification."""

    planet = _planet_name(planet)

    if planet in NATURAL_BENEFICS:
        return "benefic"

    if planet in NATURAL_MALEFICS:
        return "malefic"

    return "neutral"


# ============================================================
# FUNCTIONAL NATURE
# ============================================================

def functional_planet_type(
    ascendant_sign: str,
    planet: str,
) -> str:
    """
    Determine a basic Parashari functional classification.

    This is intentionally conservative.

    The module does not yet attempt complete yoga-based
    functional judgment. That belongs in yoga_analysis.py.
    """

    planet = _planet_name(planet)

    houses = planetary_lordships(
        ascendant_sign,
        planet,
    )

    # Nodes are handled separately later.
    if planet in {"Rahu", "Ketu"}:
        return "node"

    # Lagna lord receives a strong functional benefic bias.
    if 1 in houses:
        return "functional_benefic"

    # Lords of trikonas.
    if any(
        house in houses
        for house in (5, 9)
    ):
        return "functional_benefic"

    # Strong dusthana ownership.
    if any(
        house in houses
        for house in (6, 8, 12)
    ):
        return "functional_malefic"

    # 2nd and 11th are wealth-related but not pure trikonas.
    if any(
        house in houses
        for house in (2, 11)
    ):
        return "conditional"

    # 3rd is generally treated as functionally challenging.
    if 3 in houses:
        return "functional_malefic"

    # 4th and 7th require contextual judgment.
    if any(
        house in houses
        for house in (4, 7)
    ):
        return "conditional"

    return "neutral"


# ============================================================
# DIGNITY
# ============================================================

def _extract_dignity(
    planet: Any,
) -> Optional[str]:
    """
    Extract dignity if the calculation layer exposes it.

    The interpretation layer deliberately does not calculate
    dignity itself yet. Existing dignity calculations remain
    the source of truth.
    """

    dignity = getattr(
        planet,
        "dignity",
        None,
    )

    if dignity is None:
        return None

    return str(dignity)


# ============================================================
# KEYWORDS
# ============================================================

PLANET_KEYWORDS = {
    "Sun": [
        "authority",
        "identity",
        "leadership",
        "confidence",
        "father",
        "status",
    ],
    "Moon": [
        "mind",
        "emotions",
        "mother",
        "adaptability",
        "public response",
        "mental security",
    ],
    "Mars": [
        "initiative",
        "courage",
        "competition",
        "technical ability",
        "assertiveness",
        "energy",
    ],
    "Mercury": [
        "intellect",
        "communication",
        "analysis",
        "commerce",
        "learning",
        "calculation",
    ],
    "Jupiter": [
        "wisdom",
        "dharma",
        "knowledge",
        "teachers",
        "expansion",
        "guidance",
    ],
    "Venus": [
        "relationships",
        "beauty",
        "comfort",
        "arts",
        "harmony",
        "pleasure",
    ],
    "Saturn": [
        "discipline",
        "responsibility",
        "delay",
        "endurance",
        "service",
        "structure",
    ],
    "Rahu": [
        "ambition",
        "material desire",
        "unconventionality",
        "foreign influence",
        "obsession",
        "amplification",
    ],
    "Ketu": [
        "detachment",
        "spirituality",
        "separation",
        "intuition",
        "inwardness",
        "past-patterns",
    ],
}


HOUSE_THEMES = {
    1: "self, body, identity and life direction",
    2: "wealth, speech, family and accumulated resources",
    3: "effort, courage, communication and siblings",
    4: "home, mother, emotional foundation and property",
    5: "intelligence, education, creativity, children and purva punya",
    6: "service, competition, debts, disease and obstacles",
    7: "marriage, partnerships, contracts and public dealings",
    8: "transformation, longevity, hidden matters and research",
    9: "dharma, fortune, higher learning, teachers and long journeys",
    10: "career, authority, profession and public reputation",
    11: "income, gains, networks, ambitions and fulfillment",
    12: "expenses, foreign lands, isolation, sleep and liberation",
}


# ============================================================
# PLANET INTERPRETATION
# ============================================================

def interpret_planet(
    chart: Any,
    planet: Any,
) -> PlanetInterpretation:
    """
    Build structured Vedic interpretation context
    for one planet.

    No prediction is generated here.

    This function creates evidence that later synthesis
    modules can use.
    """

    ascendant = getattr(
        chart,
        "ascendant",
        None,
    )

    if ascendant is None:
        raise ValueError(
            "Chart does not expose ascendant."
        )

    # Existing chart helper is preferred where available.
    asc_sign_obj = getattr(
        chart,
        "ascendant_sign",
        None,
    )

    if asc_sign_obj is not None:
        ascendant_sign = _normalize_sign(
            asc_sign_obj
        )
    else:
        # The existing astronomy layer normally exposes
        # sign_enum(), but keep this module independent.
        try:
            from astronomy.signs import sign_enum

            ascendant_sign = _normalize_sign(
                sign_enum(ascendant)
            )

        except Exception as exc:
            raise ValueError(
                "Unable to determine Ascendant sign."
            ) from exc

    name = _planet_name(
        planet
    )

    sign = _normalize_sign(
        getattr(
            planet,
            "sign",
            None,
        )
    )

    house = getattr(
        planet,
        "house",
        None,
    )

    if house is None:
        house = house_from_sign(
            ascendant_sign,
            sign,
        )

    house = int(house)

    degree = float(
        getattr(
            planet,
            "sign_degree",
            0.0,
        )
    )

    nakshatra = getattr(
        planet,
        "nakshatra",
        None,
    )

    if nakshatra is not None:
        nakshatra = str(
            nakshatra
        )

    pada = getattr(
        planet,
        "pada",
        None,
    )

    if pada is not None:
        pada = int(pada)

    lordships = planetary_lordships(
        ascendant_sign,
        name,
    )

    is_lagna_lord = (
        1 in lordships
    )

    natural_type = natural_planet_type(
        name
    )

    functional_type = functional_planet_type(
        ascendant_sign,
        name,
    )

    keywords = list(
        PLANET_KEYWORDS.get(
            name,
            [],
        )
    )

    themes = [
        HOUSE_THEMES[house]
    ]

    evidence = []

    evidence.append(
        f"{name} occupies {sign} in house {house}."
    )

    if lordships:
        formatted = ", ".join(
            str(house_number)
            for house_number in lordships
        )

        evidence.append(
            f"{name} rules house(s) {formatted}."
        )

    if is_lagna_lord:
        evidence.append(
            f"{name} is the Lagna lord."
        )

    evidence.append(
        f"Natural nature: {natural_type}."
    )

    evidence.append(
        f"Functional classification: "
        f"{functional_type}."
    )

    if nakshatra:
        if pada is not None:
            evidence.append(
                f"Nakshatra: {nakshatra}, "
                f"Pada {pada}."
            )
        else:
            evidence.append(
                f"Nakshatra: {nakshatra}."
            )

    dignity = _extract_dignity(
        planet
    )

    if dignity:
        evidence.append(
            f"Recorded dignity: {dignity}."
        )

    return PlanetInterpretation(
        planet=name,
        sign=sign,
        house=house,
        sign_degree=degree,
        house_lordships=lordships,
        is_lagna_lord=is_lagna_lord,
        natural_type=natural_type,
        functional_type=functional_type,
        nakshatra=nakshatra,
        pada=pada,
        dignity=dignity,
        keywords=keywords,
        themes=themes,
        evidence=evidence,
    )


# ============================================================
# COMPLETE CHART PLANET ANALYSIS
# ============================================================

def analyze_planets(
    chart: Any,
) -> Dict[str, PlanetInterpretation]:
    """
    Analyze every planet in the chart.

    Returns:
        {
            "Sun": PlanetInterpretation(...),
            "Moon": PlanetInterpretation(...),
            ...
        }
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

    results = {}

    for planet in planets.values():

        interpretation = interpret_planet(
            chart,
            planet,
        )

        results[
            interpretation.planet
        ] = interpretation

    return results


# ============================================================
# SIMPLE REPORT
# ============================================================

def planet_analysis_report(
    chart: Any,
) -> List[str]:
    """
    Produce a concise evidence-oriented report.

    This is deliberately not the final prediction engine.
    """

    analyses = analyze_planets(
        chart
    )

    report = []

    for name in PLANETS:

        analysis = analyses.get(
            name
        )

        if analysis is None:
            continue

        lordships = (
            ", ".join(
                str(value)
                for value in analysis.house_lordships
            )
            or "none"
        )

        report.append(
            f"{name}: "
            f"{analysis.sign} "
            f"{analysis.sign_degree:.2f}°, "
            f"House {analysis.house}; "
            f"rules [{lordships}]; "
            f"natural={analysis.natural_type}; "
            f"functional={analysis.functional_type}."
        )

    return report


__all__ = [
    "PlanetInterpretation",
    "SIGNS",
    "SIGN_LORDS",
    "sign_index",
    "house_from_sign",
    "sign_for_house",
    "house_lord",
    "planetary_lordships",
    "natural_planet_type",
    "functional_planet_type",
    "interpret_planet",
    "analyze_planets",
    "planet_analysis_report",
]