"""
Swiss Ephemeris Wrapper

This module is the ONLY module that should import pyswisseph.

Responsibilities
----------------
- Configure Swiss Ephemeris
- Configure Ayanamsha
- Provide safe wrapper functions
- Normalize Swiss Ephemeris API
- Raise project-specific exceptions

All astronomical modules should import this module rather than
calling pyswisseph directly.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

import swisseph as swe

from astronomy.signs import mod360
from models.ephemeris_position import EphemerisPosition
from models.graha import Graha

# ============================================================
# Exceptions
# ============================================================


class SwissEphemerisError(Exception):
    """Base exception for Swiss Ephemeris wrapper."""


class EphemerisNotInitializedError(SwissEphemerisError):
    """Raised when the ephemeris path has not been configured."""


# ============================================================
# Supported Ayanamsha
# ============================================================


class Ayanamsha(Enum):
    """Supported sidereal ayanamsha modes."""

    LAHIRI = swe.SIDM_LAHIRI
    RAMAN = swe.SIDM_RAMAN
    KRISHNAMURTI = swe.SIDM_KRISHNAMURTI
    FAGAN_BRADLEY = swe.SIDM_FAGAN_BRADLEY


# ============================================================
# Internal State
# ============================================================

_EPHEMERIS_PATH: Optional[Path] = None

_CURRENT_AYANAMSHA = Ayanamsha.LAHIRI


# ============================================================
# Public Configuration
# ============================================================


def set_ephemeris_path(path: str | Path) -> None:
    """
    Configure Swiss Ephemeris data path.

    Parameters
    ----------
    path
        Directory containing Swiss Ephemeris files.
    """

    global _EPHEMERIS_PATH

    ephe_path = Path(path).expanduser().resolve()

    if not ephe_path.exists():
        raise FileNotFoundError(ephe_path)

    swe.set_ephe_path(str(ephe_path))

    _EPHEMERIS_PATH = ephe_path


def get_ephemeris_path() -> Optional[Path]:
    """Return the configured ephemeris path."""

    return _EPHEMERIS_PATH


def set_ayanamsha(mode: Ayanamsha) -> None:
    """
    Set the sidereal ayanamsha.

    Parameters
    ----------
    mode
        Desired ayanamsha.
    """

    global _CURRENT_AYANAMSHA

    swe.set_sid_mode(mode.value)

    _CURRENT_AYANAMSHA = mode


def get_ayanamsha() -> Ayanamsha:
    """Return the current ayanamsha."""

    return _CURRENT_AYANAMSHA


# ============================================================
# Swiss Planet Mapping
# ============================================================


_PLANET_MAP = {
    Graha.SUN: swe.SUN,
    Graha.MOON: swe.MOON,
    Graha.MARS: swe.MARS,
    Graha.MERCURY: swe.MERCURY,
    Graha.JUPITER: swe.JUPITER,
    Graha.VENUS: swe.VENUS,
    Graha.SATURN: swe.SATURN,
    Graha.RAHU: swe.MEAN_NODE,
    Graha.KETU: swe.MEAN_NODE,
}


# ============================================================
# Swiss Calculation Flags
# ============================================================

_SWISS_FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL


# ============================================================
# Internal Helpers
# ============================================================


def _require_initialized() -> None:
    """Ensure Swiss Ephemeris has been configured."""

    if _EPHEMERIS_PATH is None:
        raise EphemerisNotInitializedError(
            "Swiss Ephemeris path has not been configured."
        )


# ============================================================
# Planet Longitude
# ============================================================


def planet_position(
    julian_day: float,
    graha: Graha,
) -> EphemerisPosition:
    """
    Compute the sidereal position of a planet.

    Parameters
    ----------
    julian_day
        Julian Day (UT).

    graha
        Planet to compute.

    Returns
    -------
    EphemerisPosition
        Complete astronomical position.
    """

    _require_initialized()

    try:
        swiss_planet = _PLANET_MAP[graha]
    except KeyError as exc:
        raise ValueError(f"Unsupported graha: {graha}") from exc

    result, ret_flag = swe.calc_ut(
        julian_day,
        swiss_planet,
        _SWISS_FLAGS,
    )

    longitude = mod360(result[0])
    latitude = result[1]
    distance = result[2]

    longitude_speed = result[3]
    latitude_speed = result[4]
    distance_speed = result[5]

    # Ketu is always opposite Rahu.
    if graha == Graha.KETU:
        longitude = mod360(longitude + 180.0)

    return EphemerisPosition(
        longitude=longitude,
        latitude=latitude,
        distance=distance,
        longitude_speed=longitude_speed,
        latitude_speed=latitude_speed,
        distance_speed=distance_speed,
        retrograde=longitude_speed < 0,
    )


def planet_longitude(
    julian_day: float,
    graha: Graha,
) -> float:
    """
    Return only the sidereal longitude of a planet.
    """

    return planet_position(
        julian_day,
        graha,
    ).longitude


def houses(
    julian_day: float,
    latitude: float,
    longitude: float,
):
    """
    Compute house cusps and Ascendant using Swiss Ephemeris.

    Parameters
    ----------
    julian_day
        Julian Day (UT).

    latitude
        Geographic latitude.

    longitude
        Geographic longitude.

    Returns
    -------
    tuple
        (cusps, ascmc)
    """

    _require_initialized()

    cusps, ascmc = swe.houses_ex(
        julian_day,
        latitude,
        longitude,
        b"P",
        _SWISS_FLAGS,
    )

    return cusps, ascmc


__all__ = [
    "Ayanamsha",
    "SwissEphemerisError",
    "EphemerisNotInitializedError",
    "set_ephemeris_path",
    "get_ephemeris_path",
    "set_ayanamsha",
    "get_ayanamsha",
    "planet_position",
    "planet_longitude",
    "houses",
]
