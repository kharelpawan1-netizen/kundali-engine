"""
yogas/dhanayoga.py

Structural Parashari Dhana Yoga detection.

Primary wealth houses:
    2nd  - accumulated wealth, family resources, stored assets
    11th - gains, income, profits, fulfillment of desires

Supporting wealth houses:
    1st  - self and personal capacity
    5th  - intelligence, merit, purva punya
    9th  - fortune, dharma, blessings

Structural formations currently supported:
    1. 2nd lord placed in the 11th house.
    2. 11th lord placed in the 2nd house.
    3. Association of 2nd and 11th lords by conjunction.
    4. Association of a primary wealth lord with a
       supporting wealth-house lord by conjunction.

This module evaluates structural formation only.

It does NOT evaluate:
    - planetary dignity
    - exaltation/debilitation
    - combustion
    - retrogression
    - planetary strength
    - Shadbala
    - affliction
    - cancellation
    - timing
    - dasha
    - transits
    - actual financial manifestation

Those concerns belong to later interpretation layers.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .base import YogaResult
from .context import planet_house


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

DHANA_YOGA_NAME = "Dhana Yoga"

WEALTH_HOUSES: Tuple[int, ...] = (
    2,
    11,
)

DHANA_HOUSES: Tuple[int, ...] = WEALTH_HOUSES

SUPPORTING_WEALTH_HOUSES: Tuple[int, ...] = (
    1,
    5,
    9,
)


# ============================================================
# HOUSE CLASSIFICATION
# ============================================================

def is_wealth_house(
    house: int,
) -> bool:
    """
    Return True when the house is a primary wealth house.
    """

    return house in WEALTH_HOUSES


def is_dhana_house(
    house: int,
) -> bool:
    """
    Compatibility alias for is_wealth_house().
    """

    return is_wealth_house(house)


def is_supporting_wealth_house(
    house: int,
) -> bool:
    """
    Return True when the house supports wealth formation.
    """

    return house in SUPPORTING_WEALTH_HOUSES


def is_wealth_related_house(
    house: int,
) -> bool:
    """
    Return True when the house is either a primary wealth
    house or a supporting wealth house.
    """

    return (
        is_wealth_house(house)
        or is_supporting_wealth_house(house)
    )


# ============================================================
# HOUSE LORD
# ============================================================

def house_lord(
    context: Any,
    house: int,
) -> Optional[str]:
    """
    Return the planetary lord of a house.

    Supported representation:

        context.houses = {
            1: House(...),
            2: House(...),
            ...
        }

    Each house object must expose a `lord` attribute.

    Returns None when the house or lord is unavailable.
    """

    if not isinstance(house, int):
        raise TypeError(
            "house must be an integer."
        )

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    houses = getattr(
        context,
        "houses",
        None,
    )

    if houses is None:
        return None

    house_object = None

    if hasattr(houses, "get"):
        house_object = houses.get(house)

        if house_object is None:
            house_object = houses.get(
                str(house)
            )

    if house_object is None:
        return None

    lord = getattr(
        house_object,
        "lord",
        None,
    )

    if lord is None:
        return None

    lord = str(lord).strip()

    if not lord:
        return None

    return lord


# ============================================================
# PLANET ASSOCIATION
# ============================================================

def planets_conjunct(
    context: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Return True when two different planets occupy the same house.

    This is a whole-sign structural conjunction.
    """

    if not planet_a or not planet_b:
        return False

    if planet_a == planet_b:
        return False

    house_a = planet_house(
        context,
        planet_a,
    )

    house_b = planet_house(
        context,
        planet_b,
    )

    if (
        house_a is None
        or house_b is None
    ):
        return False

    return house_a == house_b


def lords_have_association(
    context: Any,
    lord_a: str,
    lord_b: str,
) -> bool:
    """
    Determine whether two different house lords are associated.

    The current structural association rule is conjunction.

    A planet cannot be considered conjunct with itself.
    """

    if not lord_a or not lord_b:
        return False

    if lord_a == lord_b:
        return False

    return planets_conjunct(
        context,
        lord_a,
        lord_b,
    )


# ============================================================
# WEALTH LORD PLACEMENTS
# ============================================================

