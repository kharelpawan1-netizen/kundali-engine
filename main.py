"""
main.py

Kundali Engine
Version 2.0.0
Compatible with Python 3.9
"""

from datetime import datetime

from astronomy.signs import get_sign
from engine import HoroscopeEngine
from models.birth_data import BirthData
from models.location import Location


def print_separator():
    """Print a separator line."""
    print("=" * 70)


def main():
    """
    Main entry point.
    """

    # ---------------------------------------------------------
    # Location
    # ---------------------------------------------------------

    location = Location(
        name="Kathmandu, Nepal",
        latitude=27.7172,
        longitude=85.3240,
        timezone="Asia/Kathmandu",
        elevation=1400.0,
        country="Nepal",
        city="Kathmandu",
    )

    # ---------------------------------------------------------
    # Birth Data
    # ---------------------------------------------------------

    birth = BirthData(
        name="Test User",
        birth_datetime=datetime(2000, 1, 1, 12, 0, 0),
        location=location,
    )

    # ---------------------------------------------------------
    # Generate Chart
    # ---------------------------------------------------------

    engine = HoroscopeEngine()

    chart = engine.build_chart(birth)

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    print_separator()
    print("KUNDALI ENGINE")
    print_separator()

    print(f"Name       : {birth.name}")
    print(f"Place      : {birth.location.name}")
    print(f"Timezone   : {birth.location.timezone}")

    print()
    print(f"Julian Day : {chart.julian_day:.6f}")
    print(f"Ayanamsa   : {chart.ayanamsa:.6f}")

    asc_sign, _, asc_degree = get_sign(chart.ascendant)

    print(f"Ascendant  : {asc_sign} {asc_degree:.2f}°")

    # ---------------------------------------------------------
    # Planets
    # ---------------------------------------------------------

    print()
    print_separator()
    print("PLANETS")
    print_separator()

    header = (
        f"{'Planet':<10}"
        f"{'Sign':<14}"
        f"{'Degree':>8}"
        f"{'House':>8}   "
        f"{'Nakshatra':<18}"
        f"{'Pada'}"
    )

    print(header)
    print("-" * len(header))

    for planet in chart.planets.values():

        print(
            f"{planet.name:<10}"
            f"{planet.sign:<14}"
            f"{planet.sign_degree:>7.2f}°"
            f"{planet.house:>8}   "
            f"{planet.nakshatra:<18}"
            f"{planet.pada}"
        )

    # ---------------------------------------------------------
    # Houses
    # ---------------------------------------------------------

    print()
    print_separator()
    print("WHOLE SIGN HOUSES")
    print_separator()

    for house_number in sorted(chart.houses.keys()):

        house = chart.houses[house_number]

        print(
            f"House {house.number:<2} "
            f"{house.sign:<12} "
            f"{house.start_longitude:>6.1f}° - "
            f"{house.end_longitude:>6.1f}°"
        )


if __name__ == "__main__":
    main()
