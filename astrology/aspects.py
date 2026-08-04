"""
astrology/aspects.py

Classical Parashari planetary aspect (Drishti) calculations.

Implements:
    - 7th aspect for all classical planets
    - Mars: 4th and 8th special aspects
    - Jupiter: 5th and 9th special aspects
    - Saturn: 3rd and 10th special aspects
    - Configurable Rahu/Ketu aspects

The module works using whole-sign planetary positions.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


# ============================================================
# Planet definitions
# ============================================================

CLASSICAL_PLANETS: Tuple[str, ...] = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
)

NODES: Tuple[str, ...] = (
    "Rahu",
    "Ketu",
)


# ============================================================
# Aspect definitions
# ============================================================

# Every classical graha has the 7th aspect.
DEFAULT_ASPECTS: Dict[str, Tuple[int, ...]] = {
    "Sun": (7,),
    "Moon": (7,),
    "Mars": (7, 4, 8),
    "Mercury": (7,),
    "Jupiter": (7, 5, 9),
    "Venus": (7,),
    "Saturn": (7, 3, 10),
}


# Rahu/Ketu are intentionally configurable because
# traditions differ regarding their special aspects.
#
# Default:
#     Only the 7th aspect is enabled.
#
# This keeps the engine conservative and explicitly Parashari
# rather than silently assuming a particular Nadi or other
# tradition.
DEFAULT_NODE_ASPECTS: Dict[str, Tuple[int, ...]] = {
    "Rahu": (7,),
    "Ketu": (7,),
}


# ============================================================
# Data model
# ============================================================


@dataclass(frozen=True)
class Aspect:
    """
    Represents one planetary aspect.

    Attributes
    ----------
    planet:
        Planet casting the aspect.

    target_sign:
        Zodiac sign number receiving the aspect, 1-12.

    distance:
        House/sign distance from the aspecting planet.

    special:
        True when the aspect is a special aspect rather than
        the universal 7th aspect.
    """

    planet: str
    target_sign: int
    distance: int
    special: bool = False


# ============================================================
# Validation
# ============================================================


def _validate_sign_number(sign_number: int) -> None:
    """Validate a zodiac sign number."""

    if not isinstance(sign_number, int):
        raise TypeError("sign_number must be an integer")

    if not 1 <= sign_number <= 12:
        raise ValueError("sign_number must be between 1 and 12")


def _validate_planet(planet: str) -> None:
    """Validate supported planet name."""

    if planet not in DEFAULT_ASPECTS and planet not in DEFAULT_NODE_ASPECTS:
        raise ValueError(f"Unknown planet: {planet}")


# ============================================================
# Sign-distance calculation
# ============================================================


def sign_distance(
    source_sign: int,
    target_sign: int,
) -> int:
    """
    Return the inclusive zodiacal distance from source to target.

    Examples
    --------
    Aries -> Aries = 1
    Aries -> Taurus = 2
    Aries -> Libra = 7
    Pisces -> Aries = 2
    """

    _validate_sign_number(source_sign)
    _validate_sign_number(target_sign)

    return ((target_sign - source_sign) % 12) + 1


# ============================================================
# Aspect distances
# ============================================================


def aspect_distances(
    planet: str,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> Tuple[int, ...]:
    """
    Return the house/sign distances aspected by a planet.

    Parameters
    ----------
    planet:
        Planet name.

    include_nodes:
        Whether Rahu/Ketu are allowed.

    node_aspects:
        Optional custom Rahu/Ketu aspect configuration.

    Returns
    -------
    tuple
        Aspect distances in ascending order.
    """

    _validate_planet(planet)

    if planet in NODES:

        if not include_nodes:
            return ()

        mapping = (
            node_aspects
            if node_aspects is not None
            else DEFAULT_NODE_ASPECTS
        )

        return tuple(sorted(mapping.get(planet, ())))

    return tuple(sorted(DEFAULT_ASPECTS[planet]))


# ============================================================
# Check whether one planet aspects another
# ============================================================


def has_aspect(
    planet: str,
    source_sign: int,
    target_sign: int,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> bool:
    """
    Determine whether a planet aspects a target sign.

    Parameters
    ----------
    planet:
        Aspecting planet.

    source_sign:
        Sign occupied by the aspecting planet.

    target_sign:
        Target sign.

    Returns
    -------
    bool
        True if the planet aspects the target sign.
    """

    distance = sign_distance(
        source_sign,
        target_sign,
    )

    return distance in aspect_distances(
        planet,
        include_nodes=include_nodes,
        node_aspects=node_aspects,
    )


# ============================================================
# Determine exact aspects
# ============================================================


def get_aspects(
    planet: str,
    source_sign: int,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> List[Aspect]:
    """
    Return every sign receiving an aspect from a planet.

    The source sign itself is not treated as an aspect unless
    explicitly included in the aspect configuration.
    """

    _validate_planet(planet)
    _validate_sign_number(source_sign)

    distances = aspect_distances(
        planet,
        include_nodes=include_nodes,
        node_aspects=node_aspects,
    )

    aspects: List[Aspect] = []

    for distance in distances:

        target_sign = (
            (source_sign - 1 + distance - 1) % 12
        ) + 1

        aspects.append(
            Aspect(
                planet=planet,
                target_sign=target_sign,
                distance=distance,
                special=(distance != 7),
            )
        )

    return aspects


# ============================================================
# Aspect target signs
# ============================================================


def aspect_target_signs(
    planet: str,
    source_sign: int,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> List[int]:
    """
    Return zodiac sign numbers receiving aspects.

    Example:

        Mars in Aries

    gives:

        Libra  -> 7th
        Cancer -> 4th
        Scorpio -> 8th
    """

    return [
        aspect.target_sign
        for aspect in get_aspects(
            planet,
            source_sign,
            include_nodes=include_nodes,
            node_aspects=node_aspects,
        )
    ]


# ============================================================
# Aspect map for a complete chart
# ============================================================


def build_aspect_map(
    planet_signs: Dict[str, int],
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> Dict[str, List[Aspect]]:
    """
    Build an aspect map for all supplied planets.

    Parameters
    ----------
    planet_signs:
        Mapping such as:

            {
                "Sun": 10,
                "Moon": 8,
                "Mars": 12,
            }

    Returns
    -------
    dict
        Mapping of planet name to Aspect objects.
    """

    aspect_map: Dict[str, List[Aspect]] = {}

    for planet, sign_number in planet_signs.items():

        _validate_planet(planet)
        _validate_sign_number(sign_number)

        aspect_map[planet] = get_aspects(
            planet,
            sign_number,
            include_nodes=include_nodes,
            node_aspects=node_aspects,
        )

    return aspect_map


# ============================================================
# Planet-to-planet aspect
# ============================================================


def planet_aspects_planet(
    aspecting_planet: str,
    aspecting_sign: int,
    target_planet: str,
    target_sign: int,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> bool:
    """
    Determine whether one planet aspects another planet.

    This is calculated through their whole-sign positions.
    """

    _validate_planet(aspecting_planet)
    _validate_planet(target_planet)

    _validate_sign_number(aspecting_sign)
    _validate_sign_number(target_sign)

    return has_aspect(
        aspecting_planet,
        aspecting_sign,
        target_sign,
        include_nodes=include_nodes,
        node_aspects=node_aspects,
    )


# ============================================================
# Planet-to-house aspect
# ============================================================


def planet_aspects_house(
    planet: str,
    planet_sign: int,
    house_sign: int,
    include_nodes: bool = True,
    node_aspects: Dict[str, Tuple[int, ...]] | None = None,
) -> bool:
    """
    Determine whether a planet aspects a whole-sign house.

    `house_sign` is the zodiac sign occupied by the house.
    """

    return has_aspect(
        planet,
        planet_sign,
        house_sign,
        include_nodes=include_nodes,
        node_aspects=node_aspects,
    )


# ============================================================
# Special aspect helpers
# ============================================================


def mars_aspects_4th(source_sign: int) -> int:
    """Return the sign receiving Mars' 4th aspect."""

    return _target_for_distance(source_sign, 4)


