"""
astronomy/swiss.py

Swiss Ephemeris wrapper for the Kundali Engine.
Compatible with Python 3.9
"""

import swisseph as swe

from config import EPHEMERIS_DIR


class SwissEphemeris:
    """
    Wrapper around pyswisseph.
    """

    def __init__(self):
        self._initialize()

    def _initialize(self):
        """
        Initialize Swiss Ephemeris.
        """

        try:
            swe.set_ephe_path(EPHEMERIS_DIR)
        except Exception:
            pass

        swe.set_sid_mode(swe.SIDM_LAHIRI)

    def julian_day(self, year, month, day, hour):
        """
        Return Julian Day.
        """

        return swe.julday(year, month, day, hour)

    def ayanamsa(self, jd):
        """
        Lahiri Ayanamsa.
        """

        return swe.get_ayanamsa_ut(jd)

    def planet(self, jd, planet_id):
        """
        Calculate one planet.
        """

        result, flag = swe.calc_ut(jd, planet_id, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)

        return result

    def all_planets(self, jd):
        """
        Return all major planets.
        """

        planets = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mercury": swe.MERCURY,
            "Venus": swe.VENUS,
            "Mars": swe.MARS,
            "Jupiter": swe.JUPITER,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE,
        }

        data = {}

        for name, pid in planets.items():
            data[name] = self.planet(jd, pid)

        rahu = data["Rahu"][0]

        ketu = (rahu + 180.0) % 360.0

        data["Ketu"] = (ketu, 0, 0, 0, 0, 0)

        return data
