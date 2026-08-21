"""
astrology/transit_predictions.py

Structured transit prediction-event engine for the Vedic Kundali system.

This module sits above:

    - astrology.transits
    - astrology.transit_aspects
    - astrology.transit_timeline

Its responsibility is to identify structured transit events involving
transiting planets and natal chart points.

Supported event categories include:

    - Transit planet entering a natal house
    - Transit planet contacting a natal planet
    - Transit planet contacting the natal Ascendant
    - Transit planet contacting the natal Moon
    - Transit planet contacting the natal Sun
    - Transit planet aspecting a natal planet
    - Transit planet aspecting the natal Ascendant
    - Transit planet aspecting the natal Moon
    - Transit planet aspecting the natal Sun

This module deliberately does NOT provide:

    - Predictive interpretation
    - Good/bad classification
    - Yoga formation
    - Dasha interpretation
    - Remedial recommendations
    - Psychological interpretation
    - Event certainty

Those responsibilities belong to higher-level interpretation modules.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from astrology.transit_timeline import (
    TransitSnapshot,
    filter_planet_snapshots,
)


# ============================================================
# Constants
# ============================================================

DEFAULT_CONTACT_ORB = 1.0
DEFAULT_ASPECT_ORB = 1.0

FULL_CIRCLE = 360.0
HALF_CIRCLE = 180.0

ZODIAC_SIGNS: Tuple[str, ...] = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class NatalPoint:
    """
    A natal chart reference point.

    Examples:

        NatalPoint(
            name="Moon",
            longitude=199.470553,
            house=8,
        )

        NatalPoint(
            name="Ascendant",
            longitude=349.20,
            house=1,
        )
    """

    name: str
    longitude: float
    house: Optional[int] = None


@dataclass(frozen=True)
class TransitPredictionEvent:
    """
    A structured transit prediction event.

    The event contains only measurable astronomical/chart
    relationships. It does not contain interpretation.
    """

    timestamp: datetime
    transit_planet: str
    natal_point: str
    event_type: str
    transit_longitude: float
    natal_longitude: float
    separation: float
    orb: float
    applying: Optional[bool]
    transit_sign: str
    natal_house: Optional[int] = None


# ============================================================
# Validation
# ============================================================

def validate_orb(
    orb: float,
    name: str = "orb",
) -> float:
    """Validate an angular orb."""
    if not isinstance(orb, (int, float)):
        raise TypeError(
            f"{name} must be numeric."
        )

    orb = float(orb)

    if orb < 0:
        raise ValueError(
            f"{name} cannot be negative."
        )

    if orb > HALF_CIRCLE:
        raise ValueError(
            f"{name} must not exceed {HALF_CIRCLE} degrees."
        )

    return orb


def validate_longitude(
    longitude: float,
    name: str = "longitude",
) -> float:
    """Validate and normalize a longitude."""
    if not isinstance(longitude, (int, float)):
        raise TypeError(
            f"{name} must be numeric."
        )

    return float(longitude) % FULL_CIRCLE


def validate_natal_point(
    point: NatalPoint,
) -> NatalPoint:
    """Validate a natal chart point."""
    if not isinstance(point, NatalPoint):
        raise TypeError(
            "point must be a NatalPoint instance."
        )

    if not isinstance(point.name, str):
        raise TypeError(
            "NatalPoint.name must be a string."
        )

    if not point.name.strip():
        raise ValueError(
            "NatalPoint.name cannot be empty."
        )

    longitude = validate_longitude(
        point.longitude,
        "NatalPoint.longitude",
    )

    if point.house is not None:
        if not isinstance(point.house, int):
            raise TypeError(
                "NatalPoint.house must be an integer or None."
            )

        if not 1 <= point.house <= 12:
            raise ValueError(
                "NatalPoint.house must be between 1 and 12."
            )

    return NatalPoint(
        name=point.name.strip(),
        longitude=longitude,
        house=point.house,
    )


# ============================================================
# Angular Mathematics
# ============================================================

def angular_separation(
    longitude_a: float,
    longitude_b: float,
) -> float:
    """
    Return the smallest angular separation between two longitudes.

    Result:

        0 <= separation <= 180
    """
    a = validate_longitude(
        longitude_a,
        "longitude_a",
    )

    b = validate_longitude(
        longitude_b,
        "longitude_b",
    )

    difference = abs(a - b)

    if difference > HALF_CIRCLE:
        difference = FULL_CIRCLE - difference

    return difference


def angular_distance_signed(
    from_longitude: float,
    to_longitude: float,
) -> float:
    """
    Return signed forward angular distance.

    Result:

        0 <= distance < 360
    """
    start = validate_longitude(
        from_longitude,
        "from_longitude",
    )

    end = validate_longitude(
        to_longitude,
        "to_longitude",
    )

    return (end - start) % FULL_CIRCLE


def aspect_orb(
    transit_longitude: float,
    natal_longitude: float,
    exact_angle: float,
) -> float:
    """
    Return the absolute orb from an exact aspect angle.
    """
    separation = angular_separation(
        transit_longitude,
        natal_longitude,
    )

    exact_angle = float(exact_angle) % FULL_CIRCLE

    if exact_angle > HALF_CIRCLE:
        exact_angle = FULL_CIRCLE - exact_angle

    return abs(
        separation - exact_angle
    )


# ============================================================
# Applying / Separating
# ============================================================

def determine_applying(
    previous_longitude: Optional[float],
    current_longitude: float,
    natal_longitude: float,
    exact_angle: float = 0.0,
) -> Optional[bool]:
    """
    Determine whether a transit is applying.

    This is determined from the change in angular orb.

    Returns:

        True      -> applying
        False     -> separating
        None      -> insufficient previous position
    """
    if previous_longitude is None:
        return None

    previous_orb = aspect_orb(
        previous_longitude,
        natal_longitude,
        exact_angle,
    )

    current_orb = aspect_orb(
        current_longitude,
        natal_longitude,
        exact_angle,
    )

    if current_orb < previous_orb:
        return True

    if current_orb > previous_orb:
        return False

    return None


# ============================================================
# Event Construction
# ============================================================

def build_prediction_event(
    snapshot: TransitSnapshot,
    natal_point: NatalPoint,
    event_type: str,
    orb: float,
    applying: Optional[bool],
) -> TransitPredictionEvent:
    """Create a structured prediction event."""
    natal_point = validate_natal_point(
        natal_point
    )

    orb = validate_orb(
        orb,
        "orb",
    )

    separation = angular_separation(
        snapshot.longitude,
        natal_point.longitude,
    )

    return TransitPredictionEvent(
        timestamp=snapshot.timestamp,
        transit_planet=snapshot.planet,
        natal_point=natal_point.name,
        event_type=event_type,
        transit_longitude=snapshot.longitude,
        natal_longitude=natal_point.longitude,
        separation=separation,
        orb=orb,
        applying=applying,
        transit_sign=snapshot.sign,
        natal_house=natal_point.house,
    )


# ============================================================
# Conjunction Detection
# ============================================================

def detect_conjunctions(
    snapshots: Sequence[TransitSnapshot],
    natal_points: Sequence[NatalPoint],
    orb: float = DEFAULT_CONTACT_ORB,
) -> List[TransitPredictionEvent]:
    """
    Detect transit conjunctions with natal points.

    A conjunction occurs when the angular separation is within
    the supplied orb of zero degrees.
    """
    orb = validate_orb(
        orb,
        "orb",
    )

    validated_points = tuple(
        validate_natal_point(point)
        for point in natal_points
    )

    events: List[TransitPredictionEvent] = []

    previous_longitudes: Dict[
        Tuple[str, str],
        float,
    ] = {}

    for snapshot in sorted(
        snapshots,
        key=lambda item: (
            item.timestamp,
            item.planet,
        ),
    ):
        for natal_point in validated_points:
            separation = angular_separation(
                snapshot.longitude,
                natal_point.longitude,
            )

            if separation <= orb:
                key = (
                    snapshot.planet,
                    natal_point.name,
                )

                previous_longitude = previous_longitudes.get(
                    key
                )

                applying = determine_applying(
                    previous_longitude,
                    snapshot.longitude,
                    natal_point.longitude,
                    exact_angle=0.0,
                )

                events.append(
                    build_prediction_event(
                        snapshot=snapshot,
                        natal_point=natal_point,
                        event_type="TRANSIT_CONJUNCTION",
                        orb=separation,
                        applying=applying,
                    )
                )

                previous_longitudes[key] = (
                    snapshot.longitude
                )

            else:
                previous_longitudes[
                    (
                        snapshot.planet,
                        natal_point.name,
                    )
                ] = snapshot.longitude

    return _deduplicate_events(
        events
    )


# ============================================================
# General Aspect Detection
# ============================================================

def detect_aspects(
    snapshots: Sequence[TransitSnapshot],
    natal_points: Sequence[NatalPoint],
    aspects: Sequence[float],
    orb: float = DEFAULT_ASPECT_ORB,
) -> List[TransitPredictionEvent]:
    """
    Detect transit aspects to natal points.

    ``aspects`` contains exact angular relationships.

    Examples:

        (0.0,)          conjunction
        (60.0,)         sextile
        (90.0,)         square
        (120.0,)        trine
        (180.0,)        opposition
    """
    orb = validate_orb(
        orb,
        "orb",
    )

    if not aspects:
        raise ValueError(
            "aspects must contain at least one angle."
        )

    normalized_aspects = tuple(
        float(aspect) % FULL_CIRCLE
        for aspect in aspects
    )

    validated_points = tuple(
        validate_natal_point(point)
        for point in natal_points
    )

    events: List[TransitPredictionEvent] = []

    previous_longitudes: Dict[
        Tuple[str, str, float],
        float,
    ] = {}

    ordered_snapshots = sorted(
        snapshots,
        key=lambda item: (
            item.timestamp,
            item.planet,
        ),
    )

    for snapshot in ordered_snapshots:
        for natal_point in validated_points:
            for exact_angle in normalized_aspects:
                current_orb = aspect_orb(
                    snapshot.longitude,
                    natal_point.longitude,
                    exact_angle,
                )

                if current_orb <= orb:
                    event_type = aspect_event_type(
                        exact_angle
                    )

                    key = (
                        snapshot.planet,
                        natal_point.name,
                        exact_angle,
                    )

                    previous_longitude = (
                        previous_longitudes.get(key)
                    )

                    applying = determine_applying(
                        previous_longitude,
                        snapshot.longitude,
                        natal_point.longitude,
                        exact_angle=exact_angle,
                    )

                    events.append(
                        build_prediction_event(
                            snapshot=snapshot,
                            natal_point=natal_point,
                            event_type=event_type,
                            orb=current_orb,
                            applying=applying,
                        )
                    )

                previous_longitudes[
                    (
                        snapshot.planet,
                        natal_point.name,
                        exact_angle,
                    )
                ] = snapshot.longitude

    return _deduplicate_events(
        events
    )


def aspect_event_type(
    exact_angle: float,
) -> str:
    """Return a stable event name for an aspect angle."""
    angle = float(exact_angle) % FULL_CIRCLE

    if angle == 0.0:
        return "TRANSIT_CONJUNCTION"

    if angle == 60.0:
        return "TRANSIT_SEXTILE"

    if angle == 90.0:
        return "TRANSIT_SQUARE"

    if angle == 120.0:
        return "TRANSIT_TRINE"

    if angle == 180.0:
        return "TRANSIT_OPPOSITION"

    return (
        "TRANSIT_ASPECT_"
        + format(angle, ".6f")
        .rstrip("0")
        .rstrip(".")
        .replace(".", "_")
    )


# ============================================================
# Natal Point Convenience APIs
# ============================================================

def natal_point(
    name: str,
    longitude: float,
    house: Optional[int] = None,
) -> NatalPoint:
    """Convenience constructor for a NatalPoint."""
    return validate_natal_point(
        NatalPoint(
            name=name,
            longitude=longitude,
            house=house,
        )
    )


def natal_planet(
    name: str,
    longitude: float,
    house: Optional[int] = None,
) -> NatalPoint:
    """Create a natal planetary reference point."""
    return natal_point(
        name=name,
        longitude=longitude,
        house=house,
    )


def natal_ascendant(
    longitude: float,
    house: int = 1,
) -> NatalPoint:
    """Create the natal Ascendant reference point."""
    return natal_point(
        name="Ascendant",
        longitude=longitude,
        house=house,
    )


def natal_sun(
    longitude: float,
    house: Optional[int] = None,
) -> NatalPoint:
    """Create the natal Sun reference point."""
    return natal_point(
        name="Sun",
        longitude=longitude,
        house=house,
    )


def natal_moon(
    longitude: float,
    house: Optional[int] = None,
) -> NatalPoint:
    """Create the natal Moon reference point."""
    return natal_point(
        name="Moon",
        longitude=longitude,
        house=house,
    )


# ============================================================
# Major Aspect API
# ============================================================

def detect_major_aspects(
    snapshots: Sequence[TransitSnapshot],
    natal_points: Sequence[NatalPoint],
    orb: float = DEFAULT_ASPECT_ORB,
) -> List[TransitPredictionEvent]:
    """
    Detect the five major Ptolemaic-style angular relationships:

        - Conjunction
        - Sextile
        - Square
        - Trine
        - Opposition

    This function identifies geometric relationships only.
    """
    return detect_aspects(
        snapshots=snapshots,
        natal_points=natal_points,
        aspects=(
            0.0,
            60.0,
            90.0,
            120.0,
            180.0,
        ),
        orb=orb,
    )


# ============================================================
# Vedic Transit Aspect API
# ============================================================

def detect_vedic_aspects(
    snapshots: Sequence[TransitSnapshot],
    natal_points: Sequence[NatalPoint],
    orb: float = DEFAULT_ASPECT_ORB,
) -> List[TransitPredictionEvent]:
    """
    Detect the seven traditional Parashari transit aspect
    relationships in a structural manner.

    Angular relationships used:

        1st  -> conjunction
        3rd  -> 60 degrees
        4th  -> 90 degrees
        5th  -> 120 degrees
        7th  -> 180 degrees
        9th  -> 240 degrees
        10th -> 270 degrees

    The returned events are geometric relationships only.

    Planet-specific special aspects such as:

        Mars 4th/8th
        Jupiter 5th/9th
        Saturn 3rd/10th

    are intentionally handled separately by higher-level
    Parashari aspect logic.
    """
    return detect_aspects(
        snapshots=snapshots,
        natal_points=natal_points,
        aspects=(
            0.0,
            60.0,
            90.0,
            120.0,
            180.0,
            240.0,
            270.0,
        ),
        orb=orb,
    )


# ============================================================
# Planet-Specific Transit Events
# ============================================================

def detect_planet_to_natal_planet_events(
    snapshots: Sequence[TransitSnapshot],
    natal_planets: Sequence[NatalPoint],
    orb: float = DEFAULT_CONTACT_ORB,
) -> List[TransitPredictionEvent]:
    """
    Detect transit-planet to natal-planet conjunctions.

    This function intentionally does not exclude cases where the
    transit planet and natal point have the same planetary name.
    Such filtering belongs to the caller.
    """
    return detect_conjunctions(
        snapshots=snapshots,
        natal_points=natal_planets,
        orb=orb,
    )


def detect_transit_to_ascendant_events(
    snapshots: Sequence[TransitSnapshot],
    ascendant_longitude: float,
    orb: float = DEFAULT_CONTACT_ORB,
) -> List[TransitPredictionEvent]:
    """Detect transit conjunctions to the natal Ascendant."""
    point = natal_ascendant(
        longitude=ascendant_longitude
    )

    return detect_conjunctions(
        snapshots=snapshots,
        natal_points=(point,),
        orb=orb,
    )


def detect_transit_to_moon_events(
    snapshots: Sequence[TransitSnapshot],
    moon_longitude: float,
    orb: float = DEFAULT_CONTACT_ORB,
) -> List[TransitPredictionEvent]:
    """Detect transit conjunctions to the natal Moon."""
    point = natal_moon(
        longitude=moon_longitude
    )

    return detect_conjunctions(
        snapshots=snapshots,
        natal_points=(point,),
        orb=orb,
    )


def detect_transit_to_sun_events(
    snapshots: Sequence[TransitSnapshot],
    sun_longitude: float,
    orb: float = DEFAULT_CONTACT_ORB,
) -> List[TransitPredictionEvent]:
    """Detect transit conjunctions to the natal Sun."""
    point = natal_sun(
        longitude=sun_longitude
    )

    return detect_conjunctions(
        snapshots=snapshots,
        natal_points=(point,),
        orb=orb,
    )


# ============================================================
# Event Filtering
# ============================================================

def filter_prediction_events_by_planet(
    events: Sequence[TransitPredictionEvent],
    planet: str,
) -> List[TransitPredictionEvent]:
    """Return prediction events generated by one transit planet."""
    return [
        event
        for event in events
        if event.transit_planet == planet
    ]


def filter_prediction_events_by_natal_point(
    events: Sequence[TransitPredictionEvent],
    natal_point_name: str,
) -> List[TransitPredictionEvent]:
    """Return events involving one natal point."""
    return [
        event
        for event in events
        if event.natal_point == natal_point_name
    ]


def filter_prediction_events_by_type(
    events: Sequence[TransitPredictionEvent],
    event_type: str,
) -> List[TransitPredictionEvent]:
    """Return events of one event type."""
    return [
        event
        for event in events
        if event.event_type == event_type
    ]


def filter_applying_events(
    events: Sequence[TransitPredictionEvent],
) -> List[TransitPredictionEvent]:
    """Return events classified as applying."""
    return [
        event
        for event in events
        if event.applying is True
    ]


def filter_separating_events(
    events: Sequence[TransitPredictionEvent],
) -> List[TransitPredictionEvent]:
    """Return events classified as separating."""
    return [
        event
        for event in events
        if event.applying is False
    ]


# ============================================================
# Event Ordering / Deduplication
# ============================================================

def _event_key(
    event: TransitPredictionEvent,
) -> Tuple[
    datetime,
    str,
    str,
    str,
    float,
]:
    """Return a stable event identity key."""
    return (
        event.timestamp,
        event.transit_planet,
        event.natal_point,
        event.event_type,
        round(event.natal_longitude, 9),
    )


def _deduplicate_events(
    events: Iterable[TransitPredictionEvent],
) -> List[TransitPredictionEvent]:
    """Remove duplicate prediction events while preserving chronology."""
    unique: Dict[
        Tuple[
            datetime,
            str,
            str,
            str,
            float,
        ],
        TransitPredictionEvent,
    ] = {}

    for event in events:
        unique[
            _event_key(event)
        ] = event

    result = list(
        unique.values()
    )

    result.sort(
        key=lambda event: (
            event.timestamp,
            event.transit_planet,
            event.natal_point,
            event.event_type,
        )
    )

    return result


# ============================================================
# Timeline Prediction API
# ============================================================

def build_transit_predictions(
    snapshots: Sequence[TransitSnapshot],
    natal_points: Sequence[NatalPoint],
    orb: float = DEFAULT_ASPECT_ORB,
    vedic: bool = True,
) -> List[TransitPredictionEvent]:
    """
    Build structured transit prediction events.

    When ``vedic`` is True, the structural Parashari angular
    relationships are used.

    When ``vedic`` is False, the five major conventional aspects
    are used.

    No interpretation is performed.
    """
    if vedic:
        return detect_vedic_aspects(
            snapshots=snapshots,
            natal_points=natal_points,
            orb=orb,
        )

    return detect_major_aspects(
        snapshots=snapshots,
        natal_points=natal_points,
        orb=orb,
    )


# ============================================================
# Prediction Event Summary
# ============================================================

def prediction_event_types(
    events: Sequence[TransitPredictionEvent],
) -> Tuple[str, ...]:
    """Return unique event types represented."""
    return tuple(
        sorted(
            {
                event.event_type
                for event in events
            }
        )
    )


def prediction_planets(
    events: Sequence[TransitPredictionEvent],
) -> Tuple[str, ...]:
    """Return unique transit planets represented."""
    return tuple(
        sorted(
            {
                event.transit_planet
                for event in events
            }
        )
    )


def prediction_natal_points(
    events: Sequence[TransitPredictionEvent],
) -> Tuple[str, ...]:
    """Return unique natal points represented."""
    return tuple(
        sorted(
            {
                event.natal_point
                for event in events
            }
        )
    )


def first_prediction_event(
    events: Sequence[TransitPredictionEvent],
) -> Optional[TransitPredictionEvent]:
    """Return the earliest prediction event."""
    if not events:
        return None

    return min(
        events,
        key=lambda event: event.timestamp,
    )


def last_prediction_event(
    events: Sequence[TransitPredictionEvent],
) -> Optional[TransitPredictionEvent]:
    """Return the latest prediction event."""
    if not events:
        return None

    return max(
        events,
        key=lambda event: event.timestamp,
    )


# ============================================================
# Public API
# ============================================================

__all__ = [
    "DEFAULT_CONTACT_ORB",
    "DEFAULT_ASPECT_ORB",
    "FULL_CIRCLE",
    "HALF_CIRCLE",
    "ZODIAC_SIGNS",
    "NatalPoint",
    "TransitPredictionEvent",
    "validate_orb",
    "validate_longitude",
    "validate_natal_point",
    "angular_separation",
    "angular_distance_signed",
    "aspect_orb",
    "determine_applying",
    "build_prediction_event",
    "detect_conjunctions",
    "detect_aspects",
    "aspect_event_type",
    "natal_point",
    "natal_planet",
    "natal_ascendant",
    "natal_sun",
    "natal_moon",
    "detect_major_aspects",
    "detect_vedic_aspects",
    "detect_planet_to_natal_planet_events",
    "detect_transit_to_ascendant_events",
    "detect_transit_to_moon_events",
    "detect_transit_to_sun_events",
    "filter_prediction_events_by_planet",
    "filter_prediction_events_by_natal_point",
    "filter_prediction_events_by_type",
    "filter_applying_events",
    "filter_separating_events",
    "build_transit_predictions",
    "prediction_event_types",
    "prediction_planets",
    "prediction_natal_points",
    "first_prediction_event",
    "last_prediction_event",
]