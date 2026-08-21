"""
astrology/transits.py

Vedic sidereal planetary transit calculation engine.

This module calculates current/transit planetary positions using
Swiss Ephemeris and Lahiri ayanamsa, and provides utilities for:

    - Sidereal transit longitudes
    - Zodiac sign and degree
    - Nakshatra and Pada
    - Retrograde status
    - Transit-to-natal planetary relationships
    - Transit house placement from the natal Ascendant
    - Transit aspect detection using classical Parashari
      graha drishti rules

The module is intentionally independent of the Dasha hierarchy.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import swisseph as swe

from astrology.dasha import (
    NAKSHATRA_NAMES,
    NAKSHATRA_SPAN,
    nakshatra_index,
    nakshatra_lord,
)


# ============================================================
# Constants
# ============================================================

SIDEREAL_YEAR_DAYS = 365.2568983

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

PLANET_IDS: Dict[str, int] = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
}

# Ketu is always 180 degrees from Rahu.
TRANSIT_PLANETS: Tuple[str, ...] = (
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

# Classical Parashari graha drishti.
#
# Every planet aspects the 7th from itself.
# Mars additionally aspects 4th and 8th.
# Jupiter additionally aspects 5th and 9th.
# Saturn additionally aspects 3rd and 10th.
#
# Rahu/Ketu are deliberately excluded from special
# Parashari aspects here. Their treatment varies among
# traditions, so the module keeps their default 7th aspect.
GRAHA_ASPECTS: Dict[str, Tuple[int, ...]] = {
    "Sun": (7,),
    "Moon": (7,),
    "Mars": (4, 7, 8),
    "Mercury": (7,),
    "Jupiter": (5, 7, 9),
    "Venus": (7,),
    "Saturn": (3, 7, 10),
    "Rahu": (7,),
    "Ketu": (7,),
}


# ============================================================
# Data Models
# ============================================================

@dataclass(frozen=True)
class TransitPosition:
    """Sidereal position of one transiting planet."""

    planet: str
    longitude: float
    sign: str
    sign_number: int
    degree_in_sign: float
    nakshatra: str
    nakshatra_number: int
    pada: int
    nakshatra_lord: str
    retrograde: bool
    datetime: datetime

    @property
    def sign_index(self) -> int:
        """Return zero-based zodiac sign index."""
        return self.sign_number - 1


@dataclass(frozen=True)
class TransitAspect:
    """A Parashari graha-drishti relationship."""

    transit_planet: str
    natal_planet: str
    transit_house: int
    natal_house: int
    aspect_house_distance: int


@dataclass(frozen=True)
class TransitToNatal:
    """Relationship between one transit planet and one natal planet."""

    transit_planet: str
    natal_planet: str
    transit_longitude: float
    natal_longitude: float
    angular_distance: float
    applying: bool


# ============================================================
# Validation
# ============================================================

def validate_datetime(moment: datetime) -> datetime:
    """Validate a datetime input."""
    if not isinstance(moment, datetime):
        raise TypeError("moment must be a datetime.")

    return moment


def validate_longitude(longitude: float) -> float:
    """Validate and normalize a planetary longitude."""
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be numeric.")

    if not 0.0 <= longitude <= 360.0:
        raise ValueError(
            "Longitude must be between 0 and 360 degrees."
        )

    if longitude == 360.0:
        return 0.0

    return longitude % 360.0


def validate_planet(planet: str) -> str:
    """Validate a supported transit planet."""
    if planet not in TRANSIT_PLANETS:
        raise ValueError(
            f"Unsupported transit planet: {planet}"
        )

    return planet


# ============================================================
# Zodiac Utilities
# ============================================================

def zodiac_sign_index(longitude: float) -> int:
    """Return zero-based zodiac sign index."""
    longitude = validate_longitude(longitude)

    index = int(longitude / 30.0)

    return min(index, 11)


def zodiac_sign_number(longitude: float) -> int:
    """Return zodiac sign number from 1 to 12."""
    return zodiac_sign_index(longitude) + 1


def zodiac_sign(longitude: float) -> str:
    """Return the sidereal zodiac sign."""
    return ZODIAC_SIGNS[zodiac_sign_index(longitude)]


def degree_in_sign(longitude: float) -> float:
    """Return degree within the current zodiac sign."""
    longitude = validate_longitude(longitude)

    return longitude % 30.0


def longitude_difference(
    longitude_a: float,
    longitude_b: float,
) -> float:
    """
    Return the smallest absolute angular distance.

    Result:
        0 <= distance <= 180
    """
    a = validate_longitude(longitude_a)
    b = validate_longitude(longitude_b)

    difference = abs(a - b)

    return min(difference, 360.0 - difference)


# ============================================================
# Nakshatra Utilities
# ============================================================

def transit_nakshatra(longitude: float) -> str:
    """Return the Nakshatra for a sidereal longitude."""
    return NAKSHATRA_NAMES[nakshatra_index(longitude)]


def transit_nakshatra_number(longitude: float) -> int:
    """Return Nakshatra number from 1 to 27."""
    return nakshatra_index(longitude) + 1


def transit_nakshatra_pada(longitude: float) -> int:
    """
    Return Nakshatra Pada from 1 to 4.

    Each Nakshatra spans four equal Padas.
    """
    longitude = validate_longitude(longitude)

    position = longitude % NAKSHATRA_SPAN

    pada_span = NAKSHATRA_SPAN / 4.0

    pada = int(position / pada_span) + 1

    return min(pada, 4)


# ============================================================
# Julian Day
# ============================================================

def datetime_to_julian_day(moment: datetime) -> float:
    """
    Convert datetime to Julian Day.

    Swiss Ephemeris expects UT.

    Naive datetimes are interpreted as UTC.
    Timezone-aware datetimes are converted to UTC.
    """
    moment = validate_datetime(moment)

    if moment.tzinfo is not None:
        utc = moment.astimezone(
            __import__("datetime").timezone.utc
        )
    else:
        utc = moment

    hour = (
        utc.hour
        + utc.minute / 60.0
        + utc.second / 3600.0
        + utc.microsecond / 3600000000.0
    )

    return swe.julday(
        utc.year,
        utc.month,
        utc.day,
        hour,
        swe.GREG_CAL,
    )


# ============================================================
# Swiss Ephemeris
# ============================================================

def configure_sidereal_mode() -> None:
    """Configure Swiss Ephemeris for Lahiri sidereal calculations."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)


