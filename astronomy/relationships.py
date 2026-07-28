"""
Natural planetary relationships.

According to Brihat Parashara Hora Shastra.
"""

from __future__ import annotations

from models.graha import Graha
from models.relationship import Relationship

# ---------------------------------------------------------------------
# Natural Friendships (BPHS)
# ---------------------------------------------------------------------

FRIENDS = {
    Graha.SUN: {
        Graha.MOON,
        Graha.MARS,
        Graha.JUPITER,
    },
    Graha.MOON: {
        Graha.SUN,
        Graha.MERCURY,
    },
    Graha.MARS: {
        Graha.SUN,
        Graha.MOON,
        Graha.JUPITER,
    },
    Graha.MERCURY: {
        Graha.SUN,
        Graha.VENUS,
    },
    Graha.JUPITER: {
        Graha.SUN,
        Graha.MOON,
        Graha.MARS,
    },
    Graha.VENUS: {
        Graha.MERCURY,
        Graha.SATURN,
    },
    Graha.SATURN: {
        Graha.MERCURY,
        Graha.VENUS,
    },
}

# ---------------------------------------------------------------------
# Natural Enmities (BPHS)
# ---------------------------------------------------------------------

ENEMIES = {
    Graha.SUN: {
        Graha.VENUS,
        Graha.SATURN,
    },
    Graha.MOON: set(),
    Graha.MARS: {
        Graha.MERCURY,
    },
    Graha.MERCURY: {
        Graha.MOON,
    },
    Graha.JUPITER: {
        Graha.MERCURY,
        Graha.VENUS,
    },
    Graha.VENUS: {
        Graha.SUN,
        Graha.MOON,
    },
    Graha.SATURN: {
        Graha.SUN,
        Graha.MOON,
        Graha.MARS,
    },
}


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def relationship(
    graha: Graha,
    other: Graha,
) -> Relationship:
    """
    Return the natural planetary relationship.

    Parameters
    ----------
    graha
        Reference planet.

    other
        Planet being evaluated.

    Returns
    -------
    Relationship
    """

    if other in FRIENDS[graha]:
        return Relationship.FRIEND

    if other in ENEMIES[graha]:
        return Relationship.ENEMY

    return Relationship.NEUTRAL


def natural_relationship(
    graha: Graha,
    other: Graha,
) -> Relationship:
    """
    Return the BPHS natural relationship between two planets.

    This is a convenience wrapper around ``relationship()`` and is
    used by higher-level modules such as Panchadha Maitri.
    """

    return relationship(
        graha,
        other,
    )


__all__ = [
    "FRIENDS",
    "ENEMIES",
    "relationship",
    "natural_relationship",
]
