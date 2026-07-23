"""
astronomy/ascendant.py

Ascendant (Lagna) calculations.

Version: 1.3.1
Compatible with Python 3.9
"""

import swisseph as swe


def calculate_ascendant(julian_day, latitude, longitude):
    """
    Calculate Ascendant and Midheaven.

    Parameters
    ----------
    julian_day : float
    latitude : float
    longitude : float

    Returns
    -------
    dict
    """

    cusps, ascmc = swe.houses_ex(
        julian_day, latitude, longitude, b"P", swe.FLG_SIDEREAL
    )

    return {
        "ascendant": ascmc[0] % 360,
        "midheaven": ascmc[1] % 360,
        "cusps": list(cusps),
    }
