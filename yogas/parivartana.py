"""
yogas/parivartana.py

Structural Parashari Parivartana Yoga detection.

Parivartana Yoga is formed when two planets occupy each
other's signs.

This module detects only structural sign exchange and
classifies the exchange into:

    - Maha Parivartana
    - Khala Parivartana
    - Dainya Parivartana

Classification precedence:

    1. Dainya:
       At least one involved house is 6, 8, or 12.

    2. Khala:
       No Dusthana is involved, but the 3rd house is involved.

    3. Maha:
       Neither Dainya nor Khala applies and both involved
       houses belong to the auspicious set:

           1, 2, 4, 5, 7, 9, 10, 11

This module does NOT evaluate:

    - planetary strength
    - dignity
    - exaltation/debilitation
    - combustion
    - retrogression
    - Shadbala
    - aspects
    - conjunctions
    - cancellation
    - Viparita Raja Yoga
    - dasha
    - transits
    - manifestation

Those belong to separate interpretation layers.

Rahu and Ketu are not treated as sign-exchange participants
because this detector requires planets with defined sign lordship.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from .base import YogaResult


# ============================================================
# PUBLIC CONSTANTS
# ============================================================

PARIVARTANA_YOGA_NAME = "Parivartana Yoga"

MAHA_PARIVARTANA_NAME = "Maha Parivartana Yoga"
KHALA_PARIVARTANA_NAME = "Khala Parivartana Yoga"
DAINYA_PARIVARTANA_NAME = "Dainya Parivartana Yoga"

# Seven classical sign-owning planets.
SIGN_OWNING_PLANETS: Tuple[str, ...] = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
)

# Houses classified as Dusthana / Trika.
DUSTHANA_HOUSES: Tuple[int, ...] = (
    6,
    8,
    12,
)

# 3rd house is used for Khala classification.
KHALA_HOUSES: Tuple[int, ...] = (
    3,
)

# Houses traditionally used for the Maha category in the
# three-way Parivartana classification.
MAHA_HOUSES: Tuple[int, ...] = (
    1,
    2,
    4,
    5,
    7,
    9,
    10,
    11,
)


# ============================================================
# BASIC HELPERS
# ============================================================

def _validate_house(house: int) -> None:
    """Validate a house number."""

    if not isinstance(house, int):
        raise TypeError(
            "house must be an integer."
        )

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )


def _get_planets(context: Any) -> Any:
    """Return the planet collection from the context."""

    planets = getattr(
        context,
        "planets",
        None,
    )

    if planets is None:
        return None

    return planets


def _get_planet(
    context: Any,
    planet_name: str,
) -> Optional[Any]:
    """Return a named planet from the context."""

    planets = _get_planets(
        context
    )

    if planets is None:
        return None

    if hasattr(planets, "get"):
        return planets.get(
            planet_name
        )

    return None


def _planet_house(
    context: Any,
    planet_name: str,
) -> Optional[int]:
    """Return the house occupied by a planet."""

    planet = _get_planet(
        context,
        planet_name,
    )

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
        house = int(house)
    except (TypeError, ValueError):
        return None

    if not 1 <= house <= 12:
        return None

    return house


# ============================================================
# SIGN NORMALIZATION
# ============================================================

_SIGN_NAME_TO_NUMBER: Dict[str, int] = {
    "aries": 1,
    "mesha": 1,

    "taurus": 2,
    "vrishabha": 2,
    "vrishabha": 2,

    "gemini": 3,
    "mithuna": 3,

    "cancer": 4,
    "karka": 4,

    "leo": 5,
    "simha": 5,

    "virgo": 6,
    "kanya": 6,

    "libra": 7,
    "tula": 7,

    "scorpio": 8,
    "vrischika": 8,
    "vrishchika": 8,

    "sagittarius": 9,
    "dhanu": 9,
    "dhanus": 9,

    "capricorn": 10,
    "makara": 10,

    "aquarius": 11,
    "kumbha": 11,

    "pisces": 12,
    "meena": 12,
}


def normalize_sign(
    sign: Any,
) -> Optional[int]:
    """
    Normalize a sign representation to 1–12.

    Supported representations include:

        1..12
        "Aries"
        "aries"
        "Mesha"
        etc.

    Returns None when the value cannot be interpreted.
    """

    if sign is None:
        return None

    if isinstance(sign, bool):
        return None

    if isinstance(sign, int):
        if 1 <= sign <= 12:
            return sign

        return None

    if isinstance(sign, float):
        if sign.is_integer() and 1 <= int(sign) <= 12:
            return int(sign)

        return None

    value = str(sign).strip().lower()

    if not value:
        return None

    if value.isdigit():
        number = int(value)

        if 1 <= number <= 12:
            return number

    return _SIGN_NAME_TO_NUMBER.get(
        value
    )


def _planet_sign(
    context: Any,
    planet_name: str,
) -> Optional[int]:
    """
    Return the normalized sign occupied by a planet.

    The function supports common model representations:

        planet.sign
        planet.sign_number
        planet.rashi
        planet.rashi_number

    A sign name or sign number is accepted.
    """

    planet = _get_planet(
        context,
        planet_name,
    )

    if planet is None:
        return None

    for attribute in (
        "sign",
        "sign_number",
        "rashi",
        "rashi_number",
    ):
        if hasattr(
            planet,
            attribute,
        ):
            value = getattr(
                planet,
                attribute,
            )

            normalized = normalize_sign(
                value
            )

            if normalized is not None:
                return normalized

    return None


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

        context.houses[house].lord

    Both integer and string dictionary keys are supported.
    """

    _validate_house(
        house
    )

    houses = getattr(
        context,
        "houses",
        None,
    )

    if houses is None:
        return None

    house_object = None

    if hasattr(
        houses,
        "get",
    ):
        house_object = houses.get(
            house
        )

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

    lord = str(
        lord
    ).strip()

    if not lord:
        return None

    return lord


