"""
main.py

Kundali Engine
Version 2.5.0

Displays:
    - Birth information
    - Julian Day
    - Lahiri Ayanamsa
    - Ascendant
    - Planetary positions
    - Whole Sign houses
    - Vimshottari Mahadasha
    - Antardasha
    - Pratyantardasha
    - Sookshma Dasha
    - Prana Dasha
    - Deha Dasha

Compatible with Python 3.9.
"""

from datetime import datetime

from astronomy.signs import (
    sign_degree,
    sign_enum,
)

from astronomy.swiss import (
    Ayanamsha,
    set_ayanamsha,
    set_ephemeris_path,
)

from engine import HoroscopeEngine

from models.birth_data import BirthData
from models.location import Location


from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

EPHEMERIS_PATH = str(Path(__file__).resolve().parent / "ephe")


# ============================================================
# DISPLAY UTILITIES
# ============================================================

def print_separator():
    """Print a standard separator."""
    print("=" * 70)


def print_section(title: str):
    """Print a formatted section heading."""
    print()
    print_separator()
    print(title)
    print_separator()


def format_datetime(moment):
    """
    Format a datetime with enough precision to inspect
    nested Vimshottari Dasha boundaries.
    """

    if moment is None:
        return "-"

    return moment.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def format_date(moment):
    """Format a datetime as date only."""
    if moment is None:
        return "-"

    return moment.strftime(
        "%Y-%m-%d"
    )


def format_duration_days(days: float) -> str:
    """
    Convert duration in days into a human-readable
    days / hours / minutes / seconds representation.
    """

    if days < 0:
        return "INVALID"

    total_seconds = int(
        round(days * 86400.0)
    )

    days_part = total_seconds // 86400

    remainder = (
        total_seconds
        % 86400
    )

    hours_part = (
        remainder // 3600
    )

    remainder %= 3600

    minutes_part = (
        remainder // 60
    )

    seconds_part = (
        remainder % 60
    )

    return (
        f"{days_part}d "
        f"{hours_part:02d}h "
        f"{minutes_part:02d}m "
        f"{seconds_part:02d}s"
    )


def print_dasha_period(
    lord,
    start,
    end,
    duration_days=None,
    marker="",
):
    """Print one Dasha period."""

    if duration_days is None:
        duration_days = (
            end - start
        ).total_seconds() / 86400.0

    print(
        f"{lord:<20}"
        f"{format_datetime(start):>22}"
        f"{format_datetime(end):>22}"
        f"{format_duration_days(duration_days):>20}"
        f"{marker}"
    )


# ============================================================
# MAIN
# ============================================================

