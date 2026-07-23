"""
engine.py

Main Horoscope Engine
Compatible with Python 3.9
"""

from astronomy.ascendant import calculate_ascendant
from astronomy.nakshatra import get_nakshatra
from astronomy.signs import get_sign
from astronomy.swiss import SwissEphemeris
from astronomy.timezone import local_to_utc
from models.chart import BirthChart
from models.house import House
from models.planet import Planet


class HoroscopeEngine:
    """
    Main Kundali Engine.
    """

    def __init__(self):
        self.swe = SwissEphemeris()

    def build_chart(self, birth):
        """
        Build complete birth chart.
        """

        # --------------------------------------------
        # Local Time -> UTC
        # --------------------------------------------

        utc_dt = local_to_utc(birth.birth_datetime, birth.location.timezone)

        hour = utc_dt.hour + utc_dt.minute / 60 + utc_dt.second / 3600

        jd = self.swe.julian_day(utc_dt.year, utc_dt.month, utc_dt.day, hour)

        ayanamsa = self.swe.ayanamsa(jd)

        chart = BirthChart(julian_day=jd, ayanamsa=ayanamsa)

        # --------------------------------------------
        # Ascendant
        # --------------------------------------------

        asc = calculate_ascendant(jd, birth.location.latitude, birth.location.longitude)

        asc_longitude = asc["ascendant"]

        chart.ascendant = asc_longitude

        asc_sign, _, _ = get_sign(asc_longitude)

        chart.ascendant_sign = asc_sign

        # --------------------------------------------
        # Whole Sign Houses
        # --------------------------------------------

        asc_sign_number = int(asc_longitude // 30)

        sign_names = [
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
        ]

        for house in range(12):

            sign_index = (asc_sign_number + house) % 12

            start = sign_index * 30.0
            end = start + 30.0

            chart.houses[house + 1] = House(
                number=house + 1,
                sign=sign_names[sign_index],
                start_longitude=start,
                end_longitude=end,
            )

        # --------------------------------------------
        # Planets
        # --------------------------------------------

        raw = self.swe.all_planets(jd)

        for name, values in raw.items():

            longitude = values[0]
            latitude = values[1]
            distance = values[2]
            speed = values[3]

            sign, sign_number, sign_degree = get_sign(longitude)

            nakshatra, pada, lord = get_nakshatra(longitude)

            planet = Planet(
                name=name,
                longitude=longitude,
                latitude=latitude,
                distance=distance,
                speed=speed,
                retrograde=speed < 0,
                sign=sign,
                sign_number=sign_number,
                sign_degree=sign_degree,
                nakshatra=nakshatra,
                pada=pada,
                nakshatra_lord=lord,
            )

            # ----------------------------------------
            # Planet House (Whole Sign)
            # ----------------------------------------

            house_number = ((sign_number - asc_sign_number) % 12) + 1

            planet.house = house_number

            chart.planets[name] = planet

        return chart