# ============================================================
# HOUSE CLASSIFICATION
# ============================================================

def is_dusthana_house(
    house: int,
) -> bool:
    """Return True when house is 6, 8, or 12."""

    _validate_house(
        house
    )

    return house in DUSTHANA_HOUSES


def is_khala_house(
    house: int,
) -> bool:
    """Return True when house is the 3rd."""

    _validate_house(
        house
    )

    return house in KHALA_HOUSES


def is_maha_house(
    house: int,
) -> bool:
    """Return True when house belongs to the Maha set."""

    _validate_house(
        house
    )

    return house in MAHA_HOUSES


# ============================================================
# SIGN EXCHANGE
# ============================================================

def planets_exchange_signs(
    context: Any,
    planet_a: str,
    planet_b: str,
) -> bool:
    """
    Return True when two planets occupy each other's signs.

    A genuine exchange requires:

        sign(planet_a) = sign ruled by planet_b
        sign(planet_b) = sign ruled by planet_a

    The implementation obtains sign ownership through the
    chart's house-lord structure.

    If either planet or either sign is unavailable, False
    is returned.
    """

    if not planet_a or not planet_b:
        return False

    if planet_a == planet_b:
        return False

    sign_a = _planet_sign(
        context,
        planet_a,
    )

    sign_b = _planet_sign(
        context,
        planet_b,
    )

    if (
        sign_a is None
        or sign_b is None
    ):
        return False

    # Determine which house contains each planet's sign.
    #
    # In a whole-sign Parashari chart, the lord of the house
    # containing a planet's sign is the sign lord of that sign.
    houses = getattr(
        context,
        "houses",
        None,
    )

    if houses is None:
        return False

    lord_of_sign_a = None
    lord_of_sign_b = None

    house_a = houses.get(
        sign_a
    ) if hasattr(
        houses,
        "get",
    ) else None

    house_b = houses.get(
        sign_b
    ) if hasattr(
        houses,
        "get",
    ) else None

    if house_a is None and hasattr(
        houses,
        "get",
    ):
        house_a = houses.get(
            str(sign_a)
        )

    if house_b is None and hasattr(
        houses,
        "get",
    ):
        house_b = houses.get(
            str(sign_b)
        )

    if house_a is not None:
        lord_of_sign_a = getattr(
            house_a,
            "lord",
            None,
        )

    if house_b is not None:
        lord_of_sign_b = getattr(
            house_b,
            "lord",
            None,
        )

    if (
        lord_of_sign_a is None
        or lord_of_sign_b is None
    ):
        return False

    return (
        str(lord_of_sign_a).strip()
        == planet_a
        and
        str(lord_of_sign_b).strip()
        == planet_b
    )


