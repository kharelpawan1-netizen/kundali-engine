"""
knowledge/signs.py

Permanent BPHS zodiac-sign (Rashi) knowledge database.

This module contains immutable knowledge for the twelve Rashis.
No chart calculations are performed here.

The Sign enum remains defined in models/sign.py.
This module only provides interpretive knowledge associated
with each Sign.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from models.sign import Sign


@dataclass(frozen=True)
class SignFacts:
    """
    Immutable knowledge describing one zodiac sign (Rashi).
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    sign: Sign
    sanskrit_name: str

    # ---------------------------------------------------------
    # Fundamental nature
    # ---------------------------------------------------------

    element: str
    modality: str
    gender: str
    guna: str

    # ---------------------------------------------------------
    # Lordship
    # ---------------------------------------------------------

    lord: str

    # ---------------------------------------------------------
    # Direction
    # ---------------------------------------------------------

    direction: str

    # ---------------------------------------------------------
    # Body and temperament
    # ---------------------------------------------------------

    body_part: str
    temperament: str

    # ---------------------------------------------------------
    # Sign characteristics
    # ---------------------------------------------------------

    keywords: Tuple[str, ...]

    # ---------------------------------------------------------
    # Natural significations
    # ---------------------------------------------------------

    significations: Tuple[str, ...]


# =============================================================
# TWELVE RASHIS
# =============================================================