def calculate_sidereal_longitude(
    planet: str,
    moment: datetime,
) -> float:
    """
    Calculate the Lahiri sidereal longitude of a planet.

    Rahu uses the Swiss Ephemeris True Node.

    Ketu is calculated as the point exactly opposite Rahu.
    """
    validate_planet(planet)
    moment = validate_datetime(moment)

    configure_sidereal_mode()

    if planet == "Ketu":
        rahu_longitude = calculate_sidereal_longitude(
            "Rahu",
            moment,
        )

        return (rahu_longitude + 180.0) % 360.0

    planet_id = PLANET_IDS[planet]

    julian_day = datetime_to_julian_day(moment)

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    result, _ = swe.calc_ut(
        julian_day,
        planet_id,
        flags,
    )

    longitude = result[0]

    return validate_longitude(longitude)


# ============================================================
# Retrograde
# ============================================================

def calculate_retrograde(
    planet: str,
    moment: datetime,
) -> bool:
    """
    Determine whether a planet is retrograde.

    Retrograde status is based on the Swiss Ephemeris
    longitudinal speed.

    Sun and Moon are normally direct.
    """
    validate_planet(planet)
    moment = validate_datetime(moment)

    if planet in ("Sun", "Moon"):
        return False

    configure_sidereal_mode()

    if planet == "Ketu":
        return calculate_retrograde(
            "Rahu",
            moment,
        )

    julian_day = datetime_to_julian_day(moment)

    planet_id = PLANET_IDS[planet]

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    result, _ = swe.calc_ut(
        julian_day,
        planet_id,
        flags,
    )

    speed = result[3]

    return speed < 0.0


# ============================================================
# Transit Position
# ============================================================

