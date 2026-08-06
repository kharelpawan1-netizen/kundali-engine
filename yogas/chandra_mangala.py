"""
yogas/chandra_mangala.py

Structural Parashari Chandra-Mangala Yoga detection.

Structural condition implemented in this module:
    Moon and Mars occupy the same house.

This module evaluates structural formation only.

It does NOT evaluate:
    - planetary dignity
    - exaltation or debilitation
    - combustion
    - retrogression
    - planetary strength
    - Shadbala
    - affliction
    - cancellation
    - mutual aspects
    - sign exchange
    - dasha timing
    - transit timing
    - actual manifestation

Those concerns belong to separate interpretation layers.

The current implementation uses whole-sign house placement,
consistent with the structural conjunction approach used by
the existing Yoga modules.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import YogaResult
from .context import planet_house


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

CHANDRA_MANGALA_YOGA_NAME = "Chandra-Mangala Yoga"

MOON = "Moon"
MARS = "Mars"


# ============================================================
# PLANET HOUSE HELPER
# ============================================================

def get_planet_house(
    context: Any,
    planet_name: str,
) -> Optional[int]:
    """
    Return the house occupied by a planet.

    Returns None when the planet or valid house information
    is unavailable.
    """

    if not planet_name:
        return None

    house = planet_house(
        context,
        planet_name,
    )

    if house is None:
        return None

    try:
        house = int(house)
    except (TypeError, ValueError):
        return None

    if not 1 <= house <= 12:
        return None

    return house


# ============================================================
# CONJUNCTION
# ============================================================

def moon_mars_conjunct(
    context: Any,
) -> bool:
    """
    Return True when Moon and Mars occupy the same house.

    This is a structural whole-sign conjunction.

    No planetary longitude, dignity, strength, combustion,
    retrogression, aspect, cancellation, or timing condition
    is evaluated here.
    """

    moon_house = get_planet_house(
        context,
        MOON,
    )

    mars_house = get_planet_house(
        context,
        MARS,
    )

    if (
        moon_house is None
        or mars_house is None
    ):
        return False

    return moon_house == mars_house


# ============================================================
# EVIDENCE
# ============================================================

def chandra_mangala_evidence(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Return structural evidence for Chandra-Mangala Yoga.

    Returns one evidence dictionary when Moon and Mars are
    conjunct, otherwise an empty list.
    """

    moon_house = get_planet_house(
        context,
        MOON,
    )

    mars_house = get_planet_house(
        context,
        MARS,
    )

    if (
        moon_house is None
        or mars_house is None
    ):
        return []

    if moon_house != mars_house:
        return []

    return [
        {
            "planet_a": MOON,
            "planet_b": MARS,
            "moon_house": moon_house,
            "mars_house": mars_house,
            "association": "conjunction",
        }
    ]


# ============================================================
# RESULT CREATION
# ============================================================

def _make_chandra_mangala_result(
    context: Any,
) -> YogaResult:
    """
    Build the detected Chandra-Mangala Yoga result.
    """

    moon_house = get_planet_house(
        context,
        MOON,
    )

    mars_house = get_planet_house(
        context,
        MARS,
    )

    evidence = [
        (
            "Moon and Mars are conjunct in house "
            f"{moon_house}."
        )
    ]

    conditions_met = [
        (
            "Moon and Mars occupy the same house, "
            "forming the structural conjunction."
        )
    ]

    return YogaResult(
        name=CHANDRA_MANGALA_YOGA_NAME,
        detected=True,
        category="Chandra-Mangala Yoga",
        description=(
            "A structural Chandra-Mangala Yoga is formed "
            "through the conjunction of Moon and Mars."
        ),
        evidence=evidence,
        involved_planets=[
            MOON,
            MARS,
        ],
        involved_houses=[
            moon_house,
        ],
        conditions_met=conditions_met,
        metadata={
            "formation": "moon_mars_conjunction",
            "association_type": "conjunction",
            "moon_house": moon_house,
            "mars_house": mars_house,
        },
    )


def _make_chandra_mangala_not_detected_result(
    context: Any,
) -> YogaResult:
    """
    Build the non-detected Chandra-Mangala Yoga result.
    """

    moon_house = get_planet_house(
        context,
        MOON,
    )

    mars_house = get_planet_house(
        context,
        MARS,
    )

    return YogaResult(
        name=CHANDRA_MANGALA_YOGA_NAME,
        detected=False,
        category="Chandra-Mangala Yoga",
        description=(
            "No structural Moon-Mars conjunction "
            "was found."
        ),
        conditions_failed=[
            (
                "Moon and Mars must occupy the same "
                "house for the structural conjunction."
            )
        ],
        metadata={
            "formation": "moon_mars_conjunction",
            "association_type": "conjunction",
            "moon_house": moon_house,
            "mars_house": mars_house,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_chandra_mangala(
    context: Any,
) -> YogaResult:
    """
    Detect structural Chandra-Mangala Yoga.

    Returns a YogaResult in every case.

    detected=True:
        Moon and Mars occupy the same house.

    detected=False:
        Moon and Mars do not occupy the same house, or
        required planetary house information is unavailable.
    """

    if not moon_mars_conjunct(
        context
    ):
        return _make_chandra_mangala_not_detected_result(
            context
        )

    return _make_chandra_mangala_result(
        context
    )


# ============================================================
# RULE ADAPTER
# ============================================================

class ChandraMangalaYogaRule:
    """
    YogaRule adapter for YogaAnalyzer.
    """

    name = CHANDRA_MANGALA_YOGA_NAME
    category = "Chandra-Mangala Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """
        Evaluate Chandra-Mangala Yoga.
        """

        return detect_chandra_mangala(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "CHANDRA_MANGALA_YOGA_NAME",
    "MOON",
    "MARS",
    "get_planet_house",
    "moon_mars_conjunct",
    "chandra_mangala_evidence",
    "detect_chandra_mangala",
    "ChandraMangalaYogaRule",
]