
"""
engine.py

Main Horoscope Engine.

Integrates:
    - Local birth time -> UTC
    - Julian Day calculation
    - Lahiri ayanamsa
    - Ascendant / Lagna
    - Whole Sign houses
    - Navagraha planetary positions
    - Zodiac sign information
    - Nakshatra and pada
    - Planet-to-house assignment

Compatible with Python 3.9
"""

from __future__ import annotations

from astronomy.ascendant import calculate_ascendant
from astronomy.julian import datetime_to_julian
from astronomy.nakshatra import longitude_to_nakshatra, nakshatra_pada
from astronomy.planet_houses import assign_planets_to_houses
from astronomy.planets import calculate_planets
from astronomy.signs import sign_degree, sign_enum
from astronomy.swiss import ayanamsha_value
from astronomy.timezone import local_to_utc
from models.chart import BirthChart
from models.planet import Planet


class HoroscopeEngine:
    """
    Main Kundali calculation engine.

    The engine coordinates the astronomy and astrology modules
    without duplicating their underlying calculations.
    """

    def __init__(self):
        """Initialize the Horoscope Engine."""
        pass

    def build_chart(self, birth):
        """
        Build a complete birth chart.

        Parameters
        ----------
        birth
            BirthData instance containing the native's birth
            datetime and geographical location.

        Returns
        -------
        BirthChart
            Fully populated birth chart.
        """

        # =====================================================
        # 1. LOCAL TIME -> UTC
        # =====================================================

        utc_dt = local_to_utc(
            birth.birth_datetime,
            birth.location.timezone,
        )

        # =====================================================
        # 2. UTC -> JULIAN DAY
        # =====================================================

        jd = datetime_to_julian(utc_dt)

        # =====================================================
        # 3. AYANAMSHA
        # =====================================================

        ayanamsa = ayanamsha_value(jd)

        # =====================================================
        # 4. CREATE BIRTH CHART
        # =====================================================

        chart = BirthChart(
            birth_data=birth,
            julian_day=jd,
            ayanamsa=ayanamsa,
        )

        # =====================================================
        # 5. ASCENDANT / LAGNA
        # =====================================================

        ascendant = calculate_ascendant(
            jd,
            birth.location,
        )

        chart.ascendant = ascendant.longitude
        chart.ascendant_sign = ascendant.sign.display_name
        chart.ascendant_degree = ascendant.degree_in_sign

        # =====================================================
        # 6. WHOLE SIGN HOUSES
        # =====================================================

        from astronomy.houses import whole_sign_houses

        houses = whole_sign_houses(
            ascendant.longitude,
        )

        chart.houses = houses

        # =====================================================
        # 7. PLANETARY POSITIONS
        # =====================================================

        positions = calculate_planets(jd)

        planets = []

        for graha, position in positions.items():
            longitude = position.longitude

            # -------------------------------------------------
            # Zodiac sign
            # -------------------------------------------------

            sign = sign_enum(longitude)

            # -------------------------------------------------
            # Degree within sign
            # -------------------------------------------------

            degree = sign_degree(longitude)

            # -------------------------------------------------
            # Nakshatra
            # -------------------------------------------------

            nakshatra = longitude_to_nakshatra(longitude)
            pada = nakshatra_pada(longitude)

            # -------------------------------------------------
            # Planet model
            # -------------------------------------------------

            planet = Planet(
                name=graha.display_name,
                longitude=longitude,
                latitude=position.latitude,
                distance=position.distance,
                speed=position.longitude_speed,
                retrograde=position.retrograde,
                sign=sign.display_name,
                sign_number=sign.number,
                sign_degree=degree,
                nakshatra=nakshatra.name,
                pada=pada,
                nakshatra_lord=nakshatra.lord,
            )

            planets.append(planet)

        # =====================================================
        # 8. PLANET -> HOUSE ASSIGNMENT
        # =====================================================

        planets, houses = assign_planets_to_houses(
            planets,
            houses,
        )

        # =====================================================
        # 9. STORE PLANETS AND HOUSES
        # =====================================================

        chart.planets = {
            planet.name: planet
            for planet in planets
        }

        chart.houses = houses

        # =====================================================
        # 10. RETURN COMPLETE CHART
        # =====================================================

        return chart