def mars_aspects_8th(source_sign: int) -> int:
    """Return the sign receiving Mars' 8th aspect."""

    return _target_for_distance(source_sign, 8)


def jupiter_aspects_5th(source_sign: int) -> int:
    """Return the sign receiving Jupiter's 5th aspect."""

    return _target_for_distance(source_sign, 5)


def jupiter_aspects_9th(source_sign: int) -> int:
    """Return the sign receiving Jupiter's 9th aspect."""

    return _target_for_distance(source_sign, 9)


def saturn_aspects_3rd(source_sign: int) -> int:
    """Return the sign receiving Saturn's 3rd aspect."""

    return _target_for_distance(source_sign, 3)


def saturn_aspects_10th(source_sign: int) -> int:
    """Return the sign receiving Saturn's 10th aspect."""

    return _target_for_distance(source_sign, 10)


def _target_for_distance(
    source_sign: int,
    distance: int,
) -> int:
    """Calculate target sign for an aspect distance."""

    _validate_sign_number(source_sign)

    if not 1 <= distance <= 12:
        raise ValueError("distance must be between 1 and 12")

    return (
        (source_sign - 1 + distance - 1) % 12
    ) + 1


# ============================================================
# Public API
# ============================================================


__all__ = [
    "Aspect",
    "CLASSICAL_PLANETS",
    "NODES",
    "DEFAULT_ASPECTS",
    "DEFAULT_NODE_ASPECTS",
    "sign_distance",
    "aspect_distances",
    "has_aspect",
    "get_aspects",
    "aspect_target_signs",
    "build_aspect_map",
    "planet_aspects_planet",
    "planet_aspects_house",
    "mars_aspects_4th",
    "mars_aspects_8th",
    "jupiter_aspects_5th",
    "jupiter_aspects_9th",
    "saturn_aspects_3rd",
    "saturn_aspects_10th",
]