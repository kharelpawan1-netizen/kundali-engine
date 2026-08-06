"""
Yoga evaluation context helpers.

The existing interpretation layer already provides a normalized
InterpretationContext. This module provides small, safe helpers
for Yoga rules.
"""

from __future__ import annotations

from typing import Any, Optional


def planet(
    context: Any,
    name: str,
) -> Optional[Any]:
    """
    Return a planet from InterpretationContext.

    Returns None when the planet is unavailable.
    """

    planets = getattr(
        context,
        "planets",
        None,
    )

    if not planets:
        return None

    return planets.get(name)


def planet_house(
    context: Any,
    name: str,
) -> Optional[int]:
    """Return a planet's house."""

    value = planet(
        context,
        name,
    )

    if value is None:
        return None

    house = getattr(
        value,
        "house",
        None,
    )

    if house is None:
        return None

    return int(house)


def planet_sign(
    context: Any,
    name: str,
) -> Optional[str]:
    """Return a planet's sign."""

    value = planet(
        context,
        name,
    )

    if value is None:
        return None

    sign = getattr(
        value,
        "sign",
        None,
    )

    if sign is None:
        return None

    return str(sign)


def planets_in_house(
    context: Any,
    house: int,
):
    """
    Return normalized planets occupying a house.
    """

    planets = getattr(
        context,
        "planets",
        {},
    )

    return [
        value
        for value in planets.values()
        if getattr(value, "house", None)
        == house
    ]