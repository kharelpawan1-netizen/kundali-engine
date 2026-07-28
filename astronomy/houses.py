"""
astronomy/houses.py

House and Bhava calculations for the Kundali Engine.

The module provides:
    - Whole Sign house construction from the Ascendant.
    - Swiss Ephemeris Bhava cusp calculation.
    - House lookup for a planetary longitude.

The Whole Sign system is kept separate from cusp-based Bhava
calculations so that the two systems are never accidentally mixed.

Python Version:
    3.9+
"""

from __future__ import annotations

from typing import Dict, Tuple

from astronomy.signs import sign_enum
from astronomy.swiss import houses as swiss_houses
from models.house import House


def normalize_longitude(longitude: float) -> float:
    """
    Normalize longitude into the interval [0, 360).

    Parameters
    ----------
    longitude
        Any ecliptic longitude in degrees.

    Returns
    -------
    float
        Normalized longitude.
    """

    return longitude % 360.0


def whole_sign_houses(
    ascendant_longitude: float,
) -> Dict[int, House]:
    """
    Build the twelve Whole Sign houses from the Ascendant.

    The Ascendant's zodiac sign becomes the first house. Each
    subsequent house advances exactly one zodiac sign.

    Parameters
    ----------
    ascendant_longitude
        Sidereal Ascendant longitude.

    Returns
    -------
    dict[int, House]
        Houses numbered 1 through 12.
    """

    longitude = normalize_longitude(ascendant_longitude)

    ascendant_sign = sign_enum(longitude)
    ascendant_sign_number = ascendant_sign.number

    result: Dict[int, House] = {}

    for house_number in range(1, 13):
        sign_number = ((ascendant_sign_number + house_number - 2) % 12) + 1

        house_longitude = (sign_number - 1) * 30.0

        sign = sign_enum(house_longitude)

        result[house_number] = House(
            number=house_number,
            longitude=house_longitude,
            sign=sign.value,
            sign_number=sign.number,
        )

    return result


def bhava_cusps(
    julian_day: float,
    latitude: float,
    longitude: float,
) -> Tuple[Tuple[float, ...], float]:
    """
    Calculate Swiss Ephemeris Bhava cusps.

    The underlying Swiss Ephemeris wrapper currently uses the
    Placidus house system.

    Parameters
    ----------
    julian_day
        Julian Day in UT.

    latitude
        Geographic latitude.

    longitude
        Geographic longitude.

    Returns
    -------
    tuple
        A tuple containing:

        - twelve normalized cusp longitudes
        - normalized Ascendant longitude
    """

    cusps, ascmc = swiss_houses(
        julian_day,
        latitude,
        longitude,
    )

    normalized_cusps = tuple(normalize_longitude(float(cusp)) for cusp in cusps)

    ascendant = normalize_longitude(float(ascmc[0]))

    return normalized_cusps, ascendant


def cusp_houses(
    julian_day: float,
    latitude: float,
    longitude: float,
) -> Dict[int, House]:
    """
    Build House objects from Swiss Ephemeris cusps.

    Parameters
    ----------
    julian_day
        Julian Day in UT.

    latitude
        Geographic latitude.

    longitude
        Geographic longitude.

    Returns
    -------
    dict[int, House]
        Twelve cusp-based houses.
    """

    cusps, _ = bhava_cusps(
        julian_day,
        latitude,
        longitude,
    )

    result: Dict[int, House] = {}

    for index, cusp in enumerate(cusps, start=1):
        sign = sign_enum(cusp)

        result[index] = House(
            number=index,
            longitude=cusp,
            sign=sign.value,
            sign_number=sign.number,
        )

    return result


def house_from_longitude(
    longitude: float,
    houses: Dict[int, House],
) -> int:
    """
    Determine which house contains a longitude.

    The function uses the supplied house cusp longitudes and
    correctly handles the 360° → 0° wraparound.

    Parameters
    ----------
    longitude
        Sidereal longitude.

    houses
        Dictionary containing houses 1 through 12.

    Returns
    -------
    int
        House number containing the longitude.

    Raises
    ------
    ValueError
        If the house mapping does not contain all twelve houses.
    """

    if set(houses) != set(range(1, 13)):
        raise ValueError("houses must contain exactly houses 1 through 12")

    longitude = normalize_longitude(longitude)

    cusps = [normalize_longitude(houses[number].longitude) for number in range(1, 13)]

    for index in range(12):
        current = cusps[index]
        next_cusp = cusps[(index + 1) % 12]

        if index == 11:
            if longitude >= current or longitude < next_cusp:
                return 12
        elif current <= next_cusp:
            if current <= longitude < next_cusp:
                return index + 1
        else:
            if longitude >= current or longitude < next_cusp:
                return index + 1

    # Floating-point boundary fallback.
    return 12


__all__ = [
    "normalize_longitude",
    "whole_sign_houses",
    "bhava_cusps",
    "cusp_houses",
    "house_from_longitude",
]