def calculate_transit_position(
    planet: str,
    moment: datetime,
) -> TransitPosition:
    """Calculate a complete sidereal transit position."""
    validate_planet(planet)
    moment = validate_datetime(moment)

    longitude = calculate_sidereal_longitude(
        planet,
        moment,
    )

    sign_number = zodiac_sign_number(longitude)

    return TransitPosition(
        planet=planet,
        longitude=longitude,
        sign=zodiac_sign(longitude),
        sign_number=sign_number,
        degree_in_sign=degree_in_sign(longitude),
        nakshatra=transit_nakshatra(longitude),
        nakshatra_number=transit_nakshatra_number(
            longitude
        ),
        pada=transit_nakshatra_pada(longitude),
        nakshatra_lord=nakshatra_lord(longitude),
        retrograde=calculate_retrograde(
            planet,
            moment,
        ),
        datetime=moment,
    )


def calculate_all_transits(
    moment: datetime,
) -> List[TransitPosition]:
    """
    Calculate transit positions for all supported planets.

    Order:
        Sun, Moon, Mars, Mercury, Jupiter,
        Venus, Saturn, Rahu, Ketu
    """
    moment = validate_datetime(moment)

    return [
        calculate_transit_position(
            planet,
            moment,
        )
        for planet in TRANSIT_PLANETS
    ]


def transit_map(
    moment: datetime,
) -> Dict[str, TransitPosition]:
    """Return all transit positions indexed by planet."""
    positions = calculate_all_transits(moment)

    return {
        position.planet: position
        for position in positions
    }


# ============================================================
# Transit House Placement
# ============================================================

def transit_house_from_ascendant(
    transit_longitude: float,
    ascendant_longitude: float,
) -> int:
    """
    Calculate the whole-sign house occupied by a transit.

    The natal Ascendant sign is treated as the first house.
    """
    transit_sign = zodiac_sign_index(
        transit_longitude
    )

    ascendant_sign = zodiac_sign_index(
        ascendant_longitude
    )

    return (
        (transit_sign - ascendant_sign) % 12
    ) + 1


def transit_house_map(
    moment: datetime,
    ascendant_longitude: float,
) -> Dict[str, int]:
    """
    Return whole-sign transit houses for all planets.
    """
    positions = calculate_all_transits(moment)

    return {
        position.planet: transit_house_from_ascendant(
            position.longitude,
            ascendant_longitude,
        )
        for position in positions
    }


# ============================================================
# Transit-to-Natal Relationships
# ============================================================

def transit_to_natal(
    transit_longitude: float,
    natal_longitude: float,
) -> TransitToNatal:
    """
    Calculate the angular relationship between transit
    and natal positions.

    'applying' is determined by comparing the current
    angular distance with a one-day forward distance.
    """
    transit_longitude = validate_longitude(
        transit_longitude
    )
    natal_longitude = validate_longitude(
        natal_longitude
    )

    distance = longitude_difference(
        transit_longitude,
        natal_longitude,
    )

    return TransitToNatal(
        transit_planet="Transit",
        natal_planet="Natal",
        transit_longitude=transit_longitude,
        natal_longitude=natal_longitude,
        angular_distance=distance,
        applying=False,
    )


def transit_natal_relationship(
    transit_planet: str,
    transit_moment: datetime,
    natal_planet: str,
    natal_longitude: float,
) -> TransitToNatal:
    """
    Calculate the current transit-to-natal angular relationship.
    """
    validate_planet(transit_planet)

    transit_moment = validate_datetime(
        transit_moment
    )

    transit_longitude = calculate_sidereal_longitude(
        transit_planet,
        transit_moment,
    )

    one_day_longitude = calculate_sidereal_longitude(
        transit_planet,
        transit_moment
        + __import__("datetime").timedelta(days=1),
    )

    current_distance = longitude_difference(
        transit_longitude,
        natal_longitude,
    )

    next_distance = longitude_difference(
        one_day_longitude,
        natal_longitude,
    )

    return TransitToNatal(
        transit_planet=transit_planet,
        natal_planet=natal_planet,
        transit_longitude=transit_longitude,
        natal_longitude=validate_longitude(
            natal_longitude
        ),
        angular_distance=current_distance,
        applying=next_distance < current_distance,
    )