# ============================================================
# DIRECT HOUSE-LORD EXCHANGE
# ============================================================

def house_lords_exchange(
    context: Any,
    house_a: int,
    house_b: int,
) -> bool:
    """
    Return True when the lords of two houses exchange signs.

    Example:

        Lord of house 2 occupies house 11.
        Lord of house 11 occupies house 2.

    In a whole-sign chart this is a direct Parivartana.
    """

    _validate_house(
        house_a
    )

    _validate_house(
        house_b
    )

    if house_a == house_b:
        return False

    lord_a = house_lord(
        context,
        house_a,
    )

    lord_b = house_lord(
        context,
        house_b,
    )

    if (
        lord_a is None
        or lord_b is None
    ):
        return False

    if lord_a == lord_b:
        return False

    occupied_house_a = _planet_house(
        context,
        lord_a,
    )

    occupied_house_b = _planet_house(
        context,
        lord_b,
    )

    if (
        occupied_house_a is None
        or occupied_house_b is None
    ):
        return False

    return (
        occupied_house_a == house_b
        and
        occupied_house_b == house_a
    )


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_parivartana(
    house_a: int,
    house_b: int,
) -> Optional[str]:
    """
    Classify an exchange according to the houses involved.

    Precedence:

        Dainya > Khala > Maha

    Returns None when the pair does not belong to the
    supported three-way classification.
    """

    _validate_house(
        house_a
    )

    _validate_house(
        house_b
    )

    houses = {
        house_a,
        house_b,
    }

    if houses & set(
        DUSTHANA_HOUSES
    ):
        return DAINYA_PARIVARTANA_NAME

    if houses & set(
        KHALA_HOUSES
    ):
        return KHALA_PARIVARTANA_NAME

    if (
        house_a in MAHA_HOUSES
        and house_b in MAHA_HOUSES
    ):
        return MAHA_PARIVARTANA_NAME

    return None


# ============================================================
# FIND EXCHANGES
# ============================================================

def find_parivartana_exchanges(
    context: Any,
) -> List[Dict[str, Any]]:
    """
    Find all supported house-lord sign exchanges.

    Each finding contains:

        house_a
        house_b
        lord_a
        lord_b
        occupied_house_a
        occupied_house_b
        classification
        association
    """

    findings: List[Dict[str, Any]] = []

    for house_a in range(
        1,
        13,
    ):
        lord_a = house_lord(
            context,
            house_a,
        )

        if lord_a is None:
            continue

        occupied_house_a = _planet_house(
            context,
            lord_a,
        )

        if occupied_house_a is None:
            continue

        house_b = occupied_house_a

        if house_b == house_a:
            continue

        if house_b < 1 or house_b > 12:
            continue

        if house_a > house_b:
            continue

        lord_b = house_lord(
            context,
            house_b,
        )

        if lord_b is None:
            continue

        occupied_house_b = _planet_house(
            context,
            lord_b,
        )

        if occupied_house_b != house_a:
            continue

        classification = classify_parivartana(
            house_a,
            house_b,
        )

        if classification is None:
            continue

        findings.append(
            {
                "house_a": house_a,
                "house_b": house_b,
                "lord_a": lord_a,
                "lord_b": lord_b,
                "occupied_house_a": occupied_house_a,
                "occupied_house_b": occupied_house_b,
                "classification": classification,
                "association": "mutual_sign_exchange",
            }
        )

    return findings


