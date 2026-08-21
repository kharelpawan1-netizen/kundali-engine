"""
astrology/transit_prediction_interpretation.py

Interpretation layer for transit prediction events in the Vedic Kundali system.

This module converts structurally detected transit prediction events into
deterministic, structured interpretive records.

Responsibilities:
    - Identify transit planet and natal point
    - Identify aspect/event type
    - Describe the structural significance of the transit
    - Classify the broad life domains associated with the natal point
    - Provide cautious, non-deterministic interpretation text
    - Preserve the original prediction event

It does not calculate:
    - Planetary positions
    - Natal chart positions
    - Transit aspects
    - Transit timelines
    - Vimshottari Dasha
    - Yogas
    - Strength calculations
    - Predictive timing

Those responsibilities remain in their respective modules.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Sequence, Tuple

from astrology.transit_predictions import TransitPredictionEvent


# ============================================================
# Constants
# ============================================================

ASPECT_EVENT_TYPES: Tuple[str, ...] = (
    "TRANSIT_CONJUNCTION",
    "TRANSIT_OPPOSITION",
    "TRANSIT_SQUARE",
    "TRANSIT_TRINE",
    "TRANSIT_ASPECT_240",
    "TRANSIT_ASPECT_270",
)


PLANET_NAMES: Tuple[str, ...] = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
)


NATAL_POINT_NAMES: Tuple[str, ...] = (
    "Sun",
    "Moon",
    "Ascendant",
)


# ============================================================
# Planetary Significance
# ============================================================

PLANET_DOMAINS: Dict[str, Tuple[str, ...]] = {
    "Sun": (
        "identity",
        "authority",
        "confidence",
        "vitality",
        "leadership",
        "recognition",
    ),
    "Moon": (
        "mind",
        "emotions",
        "habits",
        "comfort",
        "public_response",
        "mental_security",
    ),
    "Mars": (
        "action",
        "initiative",
        "competition",
        "courage",
        "conflict",
        "technical_energy",
    ),
    "Mercury": (
        "communication",
        "learning",
        "analysis",
        "business",
        "logic",
        "decision_making",
    ),
    "Jupiter": (
        "wisdom",
        "education",
        "guidance",
        "growth",
        "ethics",
        "opportunity",
    ),
    "Venus": (
        "relationships",
        "harmony",
        "comfort",
        "creativity",
        "values",
        "material_pleasure",
    ),
    "Saturn": (
        "discipline",
        "responsibility",
        "delay",
        "structure",
        "work",
        "endurance",
    ),
    "Rahu": (
        "ambition",
        "desire",
        "innovation",
        "foreign_influence",
        "unconventionality",
        "intensification",
    ),
    "Ketu": (
        "detachment",
        "introspection",
        "spirituality",
        "separation",
        "simplification",
        "inward_focus",
    ),
}


NATAL_POINT_DOMAINS: Dict[str, Tuple[str, ...]] = {
    "Sun": (
        "identity",
        "authority",
        "career_visibility",
        "confidence",
        "vitality",
    ),
    "Moon": (
        "mind",
        "emotions",
        "mental_security",
        "habits",
        "relationships",
        "public_life",
    ),
    "Ascendant": (
        "body",
        "personality",
        "self_direction",
        "appearance",
        "life_orientation",
        "general_activity",
    ),
}


# ============================================================
# Aspect Significance
# ============================================================

ASPECT_DESCRIPTIONS: Dict[str, str] = {
    "TRANSIT_CONJUNCTION": (
        "A conjunction concentrates the transit planet's influence "
        "directly on the natal point."
    ),
    "TRANSIT_OPPOSITION": (
        "An opposition emphasizes polarity, external circumstances, "
        "awareness, and the need to balance two opposing directions."
    ),
    "TRANSIT_SQUARE": (
        "A square indicates friction, pressure, adjustment, and "
        "circumstances requiring active response."
    ),
    "TRANSIT_TRINE": (
        "A trine indicates relative ease, support, flow, and an "
        "opportunity to express the involved principles constructively."
    ),
    "TRANSIT_ASPECT_240": (
        "This 240-degree relationship is treated structurally as a "
        "harmonious trinal relationship."
    ),
    "TRANSIT_ASPECT_270": (
        "This 270-degree relationship is treated structurally as a "
        "square relationship."
    ),
}


ASPECT_QUALITIES: Dict[str, str] = {
    "TRANSIT_CONJUNCTION": "intensifying",
    "TRANSIT_OPPOSITION": "polarizing",
    "TRANSIT_SQUARE": "challenging",
    "TRANSIT_TRINE": "supportive",
    "TRANSIT_ASPECT_240": "supportive",
    "TRANSIT_ASPECT_270": "challenging",
}


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class TransitInterpretation:
    """Structured interpretation of a transit prediction event."""

    timestamp: datetime
    transit_planet: str
    natal_point: str
    event_type: str
    quality: str
    domains: Tuple[str, ...]
    transit_domains: Tuple[str, ...]
    natal_domains: Tuple[str, ...]
    structural_summary: str
    interpretation: str
    caution: str
    source_event: TransitPredictionEvent


# ============================================================
# Validation
# ============================================================

def validate_prediction_event(
    event: TransitPredictionEvent,
) -> TransitPredictionEvent:
    """Validate that an object is a TransitPredictionEvent."""
    if not isinstance(event, TransitPredictionEvent):
        raise TypeError(
            "event must be a TransitPredictionEvent instance."
        )

    return event


def validate_planet(planet: str) -> str:
    """Validate a supported transit planet."""
    if not isinstance(planet, str):
        raise TypeError("planet must be a string.")

    if planet not in PLANET_NAMES:
        raise ValueError(
            f"Unsupported planet: {planet!r}."
        )

    return planet


def validate_natal_point(natal_point: str) -> str:
    """Validate a supported natal point."""
    if not isinstance(natal_point, str):
        raise TypeError(
            "natal_point must be a string."
        )

    if natal_point not in NATAL_POINT_NAMES:
        raise ValueError(
            f"Unsupported natal point: {natal_point!r}."
        )

    return natal_point


# ============================================================
# Event Attribute Extraction
# ============================================================

def prediction_transit_planet(
    event: TransitPredictionEvent,
) -> str:
    """Return the transit planet represented by an event."""
    validate_prediction_event(event)

    return event.transit_planet


def prediction_natal_point(
    event: TransitPredictionEvent,
) -> str:
    """Return the natal point represented by an event."""
    validate_prediction_event(event)

    return event.natal_point


def prediction_event_type(
    event: TransitPredictionEvent,
) -> str:
    """Return the event type."""
    validate_prediction_event(event)

    return event.event_type


# ============================================================
# Domain Classification
# ============================================================

def transit_planet_domains(
    planet: str,
) -> Tuple[str, ...]:
    """Return broad significations associated with a transit planet."""
    planet = validate_planet(planet)

    return PLANET_DOMAINS[planet]


def natal_point_domains(
    natal_point: str,
) -> Tuple[str, ...]:
    """Return broad significations associated with a natal point."""
    natal_point = validate_natal_point(natal_point)

    return NATAL_POINT_DOMAINS[natal_point]


def combined_domains(
    transit_planet: str,
    natal_point: str,
) -> Tuple[str, ...]:
    """
    Combine transit-planet and natal-point domains.

    Ordering is deterministic and duplicates are removed.
    """
    transit_domains = transit_planet_domains(
        transit_planet
    )

    natal_domains = natal_point_domains(
        natal_point
    )

    result: List[str] = []

    for domain in transit_domains + natal_domains:
        if domain not in result:
            result.append(domain)

    return tuple(result)


# ============================================================
# Aspect Interpretation
# ============================================================

def aspect_description(
    event_type: str,
) -> str:
    """Return the structural meaning of an event type."""
    if not isinstance(event_type, str):
        raise TypeError(
            "event_type must be a string."
        )

    if event_type not in ASPECT_DESCRIPTIONS:
        raise ValueError(
            f"Unsupported prediction event type: {event_type!r}."
        )

    return ASPECT_DESCRIPTIONS[event_type]


def aspect_quality(
    event_type: str,
) -> str:
    """Return the broad qualitative classification of an aspect."""
    if not isinstance(event_type, str):
        raise TypeError(
            "event_type must be a string."
        )

    if event_type not in ASPECT_QUALITIES:
        raise ValueError(
            f"Unsupported prediction event type: {event_type!r}."
        )

    return ASPECT_QUALITIES[event_type]


# ============================================================
# Text Construction
# ============================================================

def build_structural_summary(
    transit_planet: str,
    natal_point: str,
    event_type: str,
) -> str:
    """
    Build a concise structural description.

    This function deliberately avoids deterministic prediction.
    """
    transit_planet = validate_planet(transit_planet)
    natal_point = validate_natal_point(natal_point)

    description = aspect_description(event_type)

    return (
        f"{transit_planet} forms {event_type} with "
        f"natal {natal_point}. {description}"
    )


def build_interpretation(
    transit_planet: str,
    natal_point: str,
    event_type: str,
) -> str:
    """
    Build a cautious interpretive statement.

    Interpretation is deliberately general because house placement,
    dignity, aspects, yogas, strength, dasha, and natal context must
    be evaluated separately before making a specific prediction.
    """
    transit_planet = validate_planet(transit_planet)
    natal_point = validate_natal_point(natal_point)

    quality = aspect_quality(event_type)

    transit_domains = transit_planet_domains(
        transit_planet
    )

    natal_domains = natal_point_domains(
        natal_point
    )

    transit_focus = ", ".join(
        transit_domains[:3]
    )

    natal_focus = ", ".join(
        natal_domains[:3]
    )

    return (
        f"This {quality} transit may bring the themes of "
        f"{transit_focus} into greater awareness through natal "
        f"{natal_point} matters such as {natal_focus}. "
        f"The actual manifestation should be judged from the "
        f"natal chart, house placement, planetary strength, "
        f"other aspects, and concurrent dasha periods."
    )


def build_caution(
    event_type: str,
) -> str:
    """Return a standardized interpretive caution."""
    quality = aspect_quality(event_type)

    if quality == "challenging":
        return (
            "This is a structural indication of pressure or "
            "adjustment, not a guaranteed negative event."
        )

    if quality == "intensifying":
        return (
            "A conjunction concentrates the involved themes; "
            "its constructive or difficult expression depends "
            "on the complete natal and timing context."
        )

    if quality == "polarizing":
        return (
            "An opposition does not inherently indicate harm; "
            "it highlights balance, awareness, and polarity."
        )

    return (
        "A supportive aspect does not guarantee a specific event; "
        "the complete natal chart and timing context must be considered."
    )


# ============================================================
# Single Event Interpretation
# ============================================================

def interpret_prediction_event(
    event: TransitPredictionEvent,
) -> TransitInterpretation:
    """
    Interpret one structurally detected prediction event.
    """
    event = validate_prediction_event(event)

    transit_planet = prediction_transit_planet(event)
    natal_point = prediction_natal_point(event)
    event_type = prediction_event_type(event)

    transit_planet = validate_planet(
        transit_planet
    )

    natal_point = validate_natal_point(
        natal_point
    )

    quality = aspect_quality(
        event_type
    )

    transit_domains = transit_planet_domains(
        transit_planet
    )

    natal_domains = natal_point_domains(
        natal_point
    )

    domains = combined_domains(
        transit_planet,
        natal_point,
    )

    structural_summary = build_structural_summary(
        transit_planet,
        natal_point,
        event_type,
    )

    interpretation = build_interpretation(
        transit_planet,
        natal_point,
        event_type,
    )

    caution = build_caution(
        event_type
    )

    return TransitInterpretation(
        timestamp=event.timestamp,
        transit_planet=transit_planet,
        natal_point=natal_point,
        event_type=event_type,
        quality=quality,
        domains=domains,
        transit_domains=transit_domains,
        natal_domains=natal_domains,
        structural_summary=structural_summary,
        interpretation=interpretation,
        caution=caution,
        source_event=event,
    )


# ============================================================
# Batch Interpretation
# ============================================================

def interpret_prediction_events(
    events: Sequence[TransitPredictionEvent],
) -> List[TransitInterpretation]:
    """Interpret a sequence of prediction events."""
    interpretations = [
        interpret_prediction_event(event)
        for event in events
    ]

    interpretations.sort(
        key=lambda item: (
            item.timestamp,
            item.transit_planet,
            item.natal_point,
        )
    )

    return interpretations


def build_transit_prediction_interpretations(
    events: Sequence[TransitPredictionEvent],
) -> List[TransitInterpretation]:
    """
    Public convenience API for interpreting prediction events.
    """
    return interpret_prediction_events(events)


# ============================================================
# Filtering
# ============================================================

def filter_interpretations_by_planet(
    interpretations: Sequence[TransitInterpretation],
    planet: str,
) -> List[TransitInterpretation]:
    """Filter interpretations by transit planet."""
    planet = validate_planet(planet)

    return [
        item
        for item in interpretations
        if item.transit_planet == planet
    ]


def filter_interpretations_by_natal_point(
    interpretations: Sequence[TransitInterpretation],
    natal_point: str,
) -> List[TransitInterpretation]:
    """Filter interpretations by natal point."""
    natal_point = validate_natal_point(
        natal_point
    )

    return [
        item
        for item in interpretations
        if item.natal_point == natal_point
    ]


def filter_interpretations_by_event_type(
    interpretations: Sequence[TransitInterpretation],
    event_type: str,
) -> List[TransitInterpretation]:
    """Filter interpretations by aspect/event type."""
    aspect_quality(event_type)

    return [
        item
        for item in interpretations
        if item.event_type == event_type
    ]


def filter_challenging_interpretations(
    interpretations: Sequence[TransitInterpretation],
) -> List[TransitInterpretation]:
    """Return interpretations classified as challenging."""
    return [
        item
        for item in interpretations
        if item.quality == "challenging"
    ]


def filter_supportive_interpretations(
    interpretations: Sequence[TransitInterpretation],
) -> List[TransitInterpretation]:
    """Return interpretations classified as supportive."""
    return [
        item
        for item in interpretations
        if item.quality == "supportive"
    ]


# ============================================================
# Summary Utilities
# ============================================================

def interpretation_planets(
    interpretations: Sequence[TransitInterpretation],
) -> Tuple[str, ...]:
    """Return unique transit planets represented."""
    return tuple(
        sorted(
            {
                item.transit_planet
                for item in interpretations
            }
        )
    )


def interpretation_natal_points(
    interpretations: Sequence[TransitInterpretation],
) -> Tuple[str, ...]:
    """Return unique natal points represented."""
    return tuple(
        sorted(
            {
                item.natal_point
                for item in interpretations
            }
        )
    )


def interpretation_event_types(
    interpretations: Sequence[TransitInterpretation],
) -> Tuple[str, ...]:
    """Return unique event types represented."""
    return tuple(
        sorted(
            {
                item.event_type
                for item in interpretations
            }
        )
    )


def interpretation_qualities(
    interpretations: Sequence[TransitInterpretation],
) -> Tuple[str, ...]:
    """Return unique qualitative classifications."""
    return tuple(
        sorted(
            {
                item.quality
                for item in interpretations
            }
        )
    )


def interpretation_domains(
    interpretations: Sequence[TransitInterpretation],
) -> Tuple[str, ...]:
    """Return all unique domains represented."""
    domains: List[str] = []

    for interpretation in interpretations:
        for domain in interpretation.domains:
            if domain not in domains:
                domains.append(domain)

    return tuple(domains)


# ============================================================
# Public API
# ============================================================

__all__ = [
    "ASPECT_EVENT_TYPES",
    "PLANET_NAMES",
    "NATAL_POINT_NAMES",
    "PLANET_DOMAINS",
    "NATAL_POINT_DOMAINS",
    "ASPECT_DESCRIPTIONS",
    "ASPECT_QUALITIES",
    "TransitInterpretation",
    "validate_prediction_event",
    "validate_planet",
    "validate_natal_point",
    "prediction_transit_planet",
    "prediction_natal_point",
    "prediction_event_type",
    "transit_planet_domains",
    "natal_point_domains",
    "combined_domains",
    "aspect_description",
    "aspect_quality",
    "build_structural_summary",
    "build_interpretation",
    "build_caution",
    "interpret_prediction_event",
    "interpret_prediction_events",
    "build_transit_prediction_interpretations",
    "filter_interpretations_by_planet",
    "filter_interpretations_by_natal_point",
    "filter_interpretations_by_event_type",
    "filter_challenging_interpretations",
    "filter_supportive_interpretations",
    "interpretation_planets",
    "interpretation_natal_points",
    "interpretation_event_types",
    "interpretation_qualities",
    "interpretation_domains",
]