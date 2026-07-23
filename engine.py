"""
engine.py

Main Horoscope Engine

Version: 1.2.0
Compatible with Python 3.9
"""

from astronomy.timezone import local_to_utc
from astronomy.julian import julian_day

from astronomy.swiss import SwissEphemeris

from astronomy.signs import get_sign
from astronomy.nakshatra import get_nakshatra

from models.chart import BirthChart
from models.planet import Planet


class HoroscopeEngine:
    """
    Main horoscope engine.
    """

    def __init__(self):

        self.swe = SwissEphemeris()

    def build_chart(self, birth_data):
        """
        Generate a BirthChart.
        """

        # -------------------------------------
        # Local Time
        # -------------------------------------

        local_dt = birth_data.birth_datetime

        timezone_name = birth_data.location.timezone

        # -------------------------------------
        # Convert to UTC
        # -------------------------------------

        utc_dt = local_to_utc(
            local_dt,
            timezone_name
        )

        # -------------------------------------
        # Julian Day
        # -------------------------------------

        jd = julian_day(utc_dt)

        # -------------------------------------
        # Create chart
        # -------------------------------------

        chart = BirthChart(

            julian_day=jd,

            ayanamsa=self.swe.ayanamsa(jd)

        )

        # -------------------------------------
        # Calculate planets
        # -------------------------------------

        raw = self.swe.all_planets(jd)

        for name, values in raw.items():

            longitude = values[0]

            latitude = values[1]

            distance = values[2]

            speed = values[3]

            sign, sign_number, sign_degree = get_sign(
                longitude
            )

            nakshatra, pada, lord = get_nakshatra(
                longitude
            )

            planet = Planet(

                name=name,

                longitude=longitude,

                latitude=latitude,

                distance=distance,

                speed=speed,

                retrograde=(speed < 0),

                sign=sign,

                sign_number=sign_number,

                sign_degree=sign_degree,

                nakshatra=nakshatra,

                pada=pada,

                nakshatra_lord=lord

            )

            chart.planets[name] = planet

        return chart