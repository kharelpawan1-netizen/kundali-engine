"""
main.py

Kundali Engine
Version: 1.2.0
Compatible with Python 3.9
"""

from datetime import datetime

from engine import HoroscopeEngine

from models.birth_data import BirthData
from models.location import Location


def main():

    # -----------------------------
    # Birth Location
    # -----------------------------

    location = Location(

        latitude=27.7172,

        longitude=85.3240,

        timezone="Asia/Kathmandu",

        city="Kathmandu",

        country="Nepal"

    )

    # -----------------------------
    # Birth Data
    # -----------------------------

    birth = BirthData(

        name="Test User",

        birth_datetime=datetime(
            2000,
            1,
            1,
            12,
            0,
            0
        ),

        location=location

    )

    # -----------------------------
    # Build Chart
    # -----------------------------

    engine = HoroscopeEngine()

    chart = engine.build_chart(birth)

    # -----------------------------
    # Output
    # -----------------------------

    print()
    print("=" * 70)
    print("KUNDALI ENGINE")
    print("=" * 70)

    print(f"Name      : {birth.name}")
    print(f"Place     : {location.city}, {location.country}")
    print(f"Timezone  : {location.timezone}")

    print()
    print(f"Julian Day : {chart.julian_day:.6f}")
    print(f"Ayanamsa   : {chart.ayanamsa:.6f}")

    print()
    print("=" * 70)
    print("PLANETS")
    print("=" * 70)

    for planet in chart.planets.values():

        print(
            f"{planet.name:10}"
            f"{planet.sign:15}"
            f"{planet.sign_degree:7.2f}°   "
            f"{planet.nakshatra:18}"
            f"Pada {planet.pada}"
        )


if __name__ == "__main__":
    main()