# ============================================================
# RESULT CREATION
# ============================================================

def _make_result(
    finding: Dict[str, Any],
) -> YogaResult:
    """Create a YogaResult from one exchange finding."""

    classification = finding[
        "classification"
    ]

    house_a = finding[
        "house_a"
    ]

    house_b = finding[
        "house_b"
    ]

    lord_a = finding[
        "lord_a"
    ]

    lord_b = finding[
        "lord_b"
    ]

    if classification == MAHA_PARIVARTANA_NAME:
        description = (
            "A structural Maha Parivartana Yoga is formed "
            "through mutual sign exchange between lords of "
            "the supported auspicious houses."
        )

    elif classification == KHALA_PARIVARTANA_NAME:
        description = (
            "A structural Khala Parivartana Yoga is formed "
            "through mutual sign exchange involving the "
            "3rd house."
        )

    else:
        description = (
            "A structural Dainya Parivartana Yoga is formed "
            "through mutual sign exchange involving a "
            "Dusthana house."
        )

    evidence = (
        f"{lord_a}, lord of house {house_a}, occupies "
        f"house {house_b}, while {lord_b}, lord of house "
        f"{house_b}, occupies house {house_a}."
    )

    condition = (
        f"Houses {house_a} and {house_b} form a mutual "
        f"sign exchange classified as {classification}."
    )

    return YogaResult(
        name=classification,
        detected=True,
        category="Parivartana Yoga",
        description=description,
        evidence=[
            evidence
        ],
        involved_planets=[
            lord_a,
            lord_b,
        ],
        involved_houses=sorted(
            [
                house_a,
                house_b,
            ]
        ),
        conditions_met=[
            condition
        ],
        metadata={
            "formation": "mutual_sign_exchange",
            "association_type": "sign_exchange",
            "house_a": house_a,
            "house_b": house_b,
            "lord_a": lord_a,
            "lord_b": lord_b,
            "classification": classification,
        },
    )


# ============================================================
# MAIN DETECTOR
# ============================================================

def detect_parivartana(
    context: Any,
) -> YogaResult:
    """
    Detect the first supported Parivartana Yoga.

    Returns a YogaResult in every case.
    """

    findings = find_parivartana_exchanges(
        context
    )

    if not findings:
        return YogaResult(
            name=PARIVARTANA_YOGA_NAME,
            detected=False,
            category="Parivartana Yoga",
            description=(
                "No supported mutual sign exchange was found."
            ),
            conditions_failed=[
                (
                    "No qualifying mutual sign exchange "
                    "between house lords was detected."
                )
            ],
            metadata={
                "formation": "mutual_sign_exchange",
            },
        )

    result = _make_result(
        findings[0]
    )

    result.metadata[
        "all_exchanges"
    ] = findings

    return result


# ============================================================
# RULE ADAPTER
# ============================================================

class ParivartanaYogaRule:
    """YogaRule-compatible adapter for Parivartana Yoga."""

    name = PARIVARTANA_YOGA_NAME
    category = "Parivartana Yoga"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """Evaluate Parivartana Yoga."""

        return detect_parivartana(
            context
        )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "PARIVARTANA_YOGA_NAME",
    "MAHA_PARIVARTANA_NAME",
    "KHALA_PARIVARTANA_NAME",
    "DAINYA_PARIVARTANA_NAME",
    "SIGN_OWNING_PLANETS",
    "DUSTHANA_HOUSES",
    "KHALA_HOUSES",
    "MAHA_HOUSES",
    "normalize_sign",
    "house_lord",
    "is_dusthana_house",
    "is_khala_house",
    "is_maha_house",
    "planets_exchange_signs",
    "house_lords_exchange",
    "classify_parivartana",
    "find_parivartana_exchanges",
    "detect_parivartana",
    "ParivartanaYogaRule",
]