def find_wealth_lords_in_wealth_houses(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Find primary wealth-house lords placed in primary
    wealth houses.

    Supported structural formations:

        2nd lord  -> 11th house
        11th lord -> 2nd house

    A lord is included only when its occupied house is
    explicitly available and belongs to WEALTH_HOUSES.

    Returns dictionaries containing:

        source_house
        lord
        occupied_house
    """

    findings: List[Dict[str, Any]] = []

    for source_house in WEALTH_HOUSES:

        lord = house_lord(
            context,
            source_house,
        )

        if lord is None:
            continue

        occupied_house = planet_house(
            context,
            lord,
        )

        if occupied_house is None:
            continue

        if occupied_house not in WEALTH_HOUSES:
            continue

        findings.append(
            {
                "source_house": source_house,
                "lord": lord,
                "occupied_house": occupied_house,
            }
        )

    return findings


# ============================================================
# PRIMARY DHANA LORD ASSOCIATIONS
# ============================================================

def find_wealth_lord_associations(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Find conjunctions between the lords of the 2nd and 11th houses.

    Same-planet cases are excluded because a planet is not
    considered conjunct with itself.
    """

    associations: List[Dict[str, Any]] = []

    second_lord = house_lord(
        context,
        2,
    )

    eleventh_lord = house_lord(
        context,
        11,
    )

    if (
        second_lord is None
        or eleventh_lord is None
    ):
        return associations

    if second_lord == eleventh_lord:
        return associations

    if not lords_have_association(
        context,
        second_lord,
        eleventh_lord,
    ):
        return associations

    associations.append(
        {
            "wealth_house_a": 2,
            "wealth_lord_a": second_lord,
            "wealth_house_b": 11,
            "wealth_lord_b": eleventh_lord,
            "association": "conjunction",
        }
    )

    return associations


# ============================================================
# SUPPORTING DHANA ASSOCIATIONS
# ============================================================

def find_supporting_wealth_associations(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Find conjunctions between a primary wealth-house lord
    and a supporting wealth-house lord.

    Primary wealth houses:
        2, 11

    Supporting houses:
        1, 5, 9
    """

    associations: List[Dict[str, Any]] = []

    for wealth_house in WEALTH_HOUSES:

        wealth_lord = house_lord(
            context,
            wealth_house,
        )

        if wealth_lord is None:
            continue

        for supporting_house in SUPPORTING_WEALTH_HOUSES:

            supporting_lord = house_lord(
                context,
                supporting_house,
            )

            if supporting_lord is None:
                continue

            if wealth_lord == supporting_lord:
                continue

            if not lords_have_association(
                context,
                wealth_lord,
                supporting_lord,
            ):
                continue

            associations.append(
                {
                    "wealth_house": wealth_house,
                    "wealth_lord": wealth_lord,
                    "supporting_house": supporting_house,
                    "supporting_lord": supporting_lord,
                    "association": "conjunction",
                }
            )

    return associations


# ============================================================
# COMBINED STRUCTURAL ANALYSIS
# ============================================================

def find_dhana_associations(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Return all currently supported structural Dhana Yoga
    associations and placements.
    """

    associations: List[Dict[str, Any]] = []

    wealth_lord_placements = (
        find_wealth_lords_in_wealth_houses(
            context
        )
    )

    for finding in wealth_lord_placements:

        associations.append(
            {
                "source_house": finding[
                    "source_house"
                ],
                "lord": finding[
                    "lord"
                ],
                "occupied_house": finding[
                    "occupied_house"
                ],
                "formation": (
                    "wealth_lord_in_wealth_house"
                ),
            }
        )

    associations.extend(
        find_wealth_lord_associations(
            context
        )
    )

    associations.extend(
        find_supporting_wealth_associations(
            context
        )
    )

    return associations


# ============================================================
# RESULT CREATION
# ============================================================

def _make_dhana_yoga_result(
    associations: List[Dict[str, Any]],
) -> YogaResult:
    """
    Build a structured YogaResult from detected associations.
    """

    involved_planets: List[str] = []
    involved_houses: List[int] = []
    evidence: List[str] = []
    conditions_met: List[str] = []

    for association in associations:

        # ----------------------------------------------------
        # Wealth lord placed in wealth house
        # ----------------------------------------------------

        if "source_house" in association:

            source_house = association[
                "source_house"
            ]

            lord = association[
                "lord"
            ]

            occupied_house = association[
                "occupied_house"
            ]

            if lord not in involved_planets:
                involved_planets.append(
                    lord
                )

            if source_house not in involved_houses:
                involved_houses.append(
                    source_house
                )

            if occupied_house not in involved_houses:
                involved_houses.append(
                    occupied_house
                )

            evidence.append(
                (
                    f"{lord}, lord of house "
                    f"{source_house}, is placed in "
                    f"wealth house {occupied_house}."
                )
            )

            conditions_met.append(
                (
                    f"Lord of wealth house "
                    f"{source_house} occupies wealth "
                    f"house {occupied_house}."
                )
            )

            continue

        # ----------------------------------------------------
        # Primary wealth-lord conjunction
        # ----------------------------------------------------

        if "wealth_house_a" in association:

            wealth_house_a = association[
                "wealth_house_a"
            ]

            wealth_house_b = association[
                "wealth_house_b"
            ]

            wealth_lord_a = association[
                "wealth_lord_a"
            ]

            wealth_lord_b = association[
                "wealth_lord_b"
            ]

            if wealth_lord_a not in involved_planets:
                involved_planets.append(
                    wealth_lord_a
                )

            if wealth_lord_b not in involved_planets:
                involved_planets.append(
                    wealth_lord_b
                )

            if wealth_house_a not in involved_houses:
                involved_houses.append(
                    wealth_house_a
                )

            if wealth_house_b not in involved_houses:
                involved_houses.append(
                    wealth_house_b
                )

            evidence.append(
                (
                    f"{wealth_lord_a}, lord of house "
                    f"{wealth_house_a}, is conjunct "
                    f"{wealth_lord_b}, lord of house "
                    f"{wealth_house_b}."
                )
            )

            conditions_met.append(
                (
                    f"Lords of wealth houses "
                    f"{wealth_house_a} and "
                    f"{wealth_house_b} are associated "
                    f"by conjunction."
                )
            )

            continue

        # ----------------------------------------------------
        # Supporting wealth association
        # ----------------------------------------------------

        wealth_house = association[
            "wealth_house"
        ]

        supporting_house = association[
            "supporting_house"
        ]

        wealth_lord = association[
            "wealth_lord"
        ]

        supporting_lord = association[
            "supporting_lord"
        ]

        if wealth_lord not in involved_planets:
            involved_planets.append(
                wealth_lord
            )

        if supporting_lord not in involved_planets:
            involved_planets.append(
                supporting_lord
            )

        if wealth_house not in involved_houses:
            involved_houses.append(
                wealth_house
            )

        if supporting_house not in involved_houses:
            involved_houses.append(
                supporting_house
            )

        evidence.append(
            (
                f"{wealth_lord}, lord of wealth house "
                f"{wealth_house}, is conjunct "
                f"{supporting_lord}, lord of supporting "
                f"house {supporting_house}."
            )
        )

        conditions_met.append(
            (
                f"Wealth-house lord of house "
                f"{wealth_house} is associated with "
                f"supporting wealth-house lord of house "
                f"{supporting_house} by conjunction."
            )
        )

    return YogaResult(
        name=DHANA_YOGA_NAME,
        detected=True,
        category="Dhana Yoga",
        description=(
            "A structural Dhana Yoga is formed through "
            "wealth-house lord placement and/or association "
            "of wealth-related house lords."
        ),
        evidence=evidence,
        involved_planets=involved_planets,
        involved_houses=sorted(
            involved_houses
        ),
        conditions_met=conditions_met,
        metadata={
            "formation": "wealth_house_structure",
            "wealth_houses": list(
                WEALTH_HOUSES
            ),
            "dhana_houses": list(
                DHANA_HOUSES
            ),
            "supporting_wealth_houses": list(
                SUPPORTING_WEALTH_HOUSES
            ),
            "association_type": "conjunction",
            "associations": associations,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_dhanayoga(
    context: Any,
) -> YogaResult:
    """
    Detect structural Dhana Yoga.

    Returns a YogaResult in every case.
    """

    associations = find_dhana_associations(
        context
    )

    if not associations:

        return YogaResult(
            name=DHANA_YOGA_NAME,
            detected=False,
            category="Dhana Yoga",
            description=(
                "No qualifying structural Dhana Yoga "
                "formation was found."
            ),
            conditions_failed=[
                (
                    "No wealth lord is placed in a primary "
                    "wealth house and no qualifying wealth-house "
                    "lord association was detected."
                )
            ],
            metadata={
                "wealth_houses": list(
                    WEALTH_HOUSES
                ),
                "dhana_houses": list(
                    DHANA_HOUSES
                ),
                "supporting_wealth_houses": list(
                    SUPPORTING_WEALTH_HOUSES
                ),
            },
        )

    return _make_dhana_yoga_result(
        associations
    )


# ============================================================
# RULE ADAPTER
# ============================================================

class DhanaYogaRule:
    """
    YogaRule-compatible adapter for Dhana Yoga.
    """

    name = DHANA_YOGA_NAME
    category = "Dhana Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """
        Evaluate Dhana Yoga.
        """

        return detect_dhanayoga(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "DHANA_YOGA_NAME",
    "WEALTH_HOUSES",
    "DHANA_HOUSES",
    "SUPPORTING_WEALTH_HOUSES",
    "is_wealth_house",
    "is_dhana_house",
    "is_supporting_wealth_house",
    "is_wealth_related_house",
    "house_lord",
    "planets_conjunct",
    "lords_have_association",
    "find_wealth_lords_in_wealth_houses",
    "find_wealth_lord_associations",
    "find_supporting_wealth_associations",
    "find_dhana_associations",
    "detect_dhanayoga",
    "DhanaYogaRule",
]