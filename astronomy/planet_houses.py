"""
astronomy/planet_houses.py

Planet-to-house assignment for the Kundali Engine.

This module assigns already-calculated planets to houses.
It does not calculate house cusps itself.

The supplied house mapping determines the house system:
    - Whole Sign houses
    - Cusp-based Bhava houses
    - Any future supported house system

Python Version:
    3.9+
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from astronomy.houses import house_from_longitude
from models.house import House
from models.planet import Planet


def assign_planet_to_house(
    planet: Planet,
    houses: Dict[int, House],
) -> int:
    """
    Determine and assign the house occupied by one planet.

    Parameters
    ----------
    planet
        Planet whose longitude is to be assigned.

    houses
        Twelve-house mapping used for the calculation.

    Returns
    -------
    int
        House number occupied by the planet.

    Notes
    -----
    The planet's longitude is used directly. The supplied house
    cusp mapping determines the house system.
    """

    house_number = house_from_longitude(
        planet.longitude,
        houses,
    )

    planet.house = house_number

    return house_number


def assign_planets_to_houses(
    planets: Iterable[Planet],
    houses: Dict[int, House],
) -> Tuple[List[Planet], Dict[int, House]]:
    """
    Assign multiple planets to houses.

    Each planet receives its house number through ``planet.house``.
    Each corresponding House object receives the planet name in its
    ``planets`` list.

    Parameters
    ----------
    planets
        Iterable of Planet objects.

    houses
        Twelve-house mapping.

    Returns
    -------
    tuple
        Updated list of planets and updated house mapping.

    Raises
    ------
    TypeError
        If an item in planets is not a Planet instance.
    """

    updated_planets = list(planets)

    for planet in updated_planets:
        if not isinstance(planet, Planet):
            raise TypeError("planets must contain only Planet instances")

        house_number = assign_planet_to_house(
            planet,
            houses,
        )

        houses[house_number].add_planet(
            planet.name,
        )

    return updated_planets, houses


__all__ = [
    "assign_planet_to_house",
    "assign_planets_to_houses",
]
