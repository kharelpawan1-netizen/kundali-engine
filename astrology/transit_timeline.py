"""
astrology/transit_timeline.py

Transit timeline engine for the Vedic Kundali system.

Provides date-range transit tracking for planets, including:

    - Transit longitude
    - Sign
    - Degree within sign
    - Nakshatra
    - Pada
    - Retrograde/direct state
    - Sign ingress events
    - Retrograde station events
    - Direct station events
    - Timeline filtering

The module is intentionally focused on transit chronology.

It does not calculate:
    - Birth-chart planetary positions
    - Vimshottari Dasha
    - Transit aspects
    - Yoga formation
    - Predictive interpretation

Those responsibilities remain in their respective modules.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

from astrology.transits import (
    TransitPosition,
    calculate_all_transits,
)


# ============================================================
# Constants
# ============================================================

DEFAULT_STEP_HOURS = 24.0

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
class TransitSnapshot:
    """Planetary transit state at one point in time."""

    timestamp: datetime
    planet: str
    longitude: float
    sign: str
    degree_in_sign: float
    nakshatra: str
    pada: int
    retrograde: bool


@dataclass(frozen=True)
class TransitEvent:
    """A discrete event detected in a transit timeline."""

    planet: str
    event_type: str
    timestamp: datetime
    sign: Optional[str]
    longitude: float
    retrograde: bool
    previous_sign: Optional[str] = None
    previous_retrograde: Optional[bool] = None


# ============================================================
# Validation
# ============================================================

def validate_datetime(
    value: datetime,
    name: str = "datetime",
) -> datetime:
    """Validate a datetime value."""
    if not isinstance(value, datetime):
        raise TypeError(
            f"{name} must be a datetime instance."
        )

    return value


def validate_step_hours(step_hours: float) -> float:
    """Validate timeline sampling interval."""
    if not isinstance(step_hours, (int, float)):
        raise TypeError(
            "step_hours must be numeric."
        )

    if step_hours <= 0:
        raise ValueError(
            "step_hours must be greater than zero."
        )

    return float(step_hours)


def validate_date_range(
    start: datetime,
    end: datetime,
) -> Tuple[datetime, datetime]:
    """Validate a chronological date range."""
    start = validate_datetime(
        start,
        "start",
    )

    end = validate_datetime(
        end,
        "end",
    )

    if end < start:
        raise ValueError(
            "end must be greater than or equal to start."
        )

    return start, end


def validate_planet_name(planet: str) -> str:
    """Validate a planet name."""
    if not isinstance(planet, str):
        raise TypeError(
            "planet must be a string."
        )

    planet = planet.strip()

    if not planet:
        raise ValueError(
            "planet cannot be empty."
        )

    return planet


# ============================================================
# Transit Position Helpers
# ============================================================

def _position_map(
    moment: datetime,
) -> Dict[str, TransitPosition]:
    """
    Return transit positions indexed by planet.

    The underlying transit engine currently exposes
    ``calculate_all_transits(moment)`` as its public calculation
    API. This helper provides efficient planet-level lookup without
    requiring a separate ``calculate_transit`` function.
    """
    positions = calculate_all_transits(moment)

    return {
        position.planet: position
        for position in positions
    }


def calculate_planet_transit(
    planet: str,
    moment: datetime,
) -> TransitPosition:
    """
    Return the transit position of one planet.

    This is a compatibility/helper API built on top of the existing
    ``calculate_all_transits`` implementation.
    """
    planet = validate_planet_name(planet)
    moment = validate_datetime(
        moment,
        "moment",
    )

    positions = _position_map(moment)

    try:
        return positions[planet]
    except KeyError as exc:
        available = ", ".join(
            sorted(positions.keys())
        )

        raise ValueError(
            f"Unknown or unsupported transit planet: "
            f"{planet}. Available planets: {available}"
        ) from exc


def snapshot_from_position(
    timestamp: datetime,
    position: TransitPosition,
) -> TransitSnapshot:
    """Convert a TransitPosition into a timestamped snapshot."""
    timestamp = validate_datetime(
        timestamp,
        "timestamp",
    )

    if not isinstance(
        position,
        TransitPosition,
    ):
        raise TypeError(
            "position must be a TransitPosition instance."
        )

    return TransitSnapshot(
        timestamp=timestamp,
        planet=position.planet,
        longitude=position.longitude,
        sign=position.sign,
        degree_in_sign=position.degree_in_sign,
        nakshatra=position.nakshatra,
        pada=position.pada,
        retrograde=position.retrograde,
    )


# ============================================================
# Single-Planet Timeline
# ============================================================

def generate_planet_transit_timeline(
    planet: str,
    start: datetime,
    end: datetime,
    step_hours: float = DEFAULT_STEP_HOURS,
) -> List[TransitSnapshot]:
    """
    Generate a sampled transit timeline for one planet.

    The first snapshot is always generated at ``start``.
    Additional snapshots are generated at ``step_hours`` intervals.
    The final snapshot is always generated at ``end``.
    """
    planet = validate_planet_name(planet)

    start, end = validate_date_range(
        start,
        end,
    )

    step_hours = validate_step_hours(
        step_hours,
    )

    snapshots: List[TransitSnapshot] = []

    current = start
    step = timedelta(
        hours=step_hours,
    )

    while current < end:
        position = calculate_planet_transit(
            planet=planet,
            moment=current,
        )

        snapshots.append(
            snapshot_from_position(
                current,
                position,
            )
        )

        current += step

    final_position = calculate_planet_transit(
        planet=planet,
        moment=end,
    )

    snapshots.append(
        snapshot_from_position(
            end,
            final_position,
        )
    )

    return snapshots


# ============================================================
# All-Planet Timeline
# ============================================================

def generate_all_transit_timeline(
    start: datetime,
    end: datetime,
    step_hours: float = DEFAULT_STEP_HOURS,
    planets: Optional[Sequence[str]] = None,
) -> List[TransitSnapshot]:
    """
    Generate sampled transit snapshots for multiple planets.

    If ``planets`` is omitted, all planets supported by
    ``calculate_all_transits`` are included.

    Snapshots are ordered chronologically and then by planet.
    """
    start, end = validate_date_range(
        start,
        end,
    )

    step_hours = validate_step_hours(
        step_hours,
    )

    requested_planets: Optional[Tuple[str, ...]] = None

    if planets is not None:
        requested_planets = tuple(
            validate_planet_name(
                planet
            )
            for planet in planets
        )

        if not requested_planets:
            raise ValueError(
                "planets must contain at least one planet."
            )

    snapshots: List[TransitSnapshot] = []

    current = start
    step = timedelta(
        hours=step_hours,
    )

    while current < end:
        positions = calculate_all_transits(
            current
        )

        for position in positions:
            if (
                requested_planets is not None
                and position.planet not in requested_planets
            ):
                continue

            snapshots.append(
                snapshot_from_position(
                    current,
                    position,
                )
            )

        current += step

    final_positions = calculate_all_transits(
        end
    )

    for position in final_positions:
        if (
            requested_planets is not None
            and position.planet not in requested_planets
        ):
            continue

        snapshots.append(
            snapshot_from_position(
                end,
                position,
            )
        )

    snapshots.sort(
        key=lambda item: (
            item.timestamp,
            item.planet,
        )
    )

    return snapshots


# ============================================================
# Timeline Filtering
# ============================================================

def filter_planet_snapshots(
    snapshots: Sequence[TransitSnapshot],
    planet: str,
) -> List[TransitSnapshot]:
    """Return snapshots belonging to one planet."""
    planet = validate_planet_name(
        planet
    )

    return [
        snapshot
        for snapshot in snapshots
        if snapshot.planet == planet
    ]


def filter_retrograde_snapshots(
    snapshots: Sequence[TransitSnapshot],
    retrograde: bool = True,
) -> List[TransitSnapshot]:
    """Return snapshots matching retrograde state."""
    return [
        snapshot
        for snapshot in snapshots
        if snapshot.retrograde == retrograde
    ]


def filter_sign_snapshots(
    snapshots: Sequence[TransitSnapshot],
    sign: str,
) -> List[TransitSnapshot]:
    """Return snapshots where the planet occupies a specified sign."""
    if not isinstance(sign, str):
        raise TypeError(
            "sign must be a string."
        )

    sign = sign.strip()

    if not sign:
        raise ValueError(
            "sign cannot be empty."
        )

    return [
        snapshot
        for snapshot in snapshots
        if snapshot.sign == sign
    ]


# ============================================================
# Event Detection
# ============================================================

def _group_snapshots_by_planet(
    snapshots: Sequence[TransitSnapshot],
) -> Dict[str, List[TransitSnapshot]]:
    """Group snapshots by planet and sort each group chronologically."""
    grouped: Dict[
        str,
        List[TransitSnapshot],
    ] = {}

    for snapshot in snapshots:
        grouped.setdefault(
            snapshot.planet,
            [],
        ).append(snapshot)

    for planet_snapshots in grouped.values():
        planet_snapshots.sort(
            key=lambda item: item.timestamp
        )

    return grouped


def detect_sign_changes(
    snapshots: Sequence[TransitSnapshot],
) -> List[TransitEvent]:
    """
    Detect sign ingress events from sampled snapshots.

    A sign change is detected when two consecutive snapshots
    for the same planet have different signs.
    """
    events: List[TransitEvent] = []

    grouped = _group_snapshots_by_planet(
        snapshots
    )

    for planet_snapshots in grouped.values():
        previous: Optional[TransitSnapshot] = None

        for current in planet_snapshots:
            if previous is not None:
                if current.sign != previous.sign:
                    events.append(
                        TransitEvent(
                            planet=current.planet,
                            event_type="SIGN_INGRESS",
                            timestamp=current.timestamp,
                            sign=current.sign,
                            longitude=current.longitude,
                            retrograde=current.retrograde,
                            previous_sign=previous.sign,
                            previous_retrograde=previous.retrograde,
                        )
                    )

            previous = current

    events.sort(
        key=lambda event: (
            event.timestamp,
            event.planet,
        )
    )

    return events


def detect_retrograde_stations(
    snapshots: Sequence[TransitSnapshot],
) -> List[TransitEvent]:
    """
    Detect changes between direct and retrograde motion.

    A transition:

        Direct -> Retrograde

    produces ``RETROGRADE_STATION``.

    A transition:

        Retrograde -> Direct

    produces ``DIRECT_STATION``.
    """
    events: List[TransitEvent] = []

    grouped = _group_snapshots_by_planet(
        snapshots
    )

    for planet_snapshots in grouped.values():
        previous: Optional[TransitSnapshot] = None

        for current in planet_snapshots:
            if previous is not None:
                if (
                    not previous.retrograde
                    and current.retrograde
                ):
                    events.append(
                        TransitEvent(
                            planet=current.planet,
                            event_type="RETROGRADE_STATION",
                            timestamp=current.timestamp,
                            sign=current.sign,
                            longitude=current.longitude,
                            retrograde=True,
                            previous_sign=previous.sign,
                            previous_retrograde=False,
                        )
                    )

                elif (
                    previous.retrograde
                    and not current.retrograde
                ):
                    events.append(
                        TransitEvent(
                            planet=current.planet,
                            event_type="DIRECT_STATION",
                            timestamp=current.timestamp,
                            sign=current.sign,
                            longitude=current.longitude,
                            retrograde=False,
                            previous_sign=previous.sign,
                            previous_retrograde=True,
                        )
                    )

            previous = current

    events.sort(
        key=lambda event: (
            event.timestamp,
            event.planet,
        )
    )

    return events


def detect_transit_events(
    snapshots: Sequence[TransitSnapshot],
) -> List[TransitEvent]:
    """Detect all supported discrete transit events."""
    events: List[TransitEvent] = []

    events.extend(
        detect_sign_changes(
            snapshots
        )
    )

    events.extend(
        detect_retrograde_stations(
            snapshots
        )
    )

    events.sort(
        key=lambda event: (
            event.timestamp,
            event.planet,
            event.event_type,
        )
    )

    return events


# ============================================================
# Convenience Timeline API
# ============================================================

def build_transit_timeline(
    start: datetime,
    end: datetime,
    step_hours: float = DEFAULT_STEP_HOURS,
    planets: Optional[Sequence[str]] = None,
) -> Tuple[
    List[TransitSnapshot],
    List[TransitEvent],
]:
    """
    Build a complete transit timeline.

    Returns:

        (
            snapshots,
            detected_events,
        )
    """
    snapshots = generate_all_transit_timeline(
        start=start,
        end=end,
        step_hours=step_hours,
        planets=planets,
    )

    events = detect_transit_events(
        snapshots
    )

    return snapshots, events


# ============================================================
# Utility Functions
# ============================================================

def planets_present(
    snapshots: Sequence[TransitSnapshot],
) -> Tuple[str, ...]:
    """Return unique planets represented in a timeline."""
    return tuple(
        sorted(
            {
                snapshot.planet
                for snapshot in snapshots
            }
        )
    )


def signs_present(
    snapshots: Sequence[TransitSnapshot],
) -> Tuple[str, ...]:
    """Return unique signs represented in a timeline."""
    return tuple(
        sorted(
            {
                snapshot.sign
                for snapshot in snapshots
            }
        )
    )


def first_snapshot(
    snapshots: Sequence[TransitSnapshot],
    planet: str,
) -> Optional[TransitSnapshot]:
    """Return the earliest snapshot for a planet."""
    matches = filter_planet_snapshots(
        snapshots,
        planet,
    )

    if not matches:
        return None

    return min(
        matches,
        key=lambda item: item.timestamp,
    )


def last_snapshot(
    snapshots: Sequence[TransitSnapshot],
    planet: str,
) -> Optional[TransitSnapshot]:
    """Return the latest snapshot for a planet."""
    matches = filter_planet_snapshots(
        snapshots,
        planet,
    )

    if not matches:
        return None

    return max(
        matches,
        key=lambda item: item.timestamp,
    )


# ============================================================
# Public API
# ============================================================

__all__ = [
    "DEFAULT_STEP_HOURS",
    "ZODIAC_SIGNS",
    "TransitSnapshot",
    "TransitEvent",
    "validate_datetime",
    "validate_step_hours",
    "validate_date_range",
    "validate_planet_name",
    "calculate_planet_transit",
    "snapshot_from_position",
    "generate_planet_transit_timeline",
    "generate_all_transit_timeline",
    "filter_planet_snapshots",
    "filter_retrograde_snapshots",
    "filter_sign_snapshots",
    "detect_sign_changes",
    "detect_retrograde_stations",
    "detect_transit_events",
    "build_transit_timeline",
    "planets_present",
    "signs_present",
    "first_snapshot",
    "last_snapshot",
]