def main():
    """Build and display a test Kundali."""

    # ========================================================
    # 1. CONFIGURE SWISS EPHEMERIS
    # ========================================================

    set_ephemeris_path(
        EPHEMERIS_PATH
    )

    set_ayanamsha(
        Ayanamsha.LAHIRI
    )

    # ========================================================
    # 2. LOCATION
    # ========================================================

    location = Location(
        name="Kathmandu, Nepal",
        latitude=27.7172,
        longitude=85.3240,
        timezone="Asia/Kathmandu",
        elevation=1400.0,
        country="Nepal",
        city="Kathmandu",
    )

    # ========================================================
    # 3. BIRTH DATA
    # ========================================================

    birth = BirthData(
        name="Test User",
        birth_datetime=datetime(
            2000,
            1,
            1,
            12,
            0,
            0,
        ),
        location=location,
    )

    # ========================================================
    # 4. GENERATE CHART
    # ========================================================

    engine = HoroscopeEngine()

    chart = engine.build_chart(
        birth
    )

    # ========================================================
    # 5. HEADER
    # ========================================================

    print_separator()
    print("KUNDALI ENGINE")
    print_separator()

    print(
        f"Name       : "
        f"{birth.name}"
    )

    print(
        f"Birth Time : "
        f"{format_datetime(birth.birth_datetime)}"
    )

    print(
        f"Place      : "
        f"{birth.location.name}"
    )

    print(
        f"Timezone   : "
        f"{birth.location.timezone}"
    )

    print()

    print(
        f"Julian Day : "
        f"{chart.julian_day:.6f}"
    )

    print(
        f"Ayanamsa   : "
        f"{chart.ayanamsa:.6f}"
    )

    # ========================================================
    # 6. ASCENDANT
    # ========================================================

    asc_sign = sign_enum(
        chart.ascendant
    )

    asc_degree = sign_degree(
        chart.ascendant
    )

    print(
        f"Ascendant  : "
        f"{asc_sign.display_name} "
        f"{asc_degree:.2f}°"
    )

    # ========================================================
    # 7. PLANETS
    # ========================================================

    print_section(
        "PLANETS"
    )

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
            f"{str(planet.sign):<14}"
            f"{planet.sign_degree:>7.2f}°"
            f"{planet.house:>8}   "
            f"{planet.nakshatra:<18}"
            f"{planet.pada}"
        )

    # ========================================================
    # 8. WHOLE SIGN HOUSES
    # ========================================================

    print_section(
        "WHOLE SIGN HOUSES"
    )

    for house_number in sorted(
        chart.houses.keys()
    ):

        house = chart.houses[
            house_number
        ]

        print(
            f"House {house.number:<2} "
            f"{house.sign[0]:<12} "
            f"{house.longitude:>6.1f}°"
        )

    # ========================================================
    # 9. VIMSHOTTARI MAHADASHA
    # ========================================================

    print_section(
        "VIMSHOTTARI DASHA"
    )

    mahadashas = (
        chart.mahadashas
    )

    if mahadashas:

        first_dasha = (
            mahadashas[0]
        )

        print(
            f"Starting Mahadasha : "
            f"{first_dasha.planet}"
        )

        print(
            f"Balance at Birth   : "
            f"{first_dasha.duration_years:.4f} years"
        )

        print()

        print(
            f"{'Mahadasha':<12}"
            f"{'Duration':>12}"
            f"{'Start':>22}"
            f"{'End':>22}"
        )

        print("-" * 68)

        for dasha in mahadashas:

            print(
                f"{dasha.planet:<12}"
                f"{dasha.duration_years:>10.4f} yr"
                f"{format_date(dasha.start):>22}"
                f"{format_date(dasha.end):>22}"
            )

    # ========================================================
    # 10. CURRENT COMPLETE DASHA CHAIN
    # ========================================================

    print_section(
        "CURRENT DASHA CHAIN"
    )

    current_md = (
        chart.current_mahadasha
    )

    current_ad = (
        chart.current_antardasha
    )

    current_pd = (
        chart.current_pratyantardasha
    )

    current_sd = (
        chart.current_sookshmadasha
    )

    current_prana = (
        chart.current_pranadasha
    )

    current_deha = (
        chart.current_dehadasha
    )

    # --------------------------------------------------------
    # Mahadasha
    # --------------------------------------------------------

    if current_md is not None:

        print(
            f"Mahadasha         : "
            f"{current_md.planet}"
        )

        print(
            f"MD Start          : "
            f"{format_datetime(current_md.start)}"
        )

        print(
            f"MD End            : "
            f"{format_datetime(current_md.end)}"
        )

    # --------------------------------------------------------
    # Antardasha
    # --------------------------------------------------------

    if current_ad is not None:

        print(
            f"Antardasha        : "
            f"{current_ad.antardasha_lord}"
        )

        print(
            f"AD Start          : "
            f"{format_datetime(current_ad.start)}"
        )

        print(
            f"AD End            : "
            f"{format_datetime(current_ad.end)}"
        )

    # --------------------------------------------------------
    # Pratyantardasha
    # --------------------------------------------------------

    if current_pd is not None:

        print(
            f"Pratyantardasha   : "
            f"{current_pd.pratyantardasha_lord}"
        )

        print(
            f"PD Start          : "
            f"{format_datetime(current_pd.start)}"
        )

        print(
            f"PD End            : "
            f"{format_datetime(current_pd.end)}"
        )

    # --------------------------------------------------------
    # Sookshma
    # --------------------------------------------------------

    if current_sd is not None:

        print(
            f"Sookshma Dasha    : "
            f"{current_sd.sookshma_lord}"
        )

        print(
            f"SD Start          : "
            f"{format_datetime(current_sd.start)}"
        )

        print(
            f"SD End            : "
            f"{format_datetime(current_sd.end)}"
        )

    # --------------------------------------------------------
    # Prana
    # --------------------------------------------------------

    if current_prana is not None:

        print(
            f"Prana Dasha       : "
            f"{current_prana.prana_lord}"
        )

        print(
            f"Prana Start       : "
            f"{format_datetime(current_prana.start)}"
        )

        print(
            f"Prana End         : "
            f"{format_datetime(current_prana.end)}"
        )

        print(
            f"Prana Duration    : "
            f"{format_duration_days(current_prana.duration_days)}"
        )

    # --------------------------------------------------------
    # Deha
    # --------------------------------------------------------

    if current_deha is not None:

        print(
            f"Deha Dasha        : "
            f"{current_deha.deha_lord}"
        )

        print(
            f"Deha Start        : "
            f"{format_datetime(current_deha.start)}"
        )

        print(
            f"Deha End          : "
            f"{format_datetime(current_deha.end)}"
        )

        print(
            f"Deha Duration     : "
            f"{format_duration_days(current_deha.duration_days)}"
        )

    # ========================================================
    # 11. ANTARDASHA TABLE
    # ========================================================

    if (
        chart.current_mahadasha
        and chart.antardashas
    ):

        print_section(
            f"ANTARDASHAS — "
            f"{chart.current_mahadasha.planet.upper()} "
            f"MAHADASHA"
        )

        print(
            f"{'Antardasha':<14}"
            f"{'Start':>22}"
            f"{'End':>22}"
            f"{'Duration':>20}"
        )

        print("-" * 78)

        for antardasha in (
            chart.antardashas
        ):

            marker = ""

            if (
                chart.current_antardasha
                and
                antardasha.start
                == chart.current_antardasha.start
                and
                antardasha.end
                == chart.current_antardasha.end
            ):

                marker = "  <-- CURRENT"

            print_dasha_period(
                antardasha.antardasha_lord,
                antardasha.start,
                antardasha.end,
                antardasha.duration_days,
                marker,
            )

    # ========================================================
    # 12. PRATYANTARDASHA TABLE
    # ========================================================

    if (
        chart.current_antardasha
        and chart.pratyantardashas
    ):

        print_section(
            f"PRATYANTARDASHAS — "
            f"{chart.current_mahadasha.planet.upper()} "
            f"MD / "
            f"{chart.current_antardasha.antardasha_lord.upper()} "
            f"AD"
        )

        print(
            f"{'Pratyantardasha':<20}"
            f"{'Start':>22}"
            f"{'End':>22}"
            f"{'Duration':>20}"
        )

        print("-" * 84)

        for pratyantardasha in (
            chart.pratyantardashas
        ):

            marker = ""

            if (
                chart.current_pratyantardasha
                and
                pratyantardasha.start
                == chart.current_pratyantardasha.start
                and
                pratyantardasha.end
                == chart.current_pratyantardasha.end
            ):

                marker = "  <-- CURRENT"

            print_dasha_period(
                pratyantardasha.pratyantardasha_lord,
                pratyantardasha.start,
                pratyantardasha.end,
                pratyantardasha.duration_days,
                marker,
            )

    # ========================================================
    # 13. SOOKSHMA DASHA TABLE
    # ========================================================

    if (
        chart.current_pratyantardasha
        and chart.sookshmadashas
    ):

        print_section(
            f"SOOKSHMA DASHAS — "
            f"{chart.current_mahadasha.planet.upper()} "
            f"MD / "
            f"{chart.current_antardasha.antardasha_lord.upper()} "
            f"AD / "
            f"{chart.current_pratyantardasha.pratyantardasha_lord.upper()} "
            f"PD"
        )

        print(
            f"{'Sookshma Dasha':<20}"
            f"{'Start':>22}"
            f"{'End':>22}"
            f"{'Duration':>20}"
        )

        print("-" * 84)

        for sookshmadasha in (
            chart.sookshmadashas
        ):

            marker = ""

            if (
                chart.current_sookshmadasha
                and
                sookshmadasha.start
                == chart.current_sookshmadasha.start
                and
                sookshmadasha.end
                == chart.current_sookshmadasha.end
            ):

                marker = "  <-- CURRENT"

            print_dasha_period(
                sookshmadasha.sookshma_lord,
                sookshmadasha.start,
                sookshmadasha.end,
                sookshmadasha.duration_days,
                marker,
            )

    # ========================================================
    # 14. PRANA DASHA TABLE
    # ========================================================

    if (
        chart.current_sookshmadasha
        and chart.pranadashas
    ):

        print_section(
            f"PRANA DASHAS — "
            f"{chart.current_mahadasha.planet.upper()} "
            f"MD / "
            f"{chart.current_antardasha.antardasha_lord.upper()} "
            f"AD / "
            f"{chart.current_pratyantardasha.pratyantardasha_lord.upper()} "
            f"PD / "
            f"{chart.current_sookshmadasha.sookshma_lord.upper()} "
            f"SD"
        )

        print(
            f"{'Prana Dasha':<20}"
            f"{'Start':>22}"
            f"{'End':>22}"
            f"{'Duration':>20}"
        )

        print("-" * 84)

        for pranadasha in (
            chart.pranadashas
        ):

            marker = ""

            if (
                chart.current_pranadasha
                and
                pranadasha.start
                == chart.current_pranadasha.start
                and
                pranadasha.end
                == chart.current_pranadasha.end
            ):

                marker = "  <-- CURRENT"

            print_dasha_period(
                pranadasha.prana_lord,
                pranadasha.start,
                pranadasha.end,
                pranadasha.duration_days,
                marker,
            )

    # ========================================================
    # 15. DEHA DASHA TABLE
    # ========================================================

    if (
        chart.current_pranadasha
        and chart.dehadashas
    ):

        print_section(
            f"DEHA DASHAS — "
            f"{chart.current_mahadasha.planet.upper()} "
            f"MD / "
            f"{chart.current_antardasha.antardasha_lord.upper()} "
            f"AD / "
            f"{chart.current_pratyantardasha.pratyantardasha_lord.upper()} "
            f"PD / "
            f"{chart.current_sookshmadasha.sookshma_lord.upper()} "
            f"SD / "
            f"{chart.current_pranadasha.prana_lord.upper()} "
            f"PRANA"
        )

        print(
            f"{'Deha Dasha':<20}"
            f"{'Start':>22}"
            f"{'End':>22}"
            f"{'Duration':>20}"
        )

        print("-" * 84)

        for dehadasha in (
            chart.dehadashas
        ):

            marker = ""

            if (
                chart.current_dehadasha
                and
                dehadasha.start
                == chart.current_dehadasha.start
                and
                dehadasha.end
                == chart.current_dehadasha.end
            ):

                marker = "  <-- CURRENT"

            print_dasha_period(
                dehadasha.deha_lord,
                dehadasha.start,
                dehadasha.end,
                dehadasha.duration_days,
                marker,
            )

    # ========================================================
    # 16. FINAL HIERARCHY SUMMARY
    # ========================================================

    print_section(
        "ACTIVE VIMSHOTTARI HIERARCHY"
    )

    hierarchy = [
        (
            "Mahadasha",
            current_md.planet
            if current_md
            else None,
        ),
        (
            "Antardasha",
            current_ad.antardasha_lord
            if current_ad
            else None,
        ),
        (
            "Pratyantardasha",
            current_pd.pratyantardasha_lord
            if current_pd
            else None,
        ),
        (
            "Sookshma",
            current_sd.sookshma_lord
            if current_sd
            else None,
        ),
        (
            "Prana",
            current_prana.prana_lord
            if current_prana
            else None,
        ),
        (
            "Deha",
            current_deha.deha_lord
            if current_deha
            else None,
        ),
    ]

    for level, lord in hierarchy:

        print(
            f"{level:<20}: "
            f"{lord if lord else 'N/A'}"
        )

    print()
    print_separator()
    print("END OF KUNDALI ENGINE OUTPUT")
    print_separator()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()