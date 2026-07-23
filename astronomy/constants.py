"""
astronomy/constants.py

Astronomical and Vedic astrology constants.

Version:
    2.1.0

Compatible with Python 3.9
"""

import swisseph as swe

# ==========================================================
# Zodiac
# ==========================================================

ZODIAC_SIGNS = 12

DEGREES_PER_SIGN = 30.0

FULL_CIRCLE = 360.0

# ==========================================================
# Nakshatras
# ==========================================================

TOTAL_NAKSHATRAS = 27

NAKSHATRA_SIZE = FULL_CIRCLE / TOTAL_NAKSHATRAS

PADA_SIZE = NAKSHATRA_SIZE / 4.0

# ==========================================================
# Houses
# ==========================================================

TOTAL_HOUSES = 12

# ==========================================================
# Swiss Ephemeris
# ==========================================================

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
}

# ==========================================================
# Sidereal Mode
# ==========================================================

SIDEREAL_MODE = swe.SIDM_LAHIRI

# ==========================================================
# Swiss Ephemeris Flags
# ==========================================================

CALCULATION_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

# ==========================================================
# Time
# ==========================================================

HOURS_PER_DAY = 24.0

MINUTES_PER_HOUR = 60.0

SECONDS_PER_MINUTE = 60.0
