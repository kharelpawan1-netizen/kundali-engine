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

This module does not:
    - calculate planetary positions
    - calculate houses
    - calculate dignity
    - detect Yogas
    - calculate Dashas
    - generate deterministic predictions

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


VALID_HOUSES = range(1, 13)
VALID_PADAS = range(1, 5)


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
        raise ValueError(
            "Planet sign cannot be None."
        )

    text = str(sign).strip()

    if not text:
        raise ValueError(
            "Planet sign cannot be empty."
        )

    normalized = text.lower()

    for sign_name in SIGNS:

        canonical = sign_name.lower()

        if normalized == canonical:
            return sign_name

        if normalized == canonical.replace(
            " ",
            "_",
        ):
            return sign_name

    # Handle enum-style representations such as:
    # ZodiacSign.SAGITTARIUS
    for sign_name in SIGNS:

        if sign_name.lower() in normalized:
            return sign_name

    raise ValueError(
        f"Unknown zodiac sign representation: {sign!r}"
    )


def _planet_name(planet: Any) -> str:
    """Extract a canonical planet name."""

    name = getattr(
        planet,
        "name",
        planet,
    )

    text = str(name).strip()

    if not text:
        raise ValueError(
            "Planet name cannot be empty."
        )

    normalized = text.lower()

    for candidate in PLANETS:

        if normalized == candidate.lower():
            return candidate

    # Handle enum-style representations such as:
    # Planet.MARS
    for candidate in PLANETS:

        if candidate.lower() in normalized:
            return candidate

    raise ValueError(
        f"Unknown planet representation: {name!r}"
    )


def _validate_house(
    house: Any,
) -> int:
    """
    Validate and normalize a house number.

    Houses are strictly 1 through 12.
    """

    try:
        normalized = int(house)

    except (TypeError, ValueError) as exc:

        raise ValueError(
            f"Invalid house number: {house!r}"
        ) from exc

    if normalized not in VALID_HOUSES:
        raise ValueError(
            "House must be between 1 and 12."
        )

    return normalized


def _validate_sign_degree(
    degree: Any,
) -> float:
    """
    Validate a planetary degree within a zodiac sign.

    A sign-local degree must satisfy:

        0 <= degree < 30
    """

    try:
        normalized = float(degree)

    except (TypeError, ValueError) as exc:

        raise ValueError(
            f"Invalid sign degree: {degree!r}"
        ) from exc

    if not 0.0 <= normalized < 30.0:
        raise ValueError(
            "sign_degree must be between "
            "0.0 inclusive and 30.0 exclusive."
        )

    return normalized


def _validate_pada(
    pada: Any,
) -> Optional[int]:
    """
    Validate a Nakshatra pada.

    A pada is optional because some calculation layers may
    not expose Nakshatra information.
    """

    if pada is None:
        return None

    try:
        normalized = int(pada)

    except (TypeError, ValueError) as exc:

        raise ValueError(
            f"Invalid Nakshatra pada: {pada!r}"
        ) from exc

    if normalized not in VALID_PADAS:
        raise ValueError(
            "Nakshatra pada must be between 1 and 4."
        )

    return normalized


# ============================================================
# SIGN / HOUSE UTILITIES
# ============================================================

def sign_index(
    sign: str,
) -> int:
    """Return zero-based zodiac index."""

    normalized = _normalize_sign(
        sign
    )

    return SIGNS.index(
        normalized
    )


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

    house = _validate_house(
        house
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

    return SIGN_LORDS[
        sign
    ]


def planetary_lordships(
    ascendant_sign: str,
    planet: str,
) -> List[int]:
    """
    Return houses owned by a planet.

    Rahu and Ketu have no classical Parashari sign ownership
    in this foundational interpretation layer.
    """

    planet = _planet_name(
        planet
    )

    if planet in {
        "Rahu",
        "Ketu",
    }:
        return []

    houses = []

    for house in VALID_HOUSES:

        if house_lord(
            ascendant_sign,
            house,
        ) == planet:

            houses.append(
                house
            )

    return houses


# ============================================================
# NATURAL NATURE
# ============================================================

def natural_planet_type(
    planet: str,
) -> str:
    """
    Return the foundational natural benefic/malefic
    classification.

    This is intentionally simplified.

    A future advanced layer may refine:
        - Moon waxing/waning condition
        - Mercury association
        - combustion
        - conjunction-based modification
        - other classical contextual factors
    """

    planet = _planet_name(
        planet
    )

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
    Determine a foundational Parashari functional classification.

    This classification is deliberately conservative.

    It is not a complete assessment of:
        - Yogakaraka status
        - planetary strength
        - association
        - dignity
        - combustion
        - retrogression
        - aspects
        - Shadbala
        - Yoga formation

    Those belong to their respective interpretation layers.
    """

    ascendant_sign = _normalize_sign(
        ascendant_sign
    )

    planet = _planet_name(
        planet
    )

    houses = planetary_lordships(
        ascendant_sign,
        planet,
    )

    # Nodes are handled separately because classical
    # Parashari sign ownership is not assigned to them here.
    if planet in {
        "Rahu",
        "Ketu",
    }:
        return "node"

    # Lagna lord receives a strong functional benefic bias.
    if 1 in houses:
        return "functional_benefic"

    # Lords of the 5th or 9th have strong trinal
    # functional benefic significance.
    if any(
        house in houses
        for house in (
            5,
            9,
        )
    ):
        return "functional_benefic"

    # Dusthana ownership is treated as functionally
    # challenging in this foundational layer.
    if any(
        house in houses
        for house in (
            6,
            8,
            12,
        )
    ):
        return "functional_malefic"

    # 2nd and 11th are wealth-related houses and require
    # contextual interpretation rather than being classified
    # as inherently benefic or malefic here.
    if any(
        house in houses
        for house in (
            2,
            11,
        )
    ):
        return "conditional"

    # The 3rd is generally treated as functionally
    # challenging in this foundational classification.
    if 3 in houses:
        return "functional_malefic"

    # Kendra lordship, especially 4th and 7th, requires
    # contextual judgment and is therefore left conditional.
    if any(
        house in houses
        for house in (
            4,
            7,
        )
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

    The interpretation layer does not calculate dignity.

    Existing dignity calculations remain the source of truth.
    """

    dignity = getattr(
        planet,
        "dignity",
        None,
    )

    if dignity is None:
        return None

    text = str(
        dignity
    ).strip()

    if not text:
        return None

    return text


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
    and specialized interpretation modules can use.
    """

    if chart is None:
        raise ValueError(
            "chart must not be None."
        )

    if planet is None:
        raise ValueError(
            "planet must not be None."
        )

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
        # sign_enum(), but keep this module independent
        # from calculation implementation details.
        try:
            from astronomy.signs import sign_enum

            ascendant_sign = _normalize_sign(
                sign_enum(
                    ascendant
                )
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

    raw_house = getattr(
        planet,
        "house",
        None,
    )

    if raw_house is None:

        house = house_from_sign(
            ascendant_sign,
            sign,
        )

    else:

        house = _validate_house(
            raw_house
        )

    degree = _validate_sign_degree(
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
        ).strip()

        if not nakshatra:
            nakshatra = None

    pada = _validate_pada(
        getattr(
            planet,
            "pada",
            None,
        )
    )

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
        HOUSE_THEMES[
            house
        ]
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

    if chart is None:
        raise ValueError(
            "chart must not be None."
        )

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
        raise ValueError(
            "Chart planets must be a mapping."
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


# ============================================================
# PUBLIC API
# ============================================================

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