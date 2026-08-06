"""
yogas/gaja_kesari.py

Structural Gaja Kesari Yoga detection.

Classical Parashari condition:
Jupiter must occupy a Kendra (1st, 4th, 7th, or 10th)
from the Moon.

This module evaluates structural formation only.

It does not evaluate:
    - planetary strength
    - dignity
    - combustion
    - retrogression
    - affliction
    - cancellation
    - timing
    - manifestation

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import YogaResult, YogaRule


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

GAJA_KESARI_NAME = "Gaja Kesari Yoga"

SUN = "Sun"
MOON = "Moon"
JUPITER = "Jupiter"

KENDRA_HOUSES = (
    1,
    4,
    7,
    10,
)

KENDRA_RELATIVE_HOUSES = KENDRA_HOUSES

KENDRA_FROM_REFERENCE = KENDRA_HOUSES


# ============================================================
# CONTEXT HELPERS
# ============================================================

def _get_planets(context: Any) -> Any:
    """Return the planet collection from the context."""

    planets = getattr(
        context,
        "planets",
        None,
    )

    if planets is None:
        return {}

    return planets


def _get_planet(
    context: Any,
    name: str,
) -> Optional[Any]:
    """Return a planet by name."""

    planets = _get_planets(
        context
    )

    if hasattr(
        planets,
        "get",
    ):
        return planets.get(
            name
        )

    return None


def _get_house(
    planet: Any,
) -> Optional[int]:
    """
    Return a valid house number from a planet object.

    Returns None when the house is missing or invalid.
    """

    if planet is None:
        return None

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
    ):
        return None

    if not 1 <= house <= 12:
        return None

    return house


# ============================================================
# RELATIVE HOUSE CALCULATION
# ============================================================

def relative_house(
    reference_house: int,
    target_house: int,
) -> int:
    """
    Calculate the inclusive house distance from one house
    to another.

    Examples:

        1 -> 1  = 1
        1 -> 4  = 4
        1 -> 7  = 7
        1 -> 10 = 10

        5 -> 5  = 1
        5 -> 8  = 4
        5 -> 11 = 7
        5 -> 2  = 10
    """

    if not 1 <= reference_house <= 12:
        raise ValueError(
            "reference_house must be between 1 and 12."
        )

    if not 1 <= target_house <= 12:
        raise ValueError(
            "target_house must be between 1 and 12."
        )

    return (
        (target_house - reference_house) % 12
    ) + 1


# ============================================================
# KENDRA LOGIC
# ============================================================

def is_kendra_from_reference(
    reference_house: int,
    target_house: int,
) -> bool:
    """
    Return True when target_house is 1st, 4th, 7th,
    or 10th from reference_house.
    """

    distance = relative_house(
        reference_house,
        target_house,
    )

    return distance in KENDRA_HOUSES


def jupiter_kendra_from_moon(
    context: Any,
) -> bool:
    """
    Determine whether Jupiter is in a Kendra from Moon.

    Returns True when Jupiter is 1st, 4th, 7th, or 10th
    from the Moon.
    """

    moon = _get_planet(
        context,
        MOON,
    )

    jupiter = _get_planet(
        context,
        JUPITER,
    )

    moon_house = _get_house(
        moon
    )

    jupiter_house = _get_house(
        jupiter
    )

    if (
        moon_house is None
        or jupiter_house is None
    ):
        return False

    return is_kendra_from_reference(
        moon_house,
        jupiter_house,
    )


# ============================================================
# EVIDENCE
# ============================================================

def gaja_kesari_evidence(
    context: Any,
) -> list[str]:
    """
    Return evidence explaining the structural condition.

    Returns an empty list when required planetary house
    information is unavailable.
    """

    moon = _get_planet(
        context,
        MOON,
    )

    jupiter = _get_planet(
        context,
        JUPITER,
    )

    moon_house = _get_house(
        moon
    )

    jupiter_house = _get_house(
        jupiter
    )

    if (
        moon_house is None
        or jupiter_house is None
    ):
        return []

    distance = relative_house(
        moon_house,
        jupiter_house,
    )

    if distance not in KENDRA_HOUSES:
        return []

    return [
        (
            f"Jupiter is in house {jupiter_house}, "
            f"which is the {distance}th position from "
            f"Moon in house {moon_house}."
        )
    ]


# ============================================================
# RESULT CREATION
# ============================================================

def _make_yoga_result(
    context: Any,
) -> YogaResult:
    """
    Create a positive Gaja Kesari YogaResult.
    """

    moon = _get_planet(
        context,
        MOON,
    )

    jupiter = _get_planet(
        context,
        JUPITER,
    )

    moon_house = _get_house(
        moon
    )

    jupiter_house = _get_house(
        jupiter
    )

    distance = None

    if (
        moon_house is not None
        and jupiter_house is not None
    ):
        distance = relative_house(
            moon_house,
            jupiter_house,
        )

    evidence = gaja_kesari_evidence(
        context
    )

    return YogaResult(
        name=GAJA_KESARI_NAME,
        detected=True,
        category=GAJA_KESARI_NAME,
        description=(
            "Jupiter occupies a Kendra from the Moon, "
            "forming the structural condition for "
            "Gaja Kesari Yoga."
        ),
        evidence=evidence,
        involved_planets=[
            MOON,
            JUPITER,
        ],
        involved_houses=[
            house
            for house in (
                moon_house,
                jupiter_house,
            )
            if house is not None
        ],
        conditions_met=[
            (
                "Jupiter is positioned in the "
                "1st, 4th, 7th, or 10th position "
                "from Moon."
            )
        ],
        metadata={
            "reference_planet": MOON,
            "target_planet": JUPITER,
            "moon_house": moon_house,
            "jupiter_house": jupiter_house,
            "relative_house": distance,
            "formation": "Jupiter in Kendra from Moon",
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_gaja_kesari(
    context: Any,
) -> Optional[YogaResult]:
    """
    Detect structural Gaja Kesari Yoga.

    Returns:
        YogaResult:
            When the structural condition is present.

        None:
            When the structural condition is absent.

    The None return behavior is intentional and is part of
    the public contract used by the current test suite.
    """

    if not jupiter_kendra_from_moon(
        context
    ):
        return None

    return _make_yoga_result(
        context
    )


# ============================================================
# BACKWARD-COMPATIBLE RESULT HELPER
# ============================================================

def gaja_kesari_result(
    context: Any,
) -> Optional[YogaResult]:
    """
    Backward-compatible alias for detect_gaja_kesari().
    """

    return detect_gaja_kesari(
        context
    )


# ============================================================
# YOGA RULE ADAPTER
# ============================================================

class GajaKesariRule(YogaRule):
    """
    YogaRule adapter for Gaja Kesari Yoga.

    The detector itself returns None when the Yoga is absent,
    while the analyzer contract requires YogaRule.evaluate()
    to return a YogaResult.

    Therefore the rule adapter converts an absent Yoga into
    a negative YogaResult.
    """

    name = GAJA_KESARI_NAME
    category = GAJA_KESARI_NAME

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """Evaluate Gaja Kesari Yoga."""

        result = detect_gaja_kesari(
            context
        )

        if result is not None:
            return result

        return YogaResult(
            name=GAJA_KESARI_NAME,
            detected=False,
            category=GAJA_KESARI_NAME,
            description=(
                "Jupiter is not positioned in a "
                "Kendra from Moon."
            ),
            conditions_failed=[
                (
                    "Jupiter is not positioned in the "
                    "1st, 4th, 7th, or 10th position "
                    "from Moon."
                )
            ],
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "GAJA_KESARI_NAME",
    "SUN",
    "MOON",
    "JUPITER",
    "KENDRA_HOUSES",
    "KENDRA_RELATIVE_HOUSES",
    "KENDRA_FROM_REFERENCE",
    "relative_house",
    "is_kendra_from_reference",
    "jupiter_kendra_from_moon",
    "gaja_kesari_evidence",
    "detect_gaja_kesari",
    "gaja_kesari_result",
    "GajaKesariRule",
]