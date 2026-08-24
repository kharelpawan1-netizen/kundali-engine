"""
yogas/guru_chandal.py

Structural Parashari Guru Chandal Yoga detection.

Classical structural condition:
    Jupiter and Rahu are conjunct.

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

Note on classical scope:
    Some classical sources also recognize a Ketu-based variant of
    this Yoga. This module intentionally implements only the
    Jupiter-Rahu conjunction, which is the most widely cited
    structural form of Guru Chandal Yoga. A Ketu-based variant, if
    required, belongs in a separate module.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base import YogaResult
from .context import planet_house


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

GURU_CHANDAL_YOGA_NAME = "Guru Chandal Yoga"

JUPITER = "Jupiter"
RAHU = "Rahu"


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


def jupiter_rahu_conjunct(
    context: Any,
) -> bool:
    """
    Return True when Jupiter and Rahu occupy the same house.

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

    jupiter_house = get_planet_house(
        context,
        JUPITER,
    )

    rahu_house = get_planet_house(
        context,
        RAHU,
    )

    if (
        jupiter_house is None
        or rahu_house is None
    ):
        return False

    return jupiter_house == rahu_house


# ============================================================
# EVIDENCE
# ============================================================

def guru_chandal_evidence(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Return structural evidence for Guru Chandal Yoga.

    When Jupiter and Rahu are conjunct, one evidence dictionary
    is returned.

    Otherwise an empty list is returned.
    """

    jupiter_house = get_planet_house(
        context,
        JUPITER,
    )

    rahu_house = get_planet_house(
        context,
        RAHU,
    )

    if (
        jupiter_house is None
        or rahu_house is None
    ):
        return []

    if jupiter_house != rahu_house:
        return []

    return [
        {
            "planet_a": JUPITER,
            "planet_b": RAHU,
            "jupiter_house": jupiter_house,
            "rahu_house": rahu_house,
            "association": "conjunction",
        }
    ]


# ============================================================
# RESULT CREATION
# ============================================================

def _make_guru_chandal_result(
    context: Any,
) -> YogaResult:
    """
    Build the detected Guru Chandal Yoga result.
    """

    jupiter_house = get_planet_house(
        context,
        JUPITER,
    )

    rahu_house = get_planet_house(
        context,
        RAHU,
    )

    evidence = [
        (
            "Jupiter and Rahu are conjunct in house "
            f"{jupiter_house}."
        )
    ]

    conditions_met = [
        (
            "Jupiter and Rahu occupy the same house, "
            "forming the structural conjunction."
        )
    ]

    return YogaResult(
        name=GURU_CHANDAL_YOGA_NAME,
        detected=True,
        category="Guru Chandal Yoga",
        description=(
            "A structural Guru Chandal Yoga is formed "
            "through the conjunction of Jupiter and Rahu."
        ),
        evidence=evidence,
        involved_planets=[
            JUPITER,
            RAHU,
        ],
        involved_houses=[
            jupiter_house,
        ],
        conditions_met=conditions_met,
        metadata={
            "formation": "jupiter_rahu_conjunction",
            "association_type": "conjunction",
            "jupiter_house": jupiter_house,
            "rahu_house": rahu_house,
        },
    )


def _make_guru_chandal_not_detected_result(
    context: Any,
) -> YogaResult:
    """
    Build the non-detected Guru Chandal Yoga result.
    """

    jupiter_house = get_planet_house(
        context,
        JUPITER,
    )

    rahu_house = get_planet_house(
        context,
        RAHU,
    )

    return YogaResult(
        name=GURU_CHANDAL_YOGA_NAME,
        detected=False,
        category="Guru Chandal Yoga",
        description=(
            "No structural Jupiter-Rahu conjunction "
            "was found."
        ),
        conditions_failed=[
            (
                "Jupiter and Rahu must occupy the same "
                "house for the structural conjunction."
            )
        ],
        metadata={
            "formation": "jupiter_rahu_conjunction",
            "association_type": "conjunction",
            "jupiter_house": jupiter_house,
            "rahu_house": rahu_house,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_guru_chandal(
    context: Any,
) -> YogaResult:
    """
    Detect structural Guru Chandal Yoga.

    Returns:
        YogaResult with detected=True when Jupiter and Rahu
        occupy the same house.

        YogaResult with detected=False otherwise.

    This function always returns YogaResult because the common
    YogaAnalyzer contract expects every YogaRule evaluation to
    return a YogaResult.
    """

    if not jupiter_rahu_conjunct(
        context
    ):
        return _make_guru_chandal_not_detected_result(
            context
        )

    return _make_guru_chandal_result(
        context
    )


# ============================================================
# RULE ADAPTER
# ============================================================

class GuruChandalYogaRule:
    """
    YogaRule adapter for YogaAnalyzer.
    """

    name = GURU_CHANDAL_YOGA_NAME
    category = "Guru Chandal Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """
        Evaluate Guru Chandal Yoga.
        """

        return detect_guru_chandal(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "GURU_CHANDAL_YOGA_NAME",
    "JUPITER",
    "RAHU",
    "get_planet_house",
    "jupiter_rahu_conjunct",
    "guru_chandal_evidence",
    "detect_guru_chandal",
    "GuruChandalYogaRule",
]
