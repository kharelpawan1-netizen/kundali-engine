"""
yogas/budha_aditya.py

Structural Parashari Budha-Aditya Yoga detection.

Classical structural condition:
    Sun and Mercury are conjunct.

This module evaluates only the structural conjunction.

It does NOT evaluate:
    - planetary dignity
    - exaltation or debilitation
    - combustion
    - retrogression
    - planetary strength
    - Shadbala
    - affliction
    - cancellation
    - timing
    - dasha
    - transits
    - manifestation

Those concerns belong to later interpretation layers.

The conjunction is evaluated by house placement, consistent with
the structural whole-sign approach used by the current Yoga modules.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import YogaResult
from .context import planet_house


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

BUDHA_ADITYA_YOGA_NAME = "Budha-Aditya Yoga"

SUN = "Sun"
MERCURY = "Mercury"


# ============================================================
# PLANET HELPERS
# ============================================================

def get_planet_house(
    context: Any,
    planet_name: str,
) -> Optional[int]:
    """
    Return the house occupied by a planet.

    Returns None when the planet or its house information
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


def sun_mercury_conjunct(
    context: Any,
) -> bool:
    """
    Return True when Sun and Mercury occupy the same house.

    This is a structural whole-sign conjunction.

    The function intentionally does not inspect:
        - planetary longitude
        - combustion
        - dignity
        - strength
        - retrogression
        - aspects
        - cancellation
    """

    sun_house = get_planet_house(
        context,
        SUN,
    )

    mercury_house = get_planet_house(
        context,
        MERCURY,
    )

    if (
        sun_house is None
        or mercury_house is None
    ):
        return False

    return sun_house == mercury_house


# ============================================================
# EVIDENCE
# ============================================================

def budha_aditya_evidence(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Return structural evidence for Budha-Aditya Yoga.

    When Sun and Mercury are conjunct, one evidence dictionary
    is returned.

    Otherwise an empty list is returned.
    """

    sun_house = get_planet_house(
        context,
        SUN,
    )

    mercury_house = get_planet_house(
        context,
        MERCURY,
    )

    if (
        sun_house is None
        or mercury_house is None
    ):
        return []

    if sun_house != mercury_house:
        return []

    return [
        {
            "planet_a": SUN,
            "planet_b": MERCURY,
            "sun_house": sun_house,
            "mercury_house": mercury_house,
            "association": "conjunction",
        }
    ]


# ============================================================
# RESULT CREATION
# ============================================================

def _make_budha_aditya_result(
    context: Any,
) -> YogaResult:
    """
    Build the detected Budha-Aditya Yoga result.
    """

    sun_house = get_planet_house(
        context,
        SUN,
    )

    mercury_house = get_planet_house(
        context,
        MERCURY,
    )

    evidence = [
        (
            "Sun and Mercury are conjunct in house "
            f"{sun_house}."
        )
    ]

    conditions_met = [
        (
            "Sun and Mercury occupy the same house, "
            "forming the structural conjunction."
        )
    ]

    return YogaResult(
        name=BUDHA_ADITYA_YOGA_NAME,
        detected=True,
        category="Budha-Aditya Yoga",
        description=(
            "A structural Budha-Aditya Yoga is formed "
            "through the conjunction of Sun and Mercury."
        ),
        evidence=evidence,
        involved_planets=[
            SUN,
            MERCURY,
        ],
        involved_houses=[
            sun_house,
        ],
        conditions_met=conditions_met,
        metadata={
            "formation": "sun_mercury_conjunction",
            "association_type": "conjunction",
            "sun_house": sun_house,
            "mercury_house": mercury_house,
        },
    )


def _make_budha_aditya_not_detected_result(
    context: Any,
) -> YogaResult:
    """
    Build the non-detected Budha-Aditya Yoga result.
    """

    sun_house = get_planet_house(
        context,
        SUN,
    )

    mercury_house = get_planet_house(
        context,
        MERCURY,
    )

    return YogaResult(
        name=BUDHA_ADITYA_YOGA_NAME,
        detected=False,
        category="Budha-Aditya Yoga",
        description=(
            "No structural Sun-Mercury conjunction "
            "was found."
        ),
        conditions_failed=[
            (
                "Sun and Mercury must occupy the same "
                "house for the structural conjunction."
            )
        ],
        metadata={
            "formation": "sun_mercury_conjunction",
            "association_type": "conjunction",
            "sun_house": sun_house,
            "mercury_house": mercury_house,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_budha_aditya(
    context: Any,
) -> YogaResult:
    """
    Detect structural Budha-Aditya Yoga.

    Returns:
        YogaResult with detected=True when Sun and Mercury
        occupy the same house.

        YogaResult with detected=False otherwise.

    This function always returns YogaResult because the common
    YogaAnalyzer contract expects every YogaRule evaluation to
    return a YogaResult.
    """

    if not sun_mercury_conjunct(
        context
    ):
        return _make_budha_aditya_not_detected_result(
            context
        )

    return _make_budha_aditya_result(
        context
    )


# ============================================================
# RULE ADAPTER
# ============================================================

class BudhaAdityaYogaRule:
    """
    YogaRule adapter for YogaAnalyzer.
    """

    name = BUDHA_ADITYA_YOGA_NAME
    category = "Budha-Aditya Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """
        Evaluate Budha-Aditya Yoga.
        """

        return detect_budha_aditya(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "BUDHA_ADITYA_YOGA_NAME",
    "SUN",
    "MERCURY",
    "get_planet_house",
    "sun_mercury_conjunct",
    "budha_aditya_evidence",
    "detect_budha_aditya",
    "BudhaAdityaYogaRule",
]