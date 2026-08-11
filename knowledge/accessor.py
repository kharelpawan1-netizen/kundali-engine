"""
knowledge/accessor.py

Generic BirthChart access helpers.

This module provides a small collection of reusable helper
functions for accessing objects stored within a BirthChart.

The functions in this module intentionally do NOT perform
astrological calculations or interpretations. They simply
provide a consistent API for retrieving existing chart data.

Responsibilities
----------------
- Access planets
- Access houses
- Iterate over chart objects
- Perform simple existence checks
- Return existing model objects without modification

Non-Responsibilities
--------------------
- Astrology calculations
- Planet filtering by dignity
- Aspect calculations
- Interpretation
- Prediction

Dependencies
------------
- models.chart.BirthChart
- models.planet.Planet
- models.house.House

Version
-------
1.0.0

Compatible with
---------------
Python 3.9
"""

from typing import Dict, Iterator, List, Optional

from models.chart import BirthChart
from models.house import House
from models.planet import Planet


# ============================================================
# PLANET ACCESS
# ============================================================


def get_planet(
    chart: BirthChart,
    name: str,
) -> Optional[Planet]:
    """
    Return a planet by name.

    Parameters
    ----------
    chart
        Birth chart.

    name
        Planet name.

    Returns
    -------
    Planet or None
    """
    return chart.get_planet(name)


def get_planets(
    chart: BirthChart,
) -> Dict[str, Planet]:
    """
    Return the planet mapping.

    The returned dictionary is the chart's current
    planet collection.

    Parameters
    ----------
    chart
        Birth chart.

    Returns
    -------
    Dict[str, Planet]
    """
    return chart.planets


def iter_planets(
    chart: BirthChart,
) -> Iterator[Planet]:
    """
    Iterate over all planets.

    Parameters
    ----------
    chart
        Birth chart.

    Yields
    ------
    Planet
    """
    return iter(chart.planets.values())


def planet_names(
    chart: BirthChart,
) -> List[str]:
    """
    Return all planet names.

    Parameters
    ----------
    chart
        Birth chart.

    Returns
    -------
    List[str]
    """
    return list(chart.planets.keys())


def planet_exists(
    chart: BirthChart,
    name: str,
) -> bool:
    """
    Check whether a planet exists.

    Parameters
    ----------
    chart
        Birth chart.

    name
        Planet name.

    Returns
    -------
    bool
    """
    return chart.has_planet(name)


def planet_count(
    chart: BirthChart,
) -> int:
    """
    Return the number of planets.

    Parameters
    ----------
    chart
        Birth chart.

    Returns
    -------
    int
    """
    return chart.planet_count()


# ============================================================
# HOUSE ACCESS
# ============================================================


def get_house(
    chart: BirthChart,
    number: int,
) -> Optional[House]:
    """
    Return a house by number.

    Parameters
    ----------
    chart
        Birth chart.

    number
        House number.

    Returns
    -------
    House or None
    """
    return chart.get_house(number)


def get_houses(
    chart: BirthChart,
) -> Dict[int, House]:
    """
    Return the house mapping.

    Parameters
    ----------
    chart
        Birth chart.

    Returns
    -------
    Dict[int, House]
    """
    return chart.houses


def iter_houses(
    chart: BirthChart,
) -> Iterator[House]:
    """
    Iterate over all houses.

    Parameters
    ----------
    chart
        Birth chart.

    Yields
    ------
    House
    """
    return iter(chart.houses.values())


def house_exists(
    chart: BirthChart,
    number: int,
) -> bool:
    """
    Check whether a house exists.

    Parameters
    ----------
    chart
        Birth chart.

    number
        House number.

    Returns
    -------
    bool
    """
    return chart.has_house(number)


def house_count(
    chart: BirthChart,
) -> int:
    """
    Return the number of houses.

    Parameters
    ----------
    chart
        Birth chart.

    Returns
    -------
    int
    """
    return chart.house_count()