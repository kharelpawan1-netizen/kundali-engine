"""
astrology/relationships.py

Classical Vedic planetary relationship calculations.

Provides:
    - Natural planetary friendship
    - Natural planetary enmity
    - Natural neutrality
    - Temporary friendship/enmity
    - Panchadha Maitri (five-fold relationship)
    - Compound relationship

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Dict, Tuple


# ============================================================
# Natural planetary relationships
# ============================================================

NATURAL_FRIENDS: Dict[str, Tuple[str, ...]] = {
    "Sun": ("Moon", "Mars", "Jupiter"),
    "Moon": ("Sun", "Mercury"),
    "Mars": ("Sun", "Moon", "Jupiter"),
    "Mercury": ("Sun", "Venus"),
    "Jupiter": ("Sun", "Moon", "Mars"),
    "Venus": ("Mercury", "Saturn"),
    "Saturn": ("Mercury", "Venus"),
}


NATURAL_ENEMIES: Dict[str, Tuple[str, ...]] = {
    "Sun": ("Venus", "Saturn"),
    "Moon": (),
    "Mars": ("Mercury",),
    "Mercury": ("Moon",),
    "Jupiter": ("Mercury", "Venus"),
    "Venus": ("Sun", "Moon"),
    "Saturn": ("Sun", "Moon", "Mars"),
}


# ============================================================
# Planetary sign ownership
# ============================================================

SIGN_LORDS: Dict[str, str] = {
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


# ============================================================
# Planet validation
# ============================================================

PLANETS = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
)


def _validate_planet(planet: str) -> None:
    """Validate a classical seven-planet relationship participant."""

    if planet not in PLANETS:
        raise ValueError(
            f"Unknown planet: {planet}. "
            f"Supported planets: {', '.join(PLANETS)}"
        )


def _validate_sign(sign: str) -> None:
    """Validate a zodiac sign."""

    if sign not in SIGN_LORDS:
        raise ValueError(f"Unknown zodiac sign: {sign}")


# ============================================================
# Natural relationship
# ============================================================


def natural_relationship(
    planet_a: str,
    planet_b: str,
) -> str:
    """
    Determine the natural relationship between two planets.

    Returns:
        "Friend"
        "Enemy"
        "Neutral"

    A planet compared with itself is considered neutral for
    relationship calculations.
    """

    _validate_planet(planet_a)
    _validate_planet(planet_b)

    if planet_a == planet_b:
        return "Neutral"

    if planet_b in NATURAL_FRIENDS.get(planet_a, ()):
        return "Friend"

    if planet_b in NATURAL_ENEMIES.get(planet_a, ()):
        return "Enemy"

    return "Neutral"


# ============================================================
# Convenience helpers
# ============================================================


def are_natural_friends(
    planet_a: str,
    planet_b: str,
) -> bool:
    """Return True if planet_b is a natural friend of planet_a."""

    return natural_relationship(planet_a, planet_b) == "Friend"


def are_natural_enemies(
    planet_a: str,
    planet_b: str,
) -> bool:
    """Return True if planet_b is a natural enemy of planet_a."""

    return natural_relationship(planet_a, planet_b) == "Enemy"


def are_natural_neutral(
    planet_a: str,
    planet_b: str,
) -> bool:
    """Return True if the relationship is naturally neutral."""

    return natural_relationship(planet_a, planet_b) == "Neutral"


# ============================================================
# Temporary relationship
# ============================================================


def temporary_relationship(
    planet_a_sign_number: int,
    planet_b_sign_number: int,
) -> str:
    """
    Determine Tatkalika (temporary) relationship.

    The relationship is based on the relative house/sign
    positions of two planets.

    For the classical temporary relationship used here:

        2nd, 3rd, 4th, 10th, 11th and 12th
        positions from a planet are temporary friends.

        1st, 5th, 6th, 7th, 8th and 9th
        positions are temporary enemies.

    Parameters:
        planet_a_sign_number:
            Sign number of planet A, 1-12.

        planet_b_sign_number:
            Sign number of planet B, 1-12.
    """

    if not 1 <= planet_a_sign_number <= 12:
        raise ValueError("planet_a_sign_number must be between 1 and 12")

    if not 1 <= planet_b_sign_number <= 12:
        raise ValueError("planet_b_sign_number must be between 1 and 12")

    distance = (
        (planet_b_sign_number - planet_a_sign_number) % 12
    ) + 1

    if distance in (2, 3, 4, 10, 11, 12):
        return "Friend"

    return "Enemy"


# ============================================================
# Panchadha Maitri
# ============================================================


def panchadha_relationship(
    planet_a: str,
    planet_b: str,
    planet_a_sign_number: int,
    planet_b_sign_number: int,
) -> str:
    """
    Determine Panchadha Maitri (five-fold relationship).

    Combines:

        1. Natural relationship
        2. Temporary relationship

    Classical combination:

        Natural Friend + Temporary Friend
            -> Great Friend

        Natural Friend + Temporary Enemy
            -> Neutral

        Natural Neutral + Temporary Friend
            -> Friend

        Natural Neutral + Temporary Enemy
            -> Enemy

        Natural Enemy + Temporary Friend
            -> Neutral

        Natural Enemy + Temporary Enemy
            -> Great Enemy
    """

    natural = natural_relationship(planet_a, planet_b)

    temporary = temporary_relationship(
        planet_a_sign_number,
        planet_b_sign_number,
    )

    if natural == "Friend":
        if temporary == "Friend":
            return "Great Friend"
        return "Neutral"

    if natural == "Neutral":
        if temporary == "Friend":
            return "Friend"
        return "Enemy"

    # Natural enemy
    if temporary == "Friend":
        return "Neutral"

    return "Great Enemy"


# ============================================================
# Compound relationship alias
# ============================================================


def compound_relationship(
    planet_a: str,
    planet_b: str,
    planet_a_sign_number: int,
    planet_b_sign_number: int,
) -> str:
    """
    Alias for Panchadha Maitri.

    Kept as a separate public function because later
    interpretation modules may use the term
    "compound relationship".
    """

    return panchadha_relationship(
        planet_a,
        planet_b,
        planet_a_sign_number,
        planet_b_sign_number,
    )


# ============================================================
# Relationship matrix
# ============================================================


def natural_relationship_matrix() -> Dict[str, Dict[str, str]]:
    """
    Return the complete natural relationship matrix.

    Returns:
        {
            "Sun": {
                "Moon": "Friend",
                ...
            },
            ...
        }
    """

    return {
        planet_a: {
            planet_b: natural_relationship(
                planet_a,
                planet_b,
            )
            for planet_b in PLANETS
        }
        for planet_a in PLANETS
    }


__all__ = [
    "NATURAL_FRIENDS",
    "NATURAL_ENEMIES",
    "SIGN_LORDS",
    "PLANETS",
    "natural_relationship",
    "are_natural_friends",
    "are_natural_enemies",
    "are_natural_neutral",
    "temporary_relationship",
    "panchadha_relationship",
    "compound_relationship",
    "natural_relationship_matrix",
]