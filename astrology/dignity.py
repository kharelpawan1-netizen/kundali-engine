"""
astrology/dignity.py

Classical Vedic planetary dignity calculations.

Determines whether a planet is:
    - Exalted
    - Debilitated
    - In its own sign
    - In its Moolatrikona sign
    - In a friendly sign
    - In a neutral sign
    - In an enemy sign

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Dict


# ============================================================
# Planetary sign relationships
# ============================================================

EXALTATION_SIGNS: Dict[str, str] = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
}


DEBILITATION_SIGNS: Dict[str, str] = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
}


OWN_SIGNS: Dict[str, tuple] = {
    "Sun": ("Leo",),
    "Moon": ("Cancer",),
    "Mars": ("Aries", "Scorpio"),
    "Mercury": ("Gemini", "Virgo"),
    "Jupiter": ("Sagittarius", "Pisces"),
    "Venus": ("Taurus", "Libra"),
    "Saturn": ("Capricorn", "Aquarius"),
}


MOOLATRIKONA_SIGNS: Dict[str, str] = {
    "Sun": "Leo",
    "Moon": "Taurus",
    "Mars": "Aries",
    "Mercury": "Virgo",
    "Jupiter": "Sagittarius",
    "Venus": "Libra",
    "Saturn": "Aquarius",
}


# Natural planetary friendships.
NATURAL_FRIENDS: Dict[str, tuple] = {
    "Sun": ("Moon", "Mars", "Jupiter"),
    "Moon": ("Sun", "Mercury"),
    "Mars": ("Sun", "Moon", "Jupiter"),
    "Mercury": ("Sun", "Venus"),
    "Jupiter": ("Sun", "Moon", "Mars"),
    "Venus": ("Mercury", "Saturn"),
    "Saturn": ("Mercury", "Venus"),
}


NATURAL_ENEMIES: Dict[str, tuple] = {
    "Sun": ("Venus", "Saturn"),
    "Moon": (),
    "Mars": ("Mercury",),
    "Mercury": ("Moon",),
    "Jupiter": ("Mercury", "Venus"),
    "Venus": ("Sun", "Moon"),
    "Saturn": ("Sun", "Moon", "Mars"),
}


# Sign lords.
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
# Basic dignity
# ============================================================


def get_dignity(planet: str, sign: str) -> str:
    """
    Determine the basic dignity of a planet in a sign.

    Priority:
        Exalted
        Debilitated
        Moolatrikona
        Own Sign
        Friendly Sign
        Enemy Sign
        Neutral Sign
    """

    if planet not in SIGN_LORDS and planet not in EXALTATION_SIGNS:
        raise ValueError(f"Unknown planet: {planet}")

    if sign not in SIGN_LORDS:
        raise ValueError(f"Unknown sign: {sign}")

    if EXALTATION_SIGNS.get(planet) == sign:
        return "Exalted"

    if DEBILITATION_SIGNS.get(planet) == sign:
        return "Debilitated"

    if MOOLATRIKONA_SIGNS.get(planet) == sign:
        return "Moolatrikona"

    if sign in OWN_SIGNS.get(planet, ()):
        return "Own Sign"

    sign_lord = SIGN_LORDS[sign]

    if sign_lord in NATURAL_FRIENDS.get(planet, ()):
        return "Friendly Sign"

    if sign_lord in NATURAL_ENEMIES.get(planet, ()):
        return "Enemy Sign"

    return "Neutral Sign"


def is_exalted(planet: str, sign: str) -> bool:
    """Return True if the planet is exalted."""
    return EXALTATION_SIGNS.get(planet) == sign


def is_debilitated(planet: str, sign: str) -> bool:
    """Return True if the planet is debilitated."""
    return DEBILITATION_SIGNS.get(planet) == sign


def is_own_sign(planet: str, sign: str) -> bool:
    """Return True if the planet is in its own sign."""
    return sign in OWN_SIGNS.get(planet, ())


def is_moolatrikona(planet: str, sign: str) -> bool:
    """Return True if the planet is in its Moolatrikona sign."""
    return MOOLATRIKONA_SIGNS.get(planet) == sign


__all__ = [
    "EXALTATION_SIGNS",
    "DEBILITATION_SIGNS",
    "OWN_SIGNS",
    "MOOLATRIKONA_SIGNS",
    "NATURAL_FRIENDS",
    "NATURAL_ENEMIES",
    "SIGN_LORDS",
    "get_dignity",
    "is_exalted",
    "is_debilitated",
    "is_own_sign",
    "is_moolatrikona",
]