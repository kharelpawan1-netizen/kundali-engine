
"""
yogas/rajyoga.py

Structural Parashari Raja Yoga detection.

Supported structural associations:
    1. Kendra lord + Trikona lord conjunction
    2. Kendra lord + Trikona lord mutual Parashari aspect
    3. Kendra lord + Trikona lord Parivartana (sign exchange)

This module focuses only on structural formation.

It does NOT evaluate:
    - planetary strength
    - dignity
    - combustion
    - retrogression
    - affliction
    - cancellation
    - timing
    - manifestation

Those concerns belong to separate interpretation layers.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Optional, Tuple

from astrology.aspects import has_aspect
from astrology.relationships import SIGN_LORDS

from .base import YogaResult
from .context import planet, planet_house


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

RAJA_YOGA_NAME = "Raja Yoga"

KENDRA_HOUSES: Tuple[int, ...] = (
    1,
    4,
    7,
    10,
)

TRIKONA_HOUSES: Tuple[int, ...] = (
    1,
    5,
    9,
)


# ============================================================
# HOUSE HELPERS
# ============================================================

def is_kendra_house(
    house: int,
) -> bool:
    """Return True if the house is a Kendra."""

    return house in KENDRA_HOUSES


def is_trikona_house(
    house: int,
) -> bool:
    """Return True if the house is a Trikona."""

    return house in TRIKONA_HOUSES


def is_kendra_or_trikona(
    house: int,
) -> bool:
    """Return True if the house belongs to Kendra or Trikona."""

    return (
        is_kendra_house(house)
        or is_trikona_house(house)
    )


# ============================================================
# HOUSE LORD HELPERS
# ============================================================

def house_lord(
    context: Any,
    house: int,
) -> Optional[str]:
    """
    Return the planetary lord of a house.

    Supported house representations include:
        - dictionary keyed by house number
        - objects exposing a 'lord' attribute

    Returns None if unavailable.
    """

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
# PLANET POSITION HELPERS
# ============================================================

def planet_sign_number(
    context: Any,
    planet_name: str,
) -> Optional[int]:
    """
    Return a planet's normalized zodiac sign number.

    The Planet model exposes sign_number directly.

    Returns None when unavailable.
    """

    value = planet(
        context,
        planet_name,
    )

    if value is None:
        return None

    sign_number = getattr(
        value,
        "sign_number",
        None,
    )

    if sign_number is None:
        return None

    try:
        sign_number = int(sign_number)
    except (
        TypeError,
        ValueError,
    ):
        return None

    if not 1 <= sign_number <= 12:
        return None

    return sign_number


def sign_lord(
    sign_number: int,
) -> Optional[str]:
    """
    Return the classical planetary lord of a zodiac sign.

    Sign numbers:
        1 = Aries
        2 = Taurus
        3 = Gemini
        4 = Cancer
        5 = Leo
        6 = Virgo
        7 = Libra
        8 = Scorpio
        9 = Sagittarius
        10 = Capricorn
        11 = Aquarius
        12 = Pisces
    """

    if not 1 <= sign_number <= 12:
        raise ValueError(
            "sign_number must be between 1 and 12."
        )

    sign_names = (
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
    )

    return SIGN_LORDS.get(
        sign_names[sign_number - 1]
    )


# ============================================================
# CONJUNCTION
# ============================================================

def planets_conjunct(
    context: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Return True when two planets occupy the same house.

    This is a whole-sign structural conjunction.
    """

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


# ============================================================
# MUTUAL PARASHARI ASPECT
# ============================================================

