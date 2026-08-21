"""
astrology/transit_aspects.py

Transit-to-natal planetary aspect engine.

This module calculates geometric relationships between transiting
planets and natal planets using geocentric ecliptic longitudes.

Supported major aspects:

    Conjunction   0°
    Sextile      60°
    Square       90°
    Trine       120°
    Opposition  180°

The engine provides:

    - Exact angular separation
    - Nearest aspect
    - Orb
    - Applying/separating status when transit speed is available
    - Transit and natal planetary metadata
    - Configurable aspect orbs
    - Exact aspect detection
    - Multiple transit-to-natal aspect calculation

This module intentionally focuses on astronomical geometry.

It does not interpret:
    - Planetary benefic/malefic nature
    - House lordship
    - Yogas
    - Dasha effects
    - Gochara results
    - Ashtakavarga
    - Predictive outcomes

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


# ============================================================
# Constants
# ============================================================

ASPECT_ANGLES: Mapping[str, float] = {
    "Conjunction": 0.0,
    "Sextile": 60.0,
    "Square": 90.0,
    "Trine": 120.0,
    "Opposition": 180.0,
}

DEFAULT_ASPECT_ORBS: Mapping[str, float] = {
    "Conjunction": 8.0,
    "Sextile": 6.0,
    "Square": 7.0,
    "Trine": 7.0,
    "Opposition": 8.0,
}

# Classical planetary sequence used elsewhere in the engine.
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


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class AspectDefinition:
    """Definition of one planetary aspect."""

    name: str
    angle: float
    orb: float


@dataclass(frozen=True)
class TransitAspect:
    """
    One transit-to-natal planetary aspect.

    Attributes:
        transit_planet:
            Planet currently transiting the zodiac.

        natal_planet:
            Planet in the natal chart.

        transit_longitude:
            Transit longitude in degrees [0, 360).

        natal_longitude:
            Natal longitude in degrees [0, 360).

        separation:
            Smallest angular separation between the two planets.

        aspect:
            Aspect name, e.g. Conjunction or Trine.

        exact_angle:
            Canonical angle of the detected aspect.

        orb:
            Absolute difference between separation and exact angle.

        applying:
            True when the transit is moving toward exactness.

        separating:
            True when the transit is moving away from exactness.

        exact:
            True when the aspect is effectively exact.

        transit_retrograde:
            Retrograde state of the transiting planet when available.
    """

    transit_planet: str
    natal_planet: str
    transit_longitude: float
    natal_longitude: float
    separation: float
    aspect: str
    exact_angle: float
    orb: float
    applying: bool
    separating: bool
    exact: bool
    transit_retrograde: bool = False

    @property
    def aspect_key(self) -> str:
        """Return a normalized aspect identifier."""
        return self.aspect.lower().replace(" ", "_")

    @property
    def within_orb(self) -> bool:
        """Return True because TransitAspect represents a detected aspect."""
        return True


# ============================================================
# Longitude Utilities
# ============================================================

def normalize_longitude(longitude: float) -> float:
    """
    Normalize an ecliptic longitude to [0, 360).

    Example:
        361.0 -> 1.0
        -1.0  -> 359.0
    """
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be numeric.")

    return float(longitude) % 360.0


def validate_longitude(longitude: float) -> float:
    """Validate and normalize a planetary longitude."""
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be numeric.")

    if not 0.0 <= float(longitude) <= 360.0:
        raise ValueError(
            "Longitude must be between 0 and 360 degrees."
        )

    if float(longitude) == 360.0:
        return 0.0

    return normalize_longitude(float(longitude))


def angular_separation(
    longitude_a: float,
    longitude_b: float,
) -> float:
    """
    Return the smallest angular separation between two longitudes.

    Result:
        0 <= separation <= 180
    """
    a = validate_longitude(longitude_a)
    b = validate_longitude(longitude_b)

    difference = abs(a - b)

    return min(
        difference,
        360.0 - difference,
    )


def signed_angular_difference(
    longitude_a: float,
    longitude_b: float,
) -> float:
    """
    Return the signed shortest angular difference.

    Result:
        -180 <= difference <= 180

    Positive values represent counter-clockwise separation
    from longitude_b toward longitude_a.
    """
    a = validate_longitude(longitude_a)
    b = validate_longitude(longitude_b)

    difference = (a - b) % 360.0

    if difference > 180.0:
        difference -= 360.0

    return difference


# ============================================================
# Aspect Definitions
# ============================================================

def aspect_definitions(
    orbs: Optional[Mapping[str, float]] = None,
) -> Tuple[AspectDefinition, ...]:
    """
    Return validated aspect definitions.

    Custom orbs may override the default values.
    """
    selected_orbs: Dict[str, float] = dict(
        DEFAULT_ASPECT_ORBS
    )

    if orbs is not None:
        for name, value in orbs.items():
            if name not in ASPECT_ANGLES:
                raise ValueError(
                    f"Unknown aspect: {name}"
                )

            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Orb for {name} must be numeric."
                )

            if value < 0:
                raise ValueError(
                    f"Orb for {name} cannot be negative."
                )

            selected_orbs[name] = float(value)

    return tuple(
        AspectDefinition(
            name=name,
            angle=angle,
            orb=selected_orbs[name],
        )
        for name, angle in ASPECT_ANGLES.items()
    )


def aspect_angle(aspect: str) -> float:
    """Return the canonical angle for an aspect."""
    try:
        return ASPECT_ANGLES[aspect]
    except KeyError as exc:
        raise ValueError(
            f"Unknown aspect: {aspect}"
        ) from exc


def aspect_orb(
    aspect: str,
    orbs: Optional[Mapping[str, float]] = None,
) -> float:
    """Return the configured orb for an aspect."""
    if aspect not in ASPECT_ANGLES:
        raise ValueError(
            f"Unknown aspect: {aspect}"
        )

    if orbs is None:
        return DEFAULT_ASPECT_ORBS[aspect]

    value = orbs.get(
        aspect,
        DEFAULT_ASPECT_ORBS[aspect],
    )

    if not isinstance(value, (int, float)):
        raise TypeError(
            f"Orb for {aspect} must be numeric."
        )

    if value < 0:
        raise ValueError(
            f"Orb for {aspect} cannot be negative."
        )

    return float(value)


# ============================================================
# Aspect Detection
# ============================================================

def aspect_orb_difference(
    separation: float,
    aspect: str,
) -> float:
    """
    Return the absolute distance from an aspect's exact angle.
    """
    if not 0.0 <= separation <= 180.0:
        raise ValueError(
            "Separation must be between 0 and 180 degrees."
        )

    return abs(
        separation - aspect_angle(aspect)
    )


def detect_aspect(
    longitude_a: float,
    longitude_b: float,
    orbs: Optional[Mapping[str, float]] = None,
) -> Optional[Tuple[str, float, float]]:
    """
    Detect the closest configured aspect.

    Returns:
        (aspect_name, exact_angle, orb)

    or:
        None when no configured aspect falls within its orb.

    When multiple aspects theoretically overlap because of very
    large custom orbs, the aspect with the smallest orb difference
    is selected.
    """
    separation = angular_separation(
        longitude_a,
        longitude_b,
    )

    candidates: List[
        Tuple[str, float, float]
    ] = []

    for definition in aspect_definitions(orbs):
        difference = abs(
            separation - definition.angle
        )

        if difference <= definition.orb:
            candidates.append(
                (
                    definition.name,
                    definition.angle,
                    difference,
                )
            )

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item[2]
    )

    return candidates[0]


# ============================================================
# Applying / Separating
# ============================================================

def determine_motion_state(
    current_separation: float,
    exact_angle: float,
    previous_separation: Optional[float] = None,
    next_separation: Optional[float] = None,
) -> Tuple[bool, bool]:
    """
    Determine whether an aspect is applying or separating.

    Preferred input:
        previous_separation
        next_separation

    The function compares the distance from exactness.

    Applying:
        next position is closer to exactness.

    Separating:
        next position is farther from exactness.

    If no neighboring measurement is supplied, both values
    are False because motion cannot be established safely.
    """
    if not 0.0 <= current_separation <= 180.0:
        raise ValueError(
            "current_separation must be between 0 and 180 degrees."
        )

    if not 0.0 <= exact_angle <= 180.0:
        raise ValueError(
            "exact_angle must be between 0 and 180 degrees."
        )

    if previous_separation is None and next_separation is None:
        return False, False

    current_distance = abs(
        current_separation - exact_angle
    )

    if next_separation is not None:
        if not 0.0 <= next_separation <= 180.0:
            raise ValueError(
                "next_separation must be between 0 and 180 degrees."
            )

        next_distance = abs(
            next_separation - exact_angle
        )

        if next_distance < current_distance:
            return True, False

        if next_distance > current_distance:
            return False, True

        return False, False

    if previous_separation is not None:
        if not 0.0 <= previous_separation <= 180.0:
            raise ValueError(
                "previous_separation must be between 0 and 180 degrees."
            )

        previous_distance = abs(
            previous_separation - exact_angle
        )

        if current_distance < previous_distance:
            return True, False

        if current_distance > previous_distance:
            return False, True

    return False, False


def determine_motion_from_longitudes(
    current_transit_longitude: float,
    natal_longitude: float,
    transit_longitude_delta: float,
    exact_angle: float,
) -> Tuple[bool, bool]:
    """
    Determine applying/separating status from a transit longitude delta.

    Args:
        current_transit_longitude:
            Current transit longitude.

        natal_longitude:
            Fixed natal longitude.

        transit_longitude_delta:
            Expected transit longitude movement over a small
            future interval, in degrees.

        exact_angle:
            Exact aspect angle.

    Returns:
        (applying, separating)

    This uses the geometric separation before and after the
    projected transit movement.
    """
    current = angular_separation(
        current_transit_longitude,
        natal_longitude,
    )

    future = angular_separation(
        current_transit_longitude
        + transit_longitude_delta,
        natal_longitude,
    )

    return determine_motion_state(
        current_separation=current,
        exact_angle=exact_angle,
        next_separation=future,
    )


# ============================================================
# Individual Transit Aspect
# ============================================================

def calculate_transit_aspect(
    transit_planet: str,
    transit_longitude: float,
    natal_planet: str,
    natal_longitude: float,
    *,
    transit_retrograde: bool = False,
    transit_longitude_delta: Optional[float] = None,
    orbs: Optional[Mapping[str, float]] = None,
    exact_tolerance: float = 0.1,
) -> Optional[TransitAspect]:
    """
    Calculate one transit-to-natal planetary aspect.

    Returns None when no configured aspect is within orb.
    """
    if not isinstance(transit_planet, str):
        raise TypeError(
            "transit_planet must be a string."
        )

    if not isinstance(natal_planet, str):
        raise TypeError(
            "natal_planet must be a string."
        )

    if not transit_planet.strip():
        raise ValueError(
            "transit_planet cannot be empty."
        )

    if not natal_planet.strip():
        raise ValueError(
            "natal_planet cannot be empty."
        )

    if exact_tolerance < 0:
        raise ValueError(
            "exact_tolerance cannot be negative."
        )

    transit_longitude = validate_longitude(
        transit_longitude
    )

    natal_longitude = validate_longitude(
        natal_longitude
    )

    detected = detect_aspect(
        transit_longitude,
        natal_longitude,
        orbs,
    )

    if detected is None:
        return None

    name, exact_angle, orb = detected

    applying = False
    separating = False

    if transit_longitude_delta is not None:
        applying, separating = (
            determine_motion_from_longitudes(
                current_transit_longitude=transit_longitude,
                natal_longitude=natal_longitude,
                transit_longitude_delta=transit_longitude_delta,
                exact_angle=exact_angle,
            )
        )

    exact = orb <= exact_tolerance

    return TransitAspect(
        transit_planet=transit_planet,
        natal_planet=natal_planet,
        transit_longitude=transit_longitude,
        natal_longitude=natal_longitude,
        separation=angular_separation(
            transit_longitude,
            natal_longitude,
        ),
        aspect=name,
        exact_angle=exact_angle,
        orb=orb,
        applying=applying,
        separating=separating,
        exact=exact,
        transit_retrograde=bool(
            transit_retrograde
        ),
    )


# ============================================================
# Bulk Transit Aspect Calculation
# ============================================================

def calculate_transit_aspects(
    transit_planets: Mapping[str, float],
    natal_planets: Mapping[str, float],
    *,
    transit_retrogrades: Optional[
        Mapping[str, bool]
    ] = None,
    transit_longitude_deltas: Optional[
        Mapping[str, float]
    ] = None,
    orbs: Optional[Mapping[str, float]] = None,
    exact_tolerance: float = 0.1,
    include_same_planet: bool = True,
) -> List[TransitAspect]:
    """
    Calculate all configured transit-to-natal aspects.

    Args:
        transit_planets:
            Mapping of planet name -> transit longitude.

        natal_planets:
            Mapping of planet name -> natal longitude.

        transit_retrogrades:
            Optional mapping of planet name -> retrograde state.

        transit_longitude_deltas:
            Optional mapping of planet name -> projected longitude
            movement over a small future interval.

        orbs:
            Optional aspect-specific orb overrides.

        exact_tolerance:
            Maximum orb considered exact.

        include_same_planet:
            If False, transit Sun -> natal Sun, etc. are excluded.

    Returns:
        List of TransitAspect objects sorted by:

            1. transit planet
            2. natal planet
            3. orb
    """
    if not isinstance(transit_planets, Mapping):
        raise TypeError(
            "transit_planets must be a mapping."
        )

    if not isinstance(natal_planets, Mapping):
        raise TypeError(
            "natal_planets must be a mapping."
        )

    retrogrades = (
        transit_retrogrades or {}
    )

    deltas = (
        transit_longitude_deltas or {}
    )

    aspects: List[TransitAspect] = []

    for transit_planet, transit_longitude in (
        transit_planets.items()
    ):
        for natal_planet, natal_longitude in (
            natal_planets.items()
        ):
            if (
                not include_same_planet
                and transit_planet == natal_planet
            ):
                continue

            aspect = calculate_transit_aspect(
                transit_planet=transit_planet,
                transit_longitude=transit_longitude,
                natal_planet=natal_planet,
                natal_longitude=natal_longitude,
                transit_retrograde=bool(
                    retrogrades.get(
                        transit_planet,
                        False,
                    )
                ),
                transit_longitude_delta=deltas.get(
                    transit_planet
                ),
                orbs=orbs,
                exact_tolerance=exact_tolerance,
            )

            if aspect is not None:
                aspects.append(aspect)

    aspects.sort(
        key=lambda item: (
            item.transit_planet,
            item.natal_planet,
            item.orb,
        )
    )

    return aspects


# ============================================================
# Convenience Queries
# ============================================================

def strongest_aspects(
    aspects: Iterable[TransitAspect],
    limit: Optional[int] = None,
) -> List[TransitAspect]:
    """
    Return aspects ordered by smallest orb.
    """
    result = sorted(
        list(aspects),
        key=lambda item: item.orb,
    )

    if limit is not None:
        if limit < 0:
            raise ValueError(
                "limit cannot be negative."
            )

        result = result[:limit]

    return result


def exact_aspects(
    aspects: Iterable[TransitAspect],
    tolerance: float = 0.1,
) -> List[TransitAspect]:
    """Return aspects whose orb is within tolerance."""
    if tolerance < 0:
        raise ValueError(
            "tolerance cannot be negative."
        )

    return [
        aspect
        for aspect in aspects
        if aspect.orb <= tolerance
    ]


def applying_aspects(
    aspects: Iterable[TransitAspect],
) -> List[TransitAspect]:
    """Return currently applying aspects."""
    return [
        aspect
        for aspect in aspects
        if aspect.applying
    ]


def separating_aspects(
    aspects: Iterable[TransitAspect],
) -> List[TransitAspect]:
    """Return currently separating aspects."""
    return [
        aspect
        for aspect in aspects
        if aspect.separating
    ]


def aspects_for_transit_planet(
    aspects: Iterable[TransitAspect],
    transit_planet: str,
) -> List[TransitAspect]:
    """Return aspects involving one transiting planet."""
    return [
        aspect
        for aspect in aspects
        if aspect.transit_planet == transit_planet
    ]


def aspects_to_natal_planet(
    aspects: Iterable[TransitAspect],
    natal_planet: str,
) -> List[TransitAspect]:
    """Return aspects directed toward one natal planet."""
    return [
        aspect
        for aspect in aspects
        if aspect.natal_planet == natal_planet
    ]


# ============================================================
# Public API
# ============================================================

__all__ = [
    "ASPECT_ANGLES",
    "DEFAULT_ASPECT_ORBS",
    "PLANET_NAMES",
    "AspectDefinition",
    "TransitAspect",
    "normalize_longitude",
    "validate_longitude",
    "angular_separation",
    "signed_angular_difference",
    "aspect_definitions",
    "aspect_angle",
    "aspect_orb",
    "aspect_orb_difference",
    "detect_aspect",
    "determine_motion_state",
    "determine_motion_from_longitudes",
    "calculate_transit_aspect",
    "calculate_transit_aspects",
    "strongest_aspects",
    "exact_aspects",
    "applying_aspects",
    "separating_aspects",
    "aspects_for_transit_planet",
    "aspects_to_natal_planet",
]