SIGNS: Dict[Sign, SignFacts] = {

    # =========================================================
    # ARIES
    # =========================================================

    Sign.ARIES: SignFacts(
        sign=Sign.ARIES,
        sanskrit_name="Mesha",
        element="Fire",
        modality="Movable",
        gender="Male",
        guna="Rajas",
        lord="Mars",
        direction="East",
        body_part="Head",
        temperament="Active",
        keywords=(
            "initiative",
            "courage",
            "independence",
            "action",
            "competition",
            "leadership",
            "assertiveness",
            "energy",
        ),
        significations=(
            "beginnings",
            "initiative",
            "courage",
            "physical activity",
            "competition",
            "leadership",
            "independence",
            "assertion",
        ),
    ),

    # =========================================================
    # TAURUS
    # =========================================================

    Sign.TAURUS: SignFacts(
        sign=Sign.TAURUS,
        sanskrit_name="Vrishabha",
        element="Earth",
        modality="Fixed",
        gender="Female",
        guna="Rajas",
        lord="Venus",
        direction="South",
        body_part="Face",
        temperament="Steady",
        keywords=(
            "stability",
            "wealth",
            "resources",
            "comfort",
            "beauty",
            "patience",
            "possession",
            "sensuality",
        ),
        significations=(
            "wealth",
            "possessions",
            "resources",
            "food",
            "family values",
            "comfort",
            "beauty",
            "stability",
        ),
    ),

    # =========================================================
    # GEMINI
    # =========================================================

    Sign.GEMINI: SignFacts(
        sign=Sign.GEMINI,
        sanskrit_name="Mithuna",
        element="Air",
        modality="Dual",
        gender="Male",
        guna="Rajas",
        lord="Mercury",
        direction="West",
        body_part="Arms",
        temperament="Adaptive",
        keywords=(
            "communication",
            "intelligence",
            "learning",
            "curiosity",
            "writing",
            "speech",
            "adaptability",
            "analysis",
        ),
        significations=(
            "communication",
            "education",
            "writing",
            "speech",
            "commerce",
            "intellect",
            "siblings",
            "information",
        ),
    ),

    # =========================================================
    # CANCER
    # =========================================================

    Sign.CANCER: SignFacts(
        sign=Sign.CANCER,
        sanskrit_name="Karka",
        element="Water",
        modality="Movable",
        gender="Female",
        guna="Sattva",
        lord="Moon",
        direction="North",
        body_part="Chest",
        temperament="Sensitive",
        keywords=(
            "emotion",
            "mother",
            "home",
            "nurturing",
            "care",
            "memory",
            "security",
            "family",
        ),
        significations=(
            "mother",
            "home",
            "family",
            "emotions",
            "nourishment",
            "property",
            "domestic life",
            "mental peace",
        ),
    ),

    # =========================================================
    # LEO
    # =========================================================

    Sign.LEO: SignFacts(
        sign=Sign.LEO,
        sanskrit_name="Simha",
        element="Fire",
        modality="Fixed",
        gender="Male",
        guna="Sattva",
        lord="Sun",
        direction="East",
        body_part="Heart",
        temperament="Authoritative",
        keywords=(
            "authority",
            "leadership",
            "confidence",
            "fame",
            "power",
            "honor",
            "creativity",
            "royalty",
        ),
        significations=(
            "authority",
            "leadership",
            "government",
            "fame",
            "recognition",
            "children",
            "creativity",
            "status",
        ),
    ),

    # =========================================================
    # VIRGO
    # =========================================================

    Sign.VIRGO: SignFacts(
        sign=Sign.VIRGO,
        sanskrit_name="Kanya",
        element="Earth",
        modality="Dual",
        gender="Female",
        guna="Tamas",
        lord="Mercury",
        direction="South",
        body_part="Abdomen",
        temperament="Analytical",
        keywords=(
            "analysis",
            "service",
            "discipline",
            "detail",
            "logic",
            "health",
            "organization",
            "precision",
        ),
        significations=(
            "service",
            "analysis",
            "health",
            "routine",
            "work",
            "calculation",
            "discipline",
            "organization",
        ),
    ),

    # =========================================================
    # LIBRA
    # =========================================================

    Sign.LIBRA: SignFacts(
        sign=Sign.LIBRA,
        sanskrit_name="Tula",
        element="Air",
        modality="Movable",
        gender="Male",
        guna="Rajas",
        lord="Venus",
        direction="West",
        body_part="Kidneys",
        temperament="Balanced",
        keywords=(
            "balance",
            "relationships",
            "marriage",
            "justice",
            "harmony",
            "beauty",
            "partnership",
            "negotiation",
        ),
        significations=(
            "marriage",
            "partnership",
            "relationships",
            "trade",
            "contracts",
            "justice",
            "balance",
            "social interaction",
        ),
    ),

    # =========================================================
    # SCORPIO
    # =========================================================

    Sign.SCORPIO: SignFacts(
        sign=Sign.SCORPIO,
        sanskrit_name="Vrishchika",
        element="Water",
        modality="Fixed",
        gender="Female",
        guna="Tamas",
        lord="Mars",
        direction="North",
        body_part="Reproductive Organs",
        temperament="Intense",
        keywords=(
            "transformation",
            "depth",
            "secrecy",
            "research",
            "occult",
            "determination",
            "intensity",
            "investigation",
        ),
        significations=(
            "transformation",
            "secrets",
            "research",
            "occult",
            "hidden matters",
            "inheritance",
            "crisis",
            "deep investigation",
        ),
    ),

    # =========================================================
    # SAGITTARIUS
    # =========================================================

    Sign.SAGITTARIUS: SignFacts(
        sign=Sign.SAGITTARIUS,
        sanskrit_name="Dhanu",
        element="Fire",
        modality="Dual",
        gender="Male",
        guna="Sattva",
        lord="Jupiter",
        direction="East",
        body_part="Thighs",
        temperament="Expansive",
        keywords=(
            "wisdom",
            "dharma",
            "higher_learning",
            "philosophy",
            "religion",
            "travel",
            "fortune",
            "expansion",
        ),
        significations=(
            "dharma",
            "higher education",
            "religion",
            "philosophy",
            "long journeys",
            "teachers",
            "wisdom",
            "fortune",
        ),
    ),

    # =========================================================
    # CAPRICORN
    # =========================================================

    Sign.CAPRICORN: SignFacts(
        sign=Sign.CAPRICORN,
        sanskrit_name="Makara",
        element="Earth",
        modality="Movable",
        gender="Female",
        guna="Tamas",
        lord="Saturn",
        direction="South",
        body_part="Knees",
        temperament="Disciplined",
        keywords=(
            "discipline",
            "career",
            "responsibility",
            "ambition",
            "hard work",
            "authority",
            "structure",
            "persistence",
        ),
        significations=(
            "career",
            "profession",
            "responsibility",
            "authority",
            "organization",
            "hard work",
            "status",
            "material achievement",
        ),
    ),

    # =========================================================
    # AQUARIUS
    # =========================================================

    Sign.AQUARIUS: SignFacts(
        sign=Sign.AQUARIUS,
        sanskrit_name="Kumbha",
        element="Air",
        modality="Fixed",
        gender="Male",
        guna="Tamas",
        lord="Saturn",
        direction="West",
        body_part="Calves",
        temperament="Independent",
        keywords=(
            "innovation",
            "society",
            "humanitarianism",
            "technology",
            "networks",
            "independence",
            "reform",
            "collective",
        ),
        significations=(
            "society",
            "large organizations",
            "networks",
            "innovation",
            "technology",
            "social causes",
            "mass influence",
            "collective interests",
        ),
    ),

    # =========================================================
    # PISCES
    # =========================================================

    Sign.PISCES: SignFacts(
        sign=Sign.PISCES,
        sanskrit_name="Meena",
        element="Water",
        modality="Dual",
        gender="Female",
        guna="Sattva",
        lord="Jupiter",
        direction="North",
        body_part="Feet",
        temperament="Compassionate",
        keywords=(
            "spirituality",
            "compassion",
            "intuition",
            "imagination",
            "devotion",
            "moksha",
            "sensitivity",
            "transcendence",
        ),
        significations=(
            "spirituality",
            "moksha",
            "devotion",
            "foreign lands",
            "charity",
            "dreams",
            "intuition",
            "compassion",
        ),
    ),
}


def get_sign(sign: Sign) -> SignFacts:
    """
    Return immutable knowledge for a Rashi.
    """

    return SIGNS[sign]


def all_signs() -> Tuple[SignFacts, ...]:
    """
    Return all twelve Rashi knowledge objects.
    """

    return tuple(SIGNS.values())


__all__ = [
    "SignFacts",
    "SIGNS",
    "get_sign",
    "all_signs",
]