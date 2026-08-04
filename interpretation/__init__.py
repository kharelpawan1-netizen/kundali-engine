"""
interpretation/__init__.py

Public API for the Vedic interpretation layer.
"""

from interpretation.context import (
    PlanetContext,
    DashaContext,
    InterpretationContext,
    build_interpretation_context,
    get_planet,
    get_planets_in_house,
    get_planets_in_sign,
)

from interpretation.planet_analysis import (
    PlanetInterpretation,
    interpret_planet,
    analyze_planets,
    planet_analysis_report,
)

from interpretation.house_analysis import (
    HouseInterpretation,
    interpret_house,
    analyze_houses,
    house_analysis_report,
    occupied_houses,
    empty_houses,
    house_lord_placements,
)

__all__ = [
    # Context
    "PlanetContext",
    "DashaContext",
    "InterpretationContext",
    "build_interpretation_context",
    "get_planet",
    "get_planets_in_house",
    "get_planets_in_sign",

    # Planet interpretation
    "PlanetInterpretation",
    "interpret_planet",
    "analyze_planets",
    "planet_analysis_report",

    # House interpretation
    "HouseInterpretation",
    "interpret_house",
    "analyze_houses",
    "house_analysis_report",
    "occupied_houses",
    "empty_houses",
    "house_lord_placements",
]