def planets_mutually_aspect(
    context: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Return True when two planets mutually aspect each other
    under the configured Parashari Drishti rules.
    """

    if planet_a == planet_b:
        return False

    sign_a = planet_sign_number(
        context,
        planet_a,
    )

    sign_b = planet_sign_number(
        context,
        planet_b,
    )

    if (
        sign_a is None
        or sign_b is None
    ):
        return False

    if not has_aspect(
        planet_a,
        sign_a,
        sign_b,
    ):
        return False

    return has_aspect(
        planet_b,
        sign_b,
        sign_a,
    )


# ============================================================
# PARIVARTANA / SIGN EXCHANGE
# ============================================================

def planets_exchange_signs(
    context: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Return True when two planets are in Parivartana.

    A genuine sign exchange requires:

        Planet A occupies a sign owned by Planet B
        AND
        Planet B occupies a sign owned by Planet A

    Example:

        Mars owns Aries.
        Venus owns Taurus.

        Mars in Taurus
        Venus in Aries

    Therefore Mars and Venus exchange signs.

    This function checks only structural sign exchange.
    It does not evaluate dignity, strength, cancellation,
    or whether the exchange is auspicious.
    """

    if planet_a == planet_b:
        return False

    sign_a = planet_sign_number(
        context,
        planet_a,
    )

    sign_b = planet_sign_number(
        context,
        planet_b,
    )

    if (
        sign_a is None
        or sign_b is None
    ):
        return False

    lord_of_a_sign = sign_lord(
        sign_a
    )

    lord_of_b_sign = sign_lord(
        sign_b
    )

    if (
        lord_of_a_sign != planet_b
        or lord_of_b_sign != planet_a
    ):
        return False

    return True


# ============================================================
# LORD ASSOCIATION
# ============================================================

def lords_have_association(
    context: Any,
    lord_a: str,
    lord_b: str,
) -> bool:
    """
    Determine whether two house lords are structurally
    associated.

    Supported:
        - conjunction
        - mutual Parashari aspect
        - Parivartana
    """

    if not lord_a or not lord_b:
        return False

    if lord_a == lord_b:
        return False

    if planets_conjunct(
        context,
        lord_a,
        lord_b,
    ):
        return True

    if planets_mutually_aspect(
        context,
        lord_a,
        lord_b,
    ):
        return True

    return planets_exchange_signs(
        context,
        lord_a,
        lord_b,
    )


def lord_association_type(
    context: Any,
    lord_a: str,
    lord_b: str,
) -> Optional[str]:
    """
    Return the structural association type.

    Returns:
        "conjunction"
        "mutual_aspect"
        "parivartana"
        None

    Priority:
        conjunction
        mutual_aspect
        parivartana
    """

    if not lord_a or not lord_b:
        return None

    if lord_a == lord_b:
        return None

    if planets_conjunct(
        context,
        lord_a,
        lord_b,
    ):
        return "conjunction"

    if planets_mutually_aspect(
        context,
        lord_a,
        lord_b,
    ):
        return "mutual_aspect"

    if planets_exchange_signs(
        context,
        lord_a,
        lord_b,
    ):
        return "parivartana"

    return None


# ============================================================
# KENDRA + TRIKONA ASSOCIATIONS
# ============================================================

def find_kendra_trikona_associations(
    context: Any,
) -> list[dict[str, Any]]:
    """
    Find structural associations between Kendra and Trikona lords.

    Supported:
        - conjunction
        - mutual Parashari aspect
        - Parivartana

    The 1st house is intentionally allowed to participate in both
    groups because Lagna is both a Kendra and a Trikona.
    """

    associations: list[dict[str, Any]] = []

    for kendra in KENDRA_HOUSES:

        kendra_lord = house_lord(
            context,
            kendra,
        )

        if kendra_lord is None:
            continue

        for trikona in TRIKONA_HOUSES:

            trikona_lord = house_lord(
                context,
                trikona,
            )

            if trikona_lord is None:
                continue

            if kendra_lord == trikona_lord:
                continue

            association = lord_association_type(
                context,
                kendra_lord,
                trikona_lord,
            )

            if association is None:
                continue

            associations.append(
                {
                    "kendra_house": kendra,
                    "kendra_lord": kendra_lord,
                    "trikona_house": trikona,
                    "trikona_lord": trikona_lord,
                    "association": association,
                }
            )

    return associations


# ============================================================
# RESULT CREATION
# ============================================================

def _make_raja_yoga_result(
    context: Any,
    associations: list[dict[str, Any]],
) -> YogaResult:
    """
    Build a structured YogaResult.
    """

    involved_planets: list[str] = []
    involved_houses: list[int] = []
    evidence: list[str] = []
    conditions_met: list[str] = []

    for association in associations:

        kendra_lord = association[
            "kendra_lord"
        ]

        trikona_lord = association[
            "trikona_lord"
        ]

        kendra_house = association[
            "kendra_house"
        ]

        trikona_house = association[
            "trikona_house"
        ]

        association_type = association[
            "association"
        ]

        if kendra_lord not in involved_planets:
            involved_planets.append(
                kendra_lord
            )

        if trikona_lord not in involved_planets:
            involved_planets.append(
                trikona_lord
            )

        if kendra_house not in involved_houses:
            involved_houses.append(
                kendra_house
            )

        if trikona_house not in involved_houses:
            involved_houses.append(
                trikona_house
            )

        if association_type == "conjunction":

            evidence.append(
                (
                    f"{kendra_lord}, lord of house "
                    f"{kendra_house}, is conjunct "
                    f"{trikona_lord}, lord of house "
                    f"{trikona_house}."
                )
            )

            conditions_met.append(
                (
                    f"Kendra lord of house "
                    f"{kendra_house} associated with "
                    f"Trikona lord of house "
                    f"{trikona_house} by conjunction."
                )
            )

        elif association_type == "mutual_aspect":

            evidence.append(
                (
                    f"{kendra_lord}, lord of house "
                    f"{kendra_house}, mutually aspects "
                    f"{trikona_lord}, lord of house "
                    f"{trikona_house} under the "
                    f"configured Parashari Drishti rules."
                )
            )

            conditions_met.append(
                (
                    f"Kendra lord of house "
                    f"{kendra_house} mutually aspects "
                    f"Trikona lord of house "
                    f"{trikona_house}."
                )
            )

        elif association_type == "parivartana":

            kendra_sign = planet_sign_number(
                context,
                kendra_lord,
            )

            trikona_sign = planet_sign_number(
                context,
                trikona_lord,
            )

            evidence.append(
                (
                    f"{kendra_lord}, lord of house "
                    f"{kendra_house}, occupies a sign "
                    f"owned by {trikona_lord}, while "
                    f"{trikona_lord}, lord of house "
                    f"{trikona_house}, occupies a sign "
                    f"owned by {kendra_lord}; "
                    f"the two lords therefore form "
                    f"Parivartana (sign exchange)."
                )
            )

            conditions_met.append(
                (
                    f"Kendra lord of house "
                    f"{kendra_house} exchanges signs "
                    f"with Trikona lord of house "
                    f"{trikona_house}."
                )
            )

            association[
                "kendra_lord_sign_number"
            ] = kendra_sign

            association[
                "trikona_lord_sign_number"
            ] = trikona_sign

    association_types = sorted(
        {
            association["association"]
            for association in associations
        }
    )

    return YogaResult(
        name=RAJA_YOGA_NAME,
        detected=True,
        category="Raja Yoga",
        description=(
            "A structural Raja Yoga is formed through "
            "association of a Kendra lord and a Trikona lord."
        ),
        evidence=evidence,
        involved_planets=involved_planets,
        involved_houses=sorted(
            involved_houses
        ),
        conditions_met=conditions_met,
        metadata={
            "formation": (
                "kendra_trikona_lord_association"
            ),
            "association_types": association_types,
            "associations": associations,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_rajyoga(
    context: Any,
) -> YogaResult:
    """
    Detect structural Raja Yoga.

    Supported structural associations:

        - conjunction
        - mutual Parashari aspect
        - Parivartana

    No strength, dignity, affliction, cancellation, timing,
    or manifestation analysis is performed here.
    """

    associations = (
        find_kendra_trikona_associations(
            context
        )
    )

    if not associations:

        return YogaResult(
            name=RAJA_YOGA_NAME,
            detected=False,
            category="Raja Yoga",
            description=(
                "No qualifying structural Kendra-Trikona "
                "lord association was found."
            ),
            conditions_failed=[
                (
                    "No Kendra lord and Trikona lord "
                    "structural association detected."
                )
            ],
        )

    return _make_raja_yoga_result(
        context,
        associations,
    )


# ============================================================
# YOGA RULE ADAPTER
# ============================================================

class RajaYogaRule:
    """
    YogaRule adapter for YogaAnalyzer.
    """

    name = RAJA_YOGA_NAME
    category = "Raja Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """Evaluate Raja Yoga."""

        return detect_rajyoga(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "RAJA_YOGA_NAME",
    "KENDRA_HOUSES",
    "TRIKONA_HOUSES",
    "is_kendra_house",
    "is_trikona_house",
    "is_kendra_or_trikona",
    "house_lord",
    "planet_sign_number",
    "sign_lord",
    "planets_conjunct",
    "planets_mutually_aspect",
    "planets_exchange_signs",
    "lords_have_association",
    "lord_association_type",
    "find_kendra_trikona_associations",
    "detect_rajyoga",
    "RajaYogaRule",
]