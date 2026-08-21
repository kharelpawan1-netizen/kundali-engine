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

from interpretation.dignity_analysis import (
    DignityInterpretation,
    interpret_dignity,
    analyze_dignities,
    dignity_analysis_report,
)

from interpretation.aspect_analysis import (
    AspectInterpretation,
    ASPECT_RULES,
    aspect_houses_from_house,
    planet_aspects,
    interpret_aspect,
    aspecting_planets,
    analyze_aspects,
)

from interpretation.yoga_analysis import (
    YOGA_THEMES,
    YOGA_CAUTIONS,
    YogaInterpretation,
    interpret_yoga,
    interpret_yoga_results,
    analyze_yoga_interpretations,
    detected_yoga_interpretations,
    yoga_interpretations_by_category,
    yoga_interpretations_involving_planet,
    yoga_interpretations_involving_house,
    yoga_analysis_report,
)

from interpretation.synthesis import (
    ChartInterpretation,
    collect_themes,
    collect_evidence,
    collect_cautions,
    synthesize_planets,
    synthesize_houses,
    synthesize_dignities,
    synthesize_aspects,
    synthesize_yogas,
    synthesize_chart,
    detected_yogas,
    synthesis_report,
)


__all__ = [
    # ========================================================
    # Context
    # ========================================================

    "PlanetContext",
    "DashaContext",
    "InterpretationContext",
    "build_interpretation_context",
    "get_planet",
    "get_planets_in_house",
    "get_planets_in_sign",

    # ========================================================
    # Planet interpretation
    # ========================================================

    "PlanetInterpretation",
    "interpret_planet",
    "analyze_planets",
    "planet_analysis_report",

    # ========================================================
    # House interpretation
    # ========================================================

    "HouseInterpretation",
    "interpret_house",
    "analyze_houses",
    "house_analysis_report",
    "occupied_houses",
    "empty_houses",
    "house_lord_placements",

    # ========================================================
    # Dignity interpretation
    # ========================================================

    "DignityInterpretation",
    "interpret_dignity",
    "analyze_dignities",
    "dignity_analysis_report",

    # ========================================================
    # Aspect interpretation
    # ========================================================

    "ASPECT_RULES",
    "AspectInterpretation",
    "aspect_houses_from_house",
    "planet_aspects",
    "interpret_aspect",
    "aspecting_planets",
    "analyze_aspects",

    # ========================================================
    # Yoga interpretation
    # ========================================================

    "YOGA_THEMES",
    "YOGA_CAUTIONS",
    "YogaInterpretation",
    "interpret_yoga",
    "interpret_yoga_results",
    "analyze_yoga_interpretations",
    "detected_yoga_interpretations",
    "yoga_interpretations_by_category",
    "yoga_interpretations_involving_planet",
    "yoga_interpretations_involving_house",
    "yoga_analysis_report",

    # ========================================================
    # Chart synthesis
    # ========================================================

    "ChartInterpretation",
    "collect_themes",
    "collect_evidence",
    "collect_cautions",
    "synthesize_planets",
    "synthesize_houses",
    "synthesize_dignities",
    "synthesize_aspects",
    "synthesize_yogas",
    "synthesize_chart",
    "detected_yogas",
    "synthesis_report",
]