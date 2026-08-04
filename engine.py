
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
    - BPHS planetary dignity
    - Planet-to-planet relationships
    - Parashari planetary aspects (Drishti)
    - Vimshottari Mahadasha
    - Vimshottari Antardasha
    - Vimshottari Pratyantardasha
    - Vimshottari Sookshma Dasha
    - Vimshottari Prana Dasha
    - Vimshottari Deha Dasha

Dasha hierarchy:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha
        ↓
    Sookshma Dasha
        ↓
    Prana Dasha
        ↓
    Deha Dasha

Compatible with Python 3.9.
"""

from __future__ import annotations

from astrology.aspects import (
    build_aspect_map,
    planet_aspects_planet,
)

from astrology.dasha import (
    current_antardasha,
    current_mahadasha,
    generate_antardashas,
    generate_mahadashas,
)

from astrology.pratyantardasha import (
    current_pratyantardasha,
    generate_pratyantardashas,
)

from astrology.sookshmadasha import (
    current_sookshmadasha,
    generate_sookshmadashas,
)

from astrology.pranadasha import (
    current_pranadasha,
    generate_pranadashas,
)

from astrology.dehadasha import (
    current_dehadasha,
    generate_dehadashas,
)

from astronomy.ascendant import calculate_ascendant

from astronomy.dignity import (
    is_debilitated,
    is_exalted,
    is_moolatrikona,
    is_own_sign,
)

from astronomy.julian import datetime_to_julian

from astronomy.nakshatra import (
    longitude_to_nakshatra,
    nakshatra_pada,
)

from astronomy.planet_houses import (
    assign_planets_to_houses,
)

from astronomy.planets import calculate_planets

from astronomy.swiss import (
    Ayanamsha,
    ayanamsha_value,
    set_ayanamsha,
    set_ephemeris_path,
)

from astronomy.timezone import local_to_utc

from astronomy.signs import (
    sign_degree,
    sign_enum,
)

from models.chart import BirthChart
from models.planet import Planet


class HoroscopeEngine:
    """
    Main Kundali calculation engine.

    The engine coordinates the astronomy and astrology
    modules without duplicating their underlying
    calculations.
    """

    def __init__(self):
        """Initialize the Horoscope Engine and Swiss Ephemeris."""

        from pathlib import Path

        project_root = Path(__file__).resolve().parent
        ephemeris_path = project_root / "ephe"

        set_ephemeris_path(ephemeris_path)
        set_ayanamsha(Ayanamsha.LAHIRI)

    # =========================================================
    # BUILD COMPLETE BIRTH CHART
    # =========================================================

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

        jd = datetime_to_julian(
            utc_dt
        )

        # =====================================================
        # 3. AYANAMSHA
        # =====================================================

        ayanamsa = ayanamsha_value(
            jd
        )

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

        chart.ascendant = (
            ascendant.longitude
        )

        chart.ascendant_sign = (
            ascendant.sign.display_name
        )

        chart.ascendant_degree = (
            ascendant.degree_in_sign
        )

        # =====================================================
        # 6. WHOLE SIGN HOUSES
        # =====================================================

        from astronomy.houses import (
            whole_sign_houses
        )

        houses = whole_sign_houses(
            ascendant.longitude
        )

        chart.houses = houses

        # =====================================================
        # 7. PLANETARY POSITIONS
        # =====================================================

        positions = calculate_planets(
            jd
        )

        planets = []

        for graha, position in positions.items():

            longitude = position.longitude

            # -------------------------------------------------
            # Zodiac sign
            # -------------------------------------------------

            sign = sign_enum(
                longitude
            )

            # -------------------------------------------------
            # Degree within sign
            # -------------------------------------------------

            degree = sign_degree(
                longitude
            )

            # -------------------------------------------------
            # Nakshatra
            # -------------------------------------------------

            nakshatra = (
                longitude_to_nakshatra(
                    longitude
                )
            )

            pada = nakshatra_pada(
                longitude
            )

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

            # =================================================
            # BPHS PLANETARY DIGNITY
            # =================================================

            classical_dignity_planets = {
                "Sun",
                "Moon",
                "Mars",
                "Mercury",
                "Jupiter",
                "Venus",
                "Saturn",
            }

            if (
                graha.display_name
                in classical_dignity_planets
            ):

                planet.exalted = is_exalted(
                    graha,
                    sign,
                )

                planet.debilitated = (
                    is_debilitated(
                        graha,
                        sign,
                    )
                )

                planet.own_sign = is_own_sign(
                    graha,
                    sign,
                )

                planet.moolatrikona = (
                    is_moolatrikona(
                        graha,
                        sign,
                    )
                )

                if planet.exalted:

                    planet.dignity = (
                        "Exalted"
                    )

                elif planet.debilitated:

                    planet.dignity = (
                        "Debilitated"
                    )

                elif planet.moolatrikona:

                    planet.dignity = (
                        "Moolatrikona"
                    )

                elif planet.own_sign:

                    planet.dignity = (
                        "Own Sign"
                    )

                else:

                    planet.dignity = (
                        "Neutral"
                    )

            else:

                # Rahu and Ketu dignity is not
                # implemented in astronomy.dignity.

                planet.exalted = False
                planet.debilitated = False
                planet.own_sign = False
                planet.moolatrikona = False

                planet.dignity = (
                    "Not Implemented"
                )

            planets.append(
                planet
            )

        # =====================================================
        # 8. PLANET -> HOUSE ASSIGNMENT
        # =====================================================

        planets, houses = (
            assign_planets_to_houses(
                planets,
                houses,
            )
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
        # 10. CLASSICAL PARASHARI ASPECTS / DRISHTI
        # =====================================================

        planet_signs = {
            planet.name: planet.sign_number
            for planet in planets
        }

        chart.aspect_map = (
            build_aspect_map(
                planet_signs,
                include_nodes=True,
            )
        )

        # -----------------------------------------------------
        # Planet-to-planet aspects
        # -----------------------------------------------------

        planetary_aspects = {}

        planet_items = list(
            chart.planets.items()
        )

        for (
            aspecting_name,
            aspecting_planet,
        ) in planet_items:

            planetary_aspects[
                aspecting_name
            ] = []

            for (
                target_name,
                target_planet,
            ) in planet_items:

                if (
                    aspecting_name
                    == target_name
                ):
                    continue

                is_aspecting = (
                    planet_aspects_planet(
                        aspecting_planet=(
                            aspecting_name
                        ),
                        aspecting_sign=(
                            aspecting_planet.sign_number
                        ),
                        target_planet=(
                            target_name
                        ),
                        target_sign=(
                            target_planet.sign_number
                        ),
                        include_nodes=True,
                    )
                )

                if is_aspecting:

                    planetary_aspects[
                        aspecting_name
                    ].append(
                        target_name
                    )

        chart.planetary_aspects = (
            planetary_aspects
        )

        # -----------------------------------------------------
        # Planet-to-house aspects
        # -----------------------------------------------------

        house_aspects = {}

        for (
            house_number,
            house,
        ) in houses.items():

            house_sign_number = getattr(
                house,
                "sign_number",
                None,
            )

            if house_sign_number is None:

                house_sign = getattr(
                    house,
                    "sign",
                    None,
                )

                if house_sign is not None:

                    house_sign_number = (
                        getattr(
                            house_sign,
                            "number",
                            None,
                        )
                    )

            if house_sign_number is None:
                continue

            house_aspects[
                house_number
            ] = []

            for planet in planets:

                if planet_aspects_planet(
                    aspecting_planet=(
                        planet.name
                    ),
                    aspecting_sign=(
                        planet.sign_number
                    ),
                    target_planet=(
                        planet.name
                    ),
                    target_sign=(
                        house_sign_number
                    ),
                    include_nodes=True,
                ):

                    house_aspects[
                        house_number
                    ].append(
                        planet.name
                    )

        chart.house_aspects = (
            house_aspects
        )

        # =====================================================
        # 11. COMPLETE VIMSHOTTARI DASHA HIERARCHY
        # =====================================================

        moon = chart.get_planet(
            "Moon"
        )

        if moon is not None:

            moon_longitude = (
                moon.longitude
            )

            # =================================================
            # MAHADASHA
            # =================================================

            chart.mahadashas = (
                generate_mahadashas(
                    birth.birth_datetime,
                    moon_longitude,
                    count=18,
                )
            )

            chart.current_mahadasha = (
                current_mahadasha(
                    birth.birth_datetime,
                    moon_longitude,
                )
            )

            # =================================================
            # ANTARDASHA
            # =================================================

            chart.antardashas = (
                generate_antardashas(
                    chart.current_mahadasha
                )
            )

            chart.current_antardasha = (
                current_antardasha(
                    birth.birth_datetime,
                    moon_longitude,
                )
            )

            # =================================================
            # PRATYANTARDASHA
            # =================================================

            chart.pratyantardashas = (
                generate_pratyantardashas(
                    chart.current_antardasha
                )
            )

            # IMPORTANT:
            # current_pratyantardasha() expects an
            # Antardasha object, not birth_datetime
            # and moon_longitude.

            chart.current_pratyantardasha = (
                current_pratyantardasha(
                    chart.current_antardasha
                )
            )

            # =================================================
            # SOOKSHMA DASHA
            # =================================================

            chart.sookshmadashas = (
                generate_sookshmadashas(
                    chart.current_pratyantardasha
                )
            )

            # IMPORTANT:
            # current_sookshmadasha() expects the
            # current Pratyantardasha as its parent.

            chart.current_sookshmadasha = (
                current_sookshmadasha(
                    chart.current_pratyantardasha
                )
            )

            # =================================================
            # PRANA DASHA
            # =================================================

            chart.pranadashas = (
                generate_pranadashas(
                    chart.current_sookshmadasha
                )
            )

            # IMPORTANT:
            # current_pranadasha() expects the
            # current Sookshma Dasha as its parent.

            chart.current_pranadasha = (
                current_pranadasha(
                    chart.current_sookshmadasha
                )
            )

            # =================================================
            # DEHA DASHA
            # =================================================

            chart.dehadashas = (
                generate_dehadashas(
                    chart.current_pranadasha
                )
            )

            # IMPORTANT:
            # current_dehadasha() expects the
            # current Prana Dasha as its parent.

            chart.current_dehadasha = (
                current_dehadasha(
                    chart.current_pranadasha
                )
            )

            # =================================================
            # LEGACY DASHA FIELD
            # =================================================

            chart.dashas = (
                chart.mahadashas
            )

        # =====================================================
        # 12. RETURN COMPLETE CHART
        # =====================================================

        return chart


__all__ = [
    "HoroscopeEngine",
]