# ============================================================
# Parashari Graha Drishti
# ============================================================

def aspect_house_distance(
    transit_house: int,
    natal_house: int,
) -> int:
    """
    Return the inclusive house distance from transit house
    to natal house.

    Example:
        transit house 1 -> natal house 7 = 7th aspect
        transit house 10 -> natal house 12 = 3rd aspect
    """
    if not 1 <= transit_house <= 12:
        raise ValueError(
            "transit_house must be between 1 and 12."
        )

    if not 1 <= natal_house <= 12:
        raise ValueError(
            "natal_house must be between 1 and 12."
        )

    return (
        (natal_house - transit_house) % 12
    ) + 1


def planet_aspects_house(
    planet: str,
    transit_house: int,
    natal_house: int,
) -> bool:
    """Return whether a transit planet aspects a natal house."""
    validate_planet(planet)

    distance = aspect_house_distance(
        transit_house,
        natal_house,
    )

    return distance in GRAHA_ASPECTS[planet]


def calculate_transit_aspects(
    moment: datetime,
    ascendant_longitude: float,
    natal_planet_longitudes: Dict[str, float],
) -> List[TransitAspect]:
    """
    Calculate Parashari transit graha drishti relationships.

    natal_planet_longitudes must map planet names to their
    sidereal natal longitudes.
    """
    moment = validate_datetime(moment)

    transit_houses = transit_house_map(
        moment,
        ascendant_longitude,
    )

    aspects: List[TransitAspect] = []

    for natal_planet, natal_longitude in (
        natal_planet_longitudes.items()
    ):
        validate_longitude(natal_longitude)

        natal_house = transit_house_from_ascendant(
            natal_longitude,
            ascendant_longitude,
        )

        for transit_planet, transit_house in (
            transit_houses.items()
        ):
            distance = aspect_house_distance(
                transit_house,
                natal_house,
            )

            if distance in GRAHA_ASPECTS[
                transit_planet
            ]:
                aspects.append(
                    TransitAspect(
                        transit_planet=transit_planet,
                        natal_planet=natal_planet,
                        transit_house=transit_house,
                        natal_house=natal_house,
                        aspect_house_distance=distance,
                    )
                )

    return aspects


# ============================================================
# Transit Summary
# ============================================================

def build_transit_summary(
    moment: datetime,
    ascendant_longitude: Optional[float] = None,
) -> Dict[str, object]:
    """
    Build a structured transit summary.

    If ascendant_longitude is supplied, whole-sign transit
    houses are included.
    """
    moment = validate_datetime(moment)

    positions = calculate_all_transits(moment)

    summary: Dict[str, object] = {
        "datetime": moment,
        "transits": positions,
    }

    if ascendant_longitude is not None:
        summary["houses"] = transit_house_map(
            moment,
            ascendant_longitude,
        )

    return summary


# ============================================================
# Public API
# ============================================================

__all__ = [
    "SIDEREAL_YEAR_DAYS",
    "ZODIAC_SIGNS",
    "PLANET_IDS",
    "TRANSIT_PLANETS",
    "GRAHA_ASPECTS",
    "TransitPosition",
    "TransitAspect",
    "TransitToNatal",
    "validate_datetime",
    "validate_longitude",
    "validate_planet",
    "zodiac_sign_index",
    "zodiac_sign_number",
    "zodiac_sign",
    "degree_in_sign",
    "longitude_difference",
    "transit_nakshatra",
    "transit_nakshatra_number",
    "transit_nakshatra_pada",
    "datetime_to_julian_day",
    "configure_sidereal_mode",
    "calculate_sidereal_longitude",
    "calculate_retrograde",
    "calculate_transit_position",
    "calculate_all_transits",
    "transit_map",
    "transit_house_from_ascendant",
    "transit_house_map",
    "transit_to_natal",
    "transit_natal_relationship",
    "aspect_house_distance",
    "planet_aspects_house",
    "calculate_transit_aspects",
    "build_transit_summary",
]