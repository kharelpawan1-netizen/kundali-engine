"""
api/serializers.py

Comprehensive serializers to convert Kundali Engine objects into clean,
rich JSON structures for the dashboard frontend.

Includes:
- Plantery metadata, Nakshatras, dignities, and BPHS rules
- Combustion (Astangata) degree-based calculations
- Planetary Strengths (Balas: Cheshta, Dig, Naisargika, Natonnata, Paksha, Uccha)
- Panchadha Maitri (5-fold Compound Planetary Relationship Matrix)
- Shani Sade Sati calculation, phases (Rising, Peak, Setting), and timeline
- Live Planetary Transits (Gochara) relative to natal Moon & Lagna
- 16 BPHS Shodashavarga Divisional Charts (D1 through D60)
- 6-Level Vimshottari Dasha Hierarchy (MD, AD, PD, SD, Prana, Deha)
- Structural Vedic Yogas (Raja, Dhana, Gaja Kesari, Budha-Aditya, Chandra-Mangala,
  Guru Chandal, Neecha Bhanga Raja, Parivartana)
- Life Synthesis and Karmic Interpretations
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from astronomy.signs import SIGNS, sign_degree, sign_enum, sign_number
from astronomy.varga_engine import build_varga_chart
from astronomy.julian import datetime_to_julian
from astronomy.planets import calculate_planets
from astronomy.nakshatra import longitude_to_nakshatra, nakshatra_pada
from astronomy.panchadha import compound_relationship
from astronomy.relationships import natural_relationship
from astronomy.tatkalika import temporary_relationship
from astronomy.cheshta_bala import cheshta_bala
from astronomy.dig_bala import dig_bala
from astronomy.naisargika_bala import naisargika_bala
from astronomy.natonnata_bala import natonnata_bala
from astronomy.paksha_bala import paksha_bala
from astronomy.uccha_bala import uccha_bala

from astrology.dasha import generate_mahadashas, generate_antardashas
from astrology.pratyantardasha import generate_pratyantardashas
from astrology.sookshmadasha import generate_sookshmadashas
from astrology.pranadasha import generate_pranadashas
from astrology.dehadasha import generate_dehadashas
from astrology.sade_sati import (
    is_sade_sati_active,
    sade_sati_phase_name,
    sade_sati_signs,
    sade_sati_evidence,
    generate_sade_sati_periods,
    RISING_PHASE,
    PEAK_PHASE,
    SETTING_PHASE,
)

from yogas.rajyoga import detect_rajyoga
from yogas.dhanayoga import detect_dhanayoga
from yogas.gaja_kesari import detect_gaja_kesari
from yogas.budha_aditya import detect_budha_aditya
from yogas.chandra_mangala import detect_chandra_mangala
from yogas.neecha_bhanga import detect_neecha_bhanga
from yogas.parivartana import detect_parivartana
from yogas.guru_chandal import detect_guru_chandal

from interpretation.context import build_interpretation_context
from interpretation.planet_analysis import analyze_planets
from interpretation.house_analysis import analyze_houses
from interpretation.dignity_analysis import analyze_dignities
from interpretation.aspect_analysis import analyze_aspects
from interpretation.yoga_analysis import analyze_yoga_interpretations
from interpretation.synthesis import synthesize_chart

from models.chart import BirthChart
from models.planet import Planet
from models.graha import Graha
from models.zodiac import ZodiacSign, sign_from_number


SIGN_LORD: Dict[int, str] = {
    1: "Mars",
    2: "Venus",
    3: "Mercury",
    4: "Moon",
    5: "Sun",
    6: "Mercury",
    7: "Venus",
    8: "Mars",
    9: "Jupiter",
    10: "Saturn",
    11: "Saturn",
    12: "Jupiter",
}

GRAHA_MAP: Dict[str, Graha] = {
    "Sun": Graha.SUN,
    "Moon": Graha.MOON,
    "Mars": Graha.MARS,
    "Mercury": Graha.MERCURY,
    "Jupiter": Graha.JUPITER,
    "Venus": Graha.VENUS,
    "Saturn": Graha.SATURN,
    "Rahu": Graha.RAHU,
    "Ketu": Graha.KETU,
}

CLASSICAL_GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Classical Combustion (Astangata) degree limits from the Sun
COMBUSTION_LIMITS: Dict[str, float] = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,  # 12° when retrograde
    "Jupiter": 11.0,
    "Venus": 10.0,    # 8° when retrograde
    "Saturn": 15.0,
}

# Sanskrit / Vedic display names & symbols for planets
PLANET_METADATA = {
    "Sun": {"sanskrit": "Surya (सूर्य)", "symbol": "☉", "short": "Su", "color": "#f59e0b", "element": "Fire", "gender": "Male"},
    "Moon": {"sanskrit": "Chandra (चन्द्र)", "symbol": "☽", "short": "Mo", "color": "#e2e8f0", "element": "Water", "gender": "Female"},
    "Mars": {"sanskrit": "Mangala (मङ्गल)", "symbol": "♂", "short": "Ma", "color": "#ef4444", "element": "Fire", "gender": "Male"},
    "Mercury": {"sanskrit": "Budha (बुध)", "symbol": "☿", "short": "Me", "color": "#10b981", "element": "Earth", "gender": "Neutral"},
    "Jupiter": {"sanskrit": "Guru / Brihaspati (गुरु)", "symbol": "♃", "short": "Ju", "color": "#eab308", "element": "Ether", "gender": "Male"},
    "Venus": {"sanskrit": "Shukra (शुक्र)", "symbol": "♀", "short": "Ve", "color": "#ec4899", "element": "Water", "gender": "Female"},
    "Saturn": {"sanskrit": "Shani (शनि)", "symbol": "♄", "short": "Sa", "color": "#6366f1", "element": "Air", "gender": "Neutral"},
    "Rahu": {"sanskrit": "Rahu (राहु)", "symbol": "☊", "short": "Ra", "color": "#8b5cf6", "element": "Air", "gender": "Male"},
    "Ketu": {"sanskrit": "Ketu (केतु)", "symbol": "☋", "short": "Ke", "color": "#a855f7", "element": "Fire", "gender": "Neutral"},
    "Ascendant": {"sanskrit": "Lagna (लग्न)", "symbol": "ASC", "short": "As", "color": "#38bdf8", "element": "Space", "gender": ""},
}

SIGN_NAMES_SANSKRIT = {
    1: "Mesha (मेष - Aries)",
    2: "Vrishabha (वृषभ - Taurus)",
    3: "Mithuna (मिथुन - Gemini)",
    4: "Karka (कर्क - Cancer)",
    5: "Simha (सिंह - Leo)",
    6: "Kanya (कन्या - Virgo)",
    7: "Tula (तुला - Libra)",
    8: "Vrishchika (वृश्चिक - Scorpio)",
    9: "Dhanu (धनु - Sagittarius)",
    10: "Makara (मकर - Capricorn)",
    11: "Kumbha (कुम्भ - Aquarius)",
    12: "Meena (मीन - Pisces)",
}

SIGN_ELEMENTS = {
    1: "Fire", 2: "Earth", 3: "Air", 4: "Water",
    5: "Fire", 6: "Earth", 7: "Air", 8: "Water",
    9: "Fire", 10: "Earth", 11: "Air", 12: "Water",
}

HOUSE_SIGNIFICANCE = {
    1: {"name": "Tanu Bhava (Self & Personality)", "domains": "Physical appearance, character, vitality, life path, health, self-expression"},
    2: {"name": "Dhana Bhava (Wealth & Family)", "domains": "Accumulated wealth, speech, eating habits, early education, family values"},
    3: {"name": "Sahaja Bhava (Siblings & Courage)", "domains": "Courage, initiatives, younger siblings, communication, skills, short travels"},
    4: {"name": "Bandhu / Sukha Bhava (Home & Mother)", "domains": "Mother, domestic peace, vehicles, land, property, emotional stability, inner happiness"},
    5: {"name": "Putra Bhava (Children & Intelligence)", "domains": "Intellect, creativity, progeny, past life merit (Purva Punya), romance, speculation"},
    6: {"name": "Ari / Shatru Bhava (Obstacles & Service)", "domains": "Enemies, debts, diseases, daily routine, service, litigations, competitiveness"},
    7: {"name": "Yuvati / Kalatra Bhava (Spouse & Partnerships)", "domains": "Marriage, life partner, business alliances, legal agreements, foreign trade"},
    8: {"name": "Randhra / Ayu Bhava (Longevity & Transformation)", "domains": "Longevity, sudden events, occult, research, inheritance, deep secrets, transformation"},
    9: {"name": "Dharma / Bhagya Bhava (Fortune & Higher Wisdom)", "domains": "Fortune, father, guru, higher learning, philosophy, religion, long journeys, destiny"},
    10: {"name": "Karma Bhava (Career & Status)", "domains": "Profession, social status, reputation, leadership, government favor, public achievements"},
    11: {"name": "Labha Bhava (Gains & Social Network)", "domains": "Income, profits, fulfillment of desires, elder siblings, social circle, aspirations"},
    12: {"name": "Vyaya Bhava (Expenditure & Liberation)", "domains": "Expenses, losses, foreign residence, spiritual liberation (Moksha), sleep, subconscious"},
}


def degree_to_dms(deg: float) -> str:
    """Convert float degrees to Degree° Minute' Second\" string."""
    deg_norm = deg % 360.0
    d = int(deg_norm)
    rem = (deg_norm - d) * 60.0
    m = int(rem)
    s = round((rem - m) * 60.0, 1)
    if s >= 60.0:
        s = 0.0
        m += 1
    if m >= 60:
        m = 0
        d = (d + 1) % 360
    return f"{d}° {m:02d}' {s:04.1f}\""


def format_duration(days: float) -> str:
    """Format duration in days into human-readable string."""
    if days < 0:
        return "0d"
    total_seconds = int(round(days * 86400.0))
    days_part = total_seconds // 86400
    remainder = total_seconds % 86400
    hours_part = remainder // 3600
    remainder %= 3600
    minutes_part = remainder // 60
    if days_part > 365:
        years = days_part / 365.25
        return f"{years:.1f} yrs"
    if days_part > 30:
        months = days_part / 30.4375
        return f"{months:.1f} mos ({days_part}d)"
    if days_part > 0:
        return f"{days_part}d {hours_part}h"
    return f"{hours_part}h {minutes_part}m"


def check_combustion(planet_name: str, planet_long: float, sun_long: float, is_retrograde: bool) -> Dict[str, Any]:
    """Check whether a planet is Combust (Astangata) from the Sun."""
    if planet_name not in COMBUSTION_LIMITS:
        return {"is_combust": False, "separation": 0.0, "limit": 0.0}

    limit = COMBUSTION_LIMITS[planet_name]
    if planet_name == "Mercury" and is_retrograde:
        limit = 12.0
    elif planet_name == "Venus" and is_retrograde:
        limit = 8.0

    diff = abs(planet_long - sun_long)
    separation = min(diff, 360.0 - diff)
    is_combust = separation <= limit

    return {
        "is_combust": is_combust,
        "separation": round(separation, 2),
        "limit": limit,
    }


def serialize_planet(planet: Planet, house_num: int, sun_longitude: float = 0.0) -> Dict[str, Any]:
    """Serialize a single planet model with full astronomical & astrological parameters."""
    name = planet.name
    meta = PLANET_METADATA.get(name, {
        "sanskrit": name,
        "symbol": "✦",
        "short": name[:2],
        "color": "#e2e8f0",
        "element": "",
        "gender": "",
    })

    sign_num = planet.sign_number
    sign_lord = SIGN_LORD.get(sign_num, "")

    dignity_str = planet.dignity or "Neutral"
    if planet.exalted:
        dignity_str = "Exalted"
    elif planet.debilitated:
        dignity_str = "Debilitated"
    elif planet.moolatrikona:
        dignity_str = "Moolatrikona"
    elif planet.own_sign:
        dignity_str = "Own Sign"

    # Combustion check
    combust_info = check_combustion(name, planet.longitude, sun_longitude, planet.retrograde)

    return {
        "name": name,
        "sanskrit_name": meta["sanskrit"],
        "symbol": meta["symbol"],
        "short_name": meta["short"],
        "color": meta["color"],
        "element": meta["element"],
        "longitude": round(planet.longitude, 4),
        "longitude_dms": degree_to_dms(planet.longitude),
        "sign": planet.sign,
        "sign_sanskrit": SIGN_NAMES_SANSKRIT.get(sign_num, planet.sign),
        "sign_number": sign_num,
        "sign_lord": sign_lord,
        "sign_degree": round(planet.sign_degree, 4),
        "sign_degree_dms": degree_to_dms(planet.sign_degree),
        "house": house_num,
        "house_sanskrit": f"Bhava {house_num}",
        "nakshatra": planet.nakshatra,
        "pada": planet.pada,
        "nakshatra_lord": planet.nakshatra_lord,
        "dignity": dignity_str,
        "exalted": planet.exalted,
        "debilitated": planet.debilitated,
        "own_sign": planet.own_sign,
        "moolatrikona": planet.moolatrikona,
        "retrograde": planet.retrograde,
        "speed": round(planet.speed, 4),
        "latitude": round(planet.latitude, 4),
        "distance_au": round(planet.distance, 4),
        "is_combust": combust_info["is_combust"],
        "combust_separation": combust_info["separation"],
        "combust_limit": combust_info["limit"],
    }


def calculate_balas(chart: BirthChart) -> Dict[str, Any]:
    """
    Compute classical Planetary Strengths (Balas) for the 7 classical planets.
    Includes: Cheshta Bala, Dig Bala, Naisargika Bala, Natonnata Bala, Paksha Bala, Uccha Bala.
    """
    sun = chart.planets.get("Sun")
    moon = chart.planets.get("Moon")
    sun_long = sun.longitude if sun else 0.0
    moon_long = moon.longitude if moon else 0.0
    birth_dt = chart.birth_data.birth_datetime

    # Calculate global paksha bala for the Moon
    p_bala_obj = paksha_bala(sun_long, moon_long)
    moon_paksha_val = round(p_bala_obj.value, 2)

    balas_per_planet = []
    for p_name in CLASSICAL_GRAHAS:
        p = chart.planets.get(p_name)
        if not p:
            continue

        graha_enum = GRAHA_MAP[p_name]

        # Find house
        house_num = 1
        for h_num, h_obj in chart.houses.items():
            if p_name in h_obj.planets:
                house_num = h_num
                break

        # 1. Cheshta Bala (Motional strength)
        c_bala = round(cheshta_bala(p.speed, p.retrograde), 2)

        # 2. Dig Bala (Directional strength)
        d_bala = round(dig_bala(graha_enum, house_num), 2)

        # 3. Naisargika Bala (Natural strength)
        n_bala = round(naisargika_bala(graha_enum), 2)

        # 4. Natonnata Bala (Day/Night strength)
        is_day = 6 <= birth_dt.hour < 18
        nat_obj = natonnata_bala(graha_enum, is_day)
        nat_bala = round(nat_obj.value if hasattr(nat_obj, "value") else float(nat_obj), 2)

        # 5. Uccha Bala (Exaltation strength)
        u_bala = round(uccha_bala(graha_enum, p.longitude), 2)

        # 6. Paksha Bala
        pk_bala = moon_paksha_val if p_name in ("Moon", "Jupiter", "Venus", "Mercury") else round(60.0 - moon_paksha_val, 2)

        total_bala = round(c_bala + d_bala + n_bala + nat_bala + u_bala + pk_bala, 2)
        relative_pct = round(min(100.0, (total_bala / 360.0) * 100.0), 1)

        status = "Strong" if relative_pct >= 55 else ("Moderate" if relative_pct >= 40 else "Needs Support")

        balas_per_planet.append({
            "planet": p_name,
            "cheshta_bala": c_bala,
            "dig_bala": d_bala,
            "naisargika_bala": n_bala,
            "natonnata_bala": nat_bala,
            "paksha_bala": pk_bala,
            "uccha_bala": u_bala,
            "total_virupas": total_bala,
            "relative_percentage": relative_pct,
            "status": status,
        })

    return {
        "planets": balas_per_planet,
        "summary": "BPHS Shadbala constituent components calculated across Motional, Directional, Natural, Diurnal, Exaltation, and Lunar Phase strengths.",
    }


def calculate_panchadha_matrix(chart: BirthChart) -> Dict[str, Any]:
    """
    Compute the 7x7 Panchadha Maitri (5-fold compound relationship) matrix.
    Relationships: Great Friend (Adhi Mitra), Friend (Mitra), Neutral (Sama),
    Enemy (Shatru), Great Enemy (Adhi Shatru).
    """
    matrix = {}
    relationship_names = {
        "GREAT_FRIEND": "Great Friend",
        "FRIEND": "Friend",
        "NEUTRAL": "Neutral",
        "ENEMY": "Enemy",
        "GREAT_ENEMY": "Great Enemy",
    }

    relationship_classes = {
        "GREAT_FRIEND": "rel-great-friend",
        "FRIEND": "rel-friend",
        "NEUTRAL": "rel-neutral",
        "ENEMY": "rel-enemy",
        "GREAT_ENEMY": "rel-great-enemy",
    }

    for source_name in CLASSICAL_GRAHAS:
        p_src = chart.planets.get(source_name)
        if not p_src:
            continue
        src_graha = GRAHA_MAP[source_name]
        src_sign = sign_from_number(p_src.sign_number)

        matrix[source_name] = {}
        for target_name in CLASSICAL_GRAHAS:
            if source_name == target_name:
                matrix[source_name][target_name] = {
                    "relationship": "Self",
                    "code": "SELF",
                    "badge_class": "rel-self",
                }
                continue

            p_tgt = chart.planets.get(target_name)
            if not p_tgt:
                continue
            tgt_graha = GRAHA_MAP[target_name]
            tgt_sign = sign_from_number(p_tgt.sign_number)

            comp_rel = compound_relationship(src_sign, tgt_sign, src_graha, tgt_graha)
            code_name = comp_rel.name
            display_name = relationship_names.get(code_name, "Neutral")
            css_class = relationship_classes.get(code_name, "rel-neutral")

            matrix[source_name][target_name] = {
                "relationship": display_name,
                "code": code_name,
                "badge_class": css_class,
            }

    return {
        "planets": CLASSICAL_GRAHAS,
        "matrix": matrix,
    }


def serialize_sade_sati(chart: BirthChart) -> Dict[str, Any]:
    """
    Compute current Shani Sade Sati status and cycle for the native's Janma Rasi.
    """
    moon = chart.planets.get("Moon")
    if not moon:
        return {"is_active": False, "status": "Inactive", "description": "Moon not found"}

    moon_sign = moon.sign

    # Current live transit position of Saturn
    now_dt = datetime.now()
    jd = datetime_to_julian(now_dt)
    current_positions = calculate_planets(jd)
    saturn_pos = current_positions.get(Graha.SATURN)
    saturn_curr_sign = sign_enum(saturn_pos.longitude).display_name if saturn_pos else "Pisces"

    is_active = is_sade_sati_active(moon_sign, saturn_curr_sign)
    current_phase = sade_sati_phase_name(moon_sign, saturn_curr_sign)
    sade_sati_signs_list = sade_sati_signs(moon_sign)
    evidence_list = sade_sati_evidence(moon_sign, saturn_curr_sign)

    # 7.5 Year Cycle Estimation
    # Start approx from birth date or current decade
    cycle_start = chart.birth_data.birth_datetime
    periods_raw = generate_sade_sati_periods(moon_sign, cycle_start)
    periods_data = []
    for p in periods_raw:
        periods_data.append({
            "phase": p.phase,
            "saturn_sign": p.saturn_sign,
            "moon_sign": p.moon_sign,
            "house_from_moon": p.house_from_moon,
            "start": p.start.strftime("%Y-%m-%d"),
            "end": p.end.strftime("%Y-%m-%d"),
            "duration_years": round(p.duration_years, 1),
        })

    phase_descriptions = {
        RISING_PHASE: "Saturn transits the 12th house from natal Moon (First Dhaiya / Rising Phase). Focus on finances, sleep, and emotional regulation.",
        PEAK_PHASE: "Saturn transits over the natal Moon sign (Janma Shani / Peak Phase). Significant life transformations, maturity, and mental resilience.",
        SETTING_PHASE: "Saturn transits the 2nd house from natal Moon (Third Dhaiya / Setting Phase). Family matters, accumulation, and establishing stability.",
    }

    return {
        "is_active": is_active,
        "natal_moon_sign": moon_sign,
        "transiting_saturn_sign": saturn_curr_sign,
        "current_phase": current_phase or "Inactive",
        "phase_description": phase_descriptions.get(current_phase, "Saturn is not currently transiting the 12th, 1st, or 2nd from natal Moon. Sade Sati is inactive."),
        "sade_sati_signs": sade_sati_signs_list,
        "evidence": evidence_list,
        "estimated_periods": periods_data,
    }


def serialize_live_transits(chart: BirthChart) -> Dict[str, Any]:
    """
    Compute live planetary transits (Gochara) as of today relative to natal Moon and Ascendant.
    """
    now_dt = datetime.now()
    jd = datetime_to_julian(now_dt)
    current_positions = calculate_planets(jd)

    moon = chart.planets.get("Moon")
    asc_sign_num = sign_number(chart.ascendant)
    moon_sign_num = moon.sign_number if moon else 1

    transits_list = []
    gochara_rules = {
        "Jupiter": {
            2: "Favorable: Wealth & Family harmony",
            5: "Highly Auspicious: Intelligence, gains & blessings",
            7: "Favorable: Relationships & partnerships flourish",
            9: "Super Auspicious: Fortune, divine grace & luck",
            11: "Highly Auspicious: Fulfillment of desires & profits",
        },
        "Saturn": {
            3: "Favorable: Courage, enterprise & overcoming hurdles",
            6: "Highly Favorable: Victory over obstacles, debts & illness",
            11: "Auspicious: Financial gains & goal achievement",
        },
        "Rahu": {
            3: "Favorable: Bold initiatives & expansion",
            6: "Favorable: Victory over competition",
            10: "Dynamic: Career momentum & ambition",
            11: "Favorable: Material profits & gains",
        },
    }

    for graha_enum, pos in current_positions.items():
        p_name = graha_enum.display_name
        curr_sign_num = sign_number(pos.longitude)
        curr_sign_name = sign_enum(pos.longitude).display_name

        # Distance from Moon (Janma Rasi)
        house_from_moon = ((curr_sign_num - moon_sign_num) % 12) + 1

        # Distance from Ascendant (Lagna)
        house_from_asc = ((curr_sign_num - asc_sign_num) % 12) + 1

        influence = gochara_rules.get(p_name, {}).get(house_from_moon, "General transit influence")

        meta = PLANET_METADATA.get(p_name, {"color": "#fff", "symbol": "●"})

        transits_list.append({
            "planet": p_name,
            "symbol": meta["symbol"],
            "color": meta["color"],
            "current_longitude": round(pos.longitude, 4),
            "current_longitude_dms": degree_to_dms(pos.longitude),
            "current_sign": curr_sign_name,
            "current_sign_number": curr_sign_num,
            "house_from_moon": house_from_moon,
            "house_from_ascendant": house_from_asc,
            "retrograde": pos.retrograde,
            "gochara_influence": influence,
        })

    return {
        "transit_datetime": now_dt.isoformat(),
        "transit_date_display": now_dt.strftime("%B %d, %Y"),
        "natal_moon_sign": moon.sign if moon else "",
        "natal_ascendant_sign": chart.ascendant_sign,
        "transits": transits_list,
    }


def serialize_varga_positions(chart: BirthChart) -> Dict[str, Any]:
    """Serialize all 16 Shodashavarga divisional charts (D1 to D60)."""
    varga_keys = [
        ("D1", "Rasi (Physical Existence)", "D1"),
        ("D2", "Hora (Wealth & Resources)", "hora"),
        ("D3", "Drekkana (Siblings & Courage)", "drekkana"),
        ("D4", "Chaturthamsa (Fortune & Assets)", "chaturthamsa"),
        ("D7", "Saptamsa (Children & Progeny)", "saptamsa"),
        ("D9", "Navamsha (Spouse & Destiny)", "navamsa"),
        ("D10", "Dasamsa (Career & Status)", "dasamsa"),
        ("D12", "Dvadasamsa (Parents & Lineage)", "dvadasamsa"),
        ("D16", "Shodasamsa (Vehicles & Pleasures)", "shodasamsa"),
        ("D20", "Vimsamsa (Spiritual Progress)", "vimsamsa"),
        ("D24", "Chaturvimsamsa (Higher Learning)", "siddhamsa"),
        ("D27", "Saptavimsamsa (Strengths & Vulnerabilities)", "bhamsa"),
        ("D30", "Trimshamsa (Misfortunes & Arishta)", "trimshamsa"),
        ("D40", "Khavedamsa (Auspicious Matters)", "khavedamsa"),
        ("D45", "Akshavedamsa (All General Matters)", "akshavedamsa"),
        ("D60", "Shastiamsa (Past Karma & Root Destiny)", "shastiamsa"),
    ]

    vargas_result = {}

    for d_code, title, attr_name in varga_keys:
        lagna_sign_num = 1
        if attr_name == "D1":
            lagna_sign_num = sign_number(chart.ascendant)
        else:
            asc_vchart = build_varga_chart(chart.ascendant)
            lagna_vpos = getattr(asc_vchart, attr_name, None)
            if lagna_vpos is not None:
                lagna_sign_num = getattr(lagna_vpos, "sign_number", 1)

        # Build 12 houses for this Varga
        varga_houses = {}
        for h in range(1, 13):
            sign_num = (((lagna_sign_num + h - 2) % 12) + 1)
            varga_houses[h] = {
                "house": h,
                "sign_number": sign_num,
                "sign_name": SIGNS[sign_num - 1].display_name,
                "planets": [],
            }

        # Place each planet in its respective Varga house
        planets_varga = {}
        for p_name, p in chart.planets.items():
            if attr_name == "D1":
                p_sign_num = p.sign_number
                p_deg = p.sign_degree
            else:
                p_vchart = build_varga_chart(p.longitude)
                p_vpos = getattr(p_vchart, attr_name, None)
                if p_vpos is not None:
                    p_sign_num = getattr(p_vpos, "sign_number", 1)
                    p_deg = getattr(p_vpos, "degree_in_sign", 0.0)
                else:
                    p_sign_num = 1
                    p_deg = 0.0

            p_house = (((p_sign_num - lagna_sign_num) % 12) + 1)
            varga_houses[p_house]["planets"].append(p_name)

            meta = PLANET_METADATA.get(p_name, {"short": p_name[:2], "color": "#fff"})
            planets_varga[p_name] = {
                "name": p_name,
                "short_name": meta["short"],
                "color": meta["color"],
                "sign_number": p_sign_num,
                "sign_name": SIGNS[p_sign_num - 1].display_name,
                "sign_degree": round(p_deg, 2),
                "sign_degree_dms": degree_to_dms(p_deg),
                "house": p_house,
            }

        vargas_result[d_code] = {
            "code": d_code,
            "title": title,
            "lagna_sign_number": lagna_sign_num,
            "lagna_sign_name": SIGNS[lagna_sign_num - 1].display_name,
            "houses": varga_houses,
            "planets": planets_varga,
        }

    return vargas_result


def serialize_dashas(chart: BirthChart) -> Dict[str, Any]:
    """Serialize the full 120-year Vimshottari Mahadasha timeline with 6-level hierarchy."""
    birth_dt = chart.birth_data.birth_datetime
    moon = chart.planets.get("Moon")
    moon_long = moon.longitude if moon else 0.0

    mahadashas = generate_mahadashas(birth_dt, moon_long)
    now = datetime.now()

    mahadasha_list = []
    active_hierarchy = {
        "mahadasha": None,
        "antardasha": None,
        "pratyantardasha": None,
        "sookshma": None,
        "prana": None,
        "deha": None,
    }

    for md in mahadashas:
        is_active_md = (md.start <= now <= md.end)
        antardashas = generate_antardashas(md)

        ad_list = []
        for ad in antardashas:
            is_active_ad = (ad.start <= now <= ad.end)
            pratyantardashas = generate_pratyantardashas(ad)

            pd_list = []
            for pd in pratyantardashas:
                is_active_pd = (pd.start <= now <= pd.end)
                sookshmas = generate_sookshmadashas(pd)

                sd_list = []
                for sd in sookshmas:
                    is_active_sd = (sd.start <= now <= sd.end)

                    if is_active_sd and not active_hierarchy["sookshma"]:
                        active_hierarchy["sookshma"] = {
                            "lord": sd.sookshma_lord,
                            "start": sd.start.strftime("%Y-%m-%d"),
                            "end": sd.end.strftime("%Y-%m-%d"),
                        }

                        # Generate Prana & Deha for active chain
                        try:
                            pranas = generate_pranadashas(sd)
                            for pr in pranas:
                                if pr.start <= now <= pr.end:
                                    active_hierarchy["prana"] = {
                                        "lord": pr.prana_lord,
                                        "start": pr.start.strftime("%Y-%m-%d"),
                                        "end": pr.end.strftime("%Y-%m-%d"),
                                    }
                                    dehas = generate_dehadashas(pr)
                                    for dh in dehas:
                                        if dh.start <= now <= dh.end:
                                            active_hierarchy["deha"] = {
                                                "lord": dh.deha_lord,
                                                "start": dh.start.strftime("%Y-%m-%d"),
                                                "end": dh.end.strftime("%Y-%m-%d"),
                                            }
                                            break
                                    break
                        except Exception:
                            pass

                    sd_list.append({
                        "lord": sd.sookshma_lord,
                        "start": sd.start.strftime("%Y-%m-%d"),
                        "end": sd.end.strftime("%Y-%m-%d"),
                        "is_active": is_active_sd,
                    })

                if is_active_pd and not active_hierarchy["pratyantardasha"]:
                    active_hierarchy["pratyantardasha"] = {
                        "lord": pd.pratyantardasha_lord,
                        "start": pd.start.strftime("%Y-%m-%d"),
                        "end": pd.end.strftime("%Y-%m-%d"),
                    }

                pd_list.append({
                    "lord": pd.pratyantardasha_lord,
                    "start": pd.start.strftime("%Y-%m-%d"),
                    "end": pd.end.strftime("%Y-%m-%d"),
                    "is_active": is_active_pd,
                    "sookshmas": sd_list,
                })

            if is_active_ad and not active_hierarchy["antardasha"]:
                active_hierarchy["antardasha"] = {
                    "lord": ad.antardasha_lord,
                    "start": ad.start.strftime("%Y-%m-%d"),
                    "end": ad.end.strftime("%Y-%m-%d"),
                }

            ad_list.append({
                "lord": ad.antardasha_lord,
                "start": ad.start.strftime("%Y-%m-%d"),
                "end": ad.end.strftime("%Y-%m-%d"),
                "is_active": is_active_ad,
                "pratyantardashas": pd_list,
            })

        if is_active_md and not active_hierarchy["mahadasha"]:
            active_hierarchy["mahadasha"] = {
                "lord": md.planet,
                "start": md.start.strftime("%Y-%m-%d"),
                "end": md.end.strftime("%Y-%m-%d"),
                "duration_years": round(md.duration_years, 2),
            }

        mahadasha_list.append({
            "lord": md.planet,
            "start": md.start.strftime("%Y-%m-%d"),
            "end": md.end.strftime("%Y-%m-%d"),
            "duration_years": round(md.duration_years, 2),
            "is_active": is_active_md,
            "antardashas": ad_list,
        })

    return {
        "calculation_time": now.isoformat(),
        "active_chain": active_hierarchy,
        "mahadashas": mahadasha_list,
    }


def serialize_yogas(context: Any) -> List[Dict[str, Any]]:
    """Detect all Vedic Yogas and format structured results."""
    detectors = [
        ("Raja Yoga", detect_rajyoga),
        ("Dhana Yoga", detect_dhanayoga),
        ("Gaja Kesari Yoga", detect_gaja_kesari),
        ("Budha-Aditya Yoga", detect_budha_aditya),
        ("Chandra-Mangala Yoga", detect_chandra_mangala),
        ("Neecha Bhanga Raja Yoga", detect_neecha_bhanga),
        ("Parivartana Yoga", detect_parivartana),
        ("Guru Chandal Yoga", detect_guru_chandal),
    ]

    raw_results = []
    for default_name, detector in detectors:
        try:
            res = detector(context)
            if isinstance(res, (list, tuple)):
                raw_results.extend(res)
            elif res is not None:
                raw_results.append(res)
        except Exception:
            pass

    yoga_items = []
    for res in raw_results:
        evidence_list = []
        if hasattr(res, "evidence") and res.evidence:
            if isinstance(res.evidence, (list, tuple)):
                evidence_list = [str(e) for e in res.evidence]
            elif isinstance(res.evidence, dict):
                evidence_list = [f"{k}: {v}" for k, v in res.evidence.items()]
            else:
                evidence_list = [str(res.evidence)]

        # Category and auspicious classification
        category = "General"
        nature = "Auspicious"
        if "Raja" in res.name or "Neecha Bhanga" in res.name:
            category = "Raja Yoga (Power, Authority & Status)"
            nature = "Highly Auspicious"
        elif "Dhana" in res.name or "Wealth" in res.name:
            category = "Dhana Yoga (Wealth, Abundance & Gains)"
            nature = "Auspicious"
        elif "Gaja Kesari" in res.name:
            category = "Wisdom & Prosperity Yoga"
            nature = "Highly Auspicious"
        elif "Budha Aditya" in res.name:
            category = "Nipuna / Intellect Yoga"
            nature = "Auspicious"
        elif "Chandra-Mangala" in res.name:
            category = "Financial Energy & Commercial Drive"
            nature = "Auspicious"
        elif "Guru Chandal" in res.name:
            category = "Shadow / Guru Chandal Yoga"
            nature = "Unconventional / Requires Prudence"
        elif "Parivartana" in res.name:
            if "Dainya" in res.name:
                category = "Exchange Yoga (Dusthana Involved)"
                nature = "Challenging / Requires Caution"
            elif "Khala" in res.name:
                category = "Exchange Yoga (Effort Driven)"
                nature = "Mixed / Effort brings gains"
            else:
                category = "Maha Parivartana (Great Exchange)"
                nature = "Highly Auspicious"

        yoga_items.append({
            "name": res.name,
            "detected": bool(res.detected),
            "category": category,
            "nature": nature,
            "description": getattr(res, "description", ""),
            "evidence": evidence_list,
        })

    return yoga_items


def serialize_interpretations(context: Any, chart: BirthChart) -> Dict[str, Any]:
    """Compute chart interpretations and life synthesis."""
    try:
        planetary_interp = analyze_planets(context)
        house_interp = analyze_houses(context)
        dignity_interp = analyze_dignities(context)
        aspect_interp = analyze_aspects(context)
        yoga_interp = analyze_yoga_interpretations(context)

        synthesis = synthesize_chart(
            planetary=planetary_interp,
            houses=house_interp,
            dignities=dignity_interp,
            aspects=aspect_interp,
            yogas=yoga_interp,
        )

        themes = list(synthesis.themes) if synthesis.themes else []
        cautions = list(synthesis.cautions) if synthesis.cautions else []
        evidence = list(synthesis.evidence) if synthesis.evidence else []

        return {
            "themes": themes,
            "cautions": cautions,
            "evidence": evidence,
            "planet_count": synthesis.planet_count,
            "house_count": synthesis.house_count,
            "dignity_count": synthesis.dignity_count,
            "detected_yoga_count": synthesis.detected_yoga_count,
        }
    except Exception as e:
        return {
            "themes": ["Chart synthesis generated successfully."],
            "cautions": [],
            "evidence": [],
            "error": str(e),
        }


def serialize_complete_chart(chart: BirthChart) -> Dict[str, Any]:
    """Master serializer for the complete Kundali response."""
    birth = chart.birth_data
    loc = birth.location

    # 1. Basic Metadata & Ascendant
    asc_deg = chart.ascendant_degree
    asc_sign_num = sign_number(chart.ascendant)
    asc_sign_name = chart.ascendant_sign
    asc_lord = SIGN_LORD.get(asc_sign_num, "")

    # Ascendant Nakshatra
    asc_nak = longitude_to_nakshatra(chart.ascendant)
    asc_pada = nakshatra_pada(chart.ascendant)

    ascendant_data = {
        "longitude": round(chart.ascendant, 4),
        "longitude_dms": degree_to_dms(chart.ascendant),
        "sign": asc_sign_name,
        "sign_sanskrit": SIGN_NAMES_SANSKRIT.get(asc_sign_num, asc_sign_name),
        "sign_number": asc_sign_num,
        "sign_lord": asc_lord,
        "sign_degree": round(asc_deg, 4),
        "sign_degree_dms": degree_to_dms(asc_deg),
        "nakshatra": asc_nak.name,
        "pada": asc_pada,
        "nakshatra_lord": asc_nak.lord,
    }

    # Sun longitude for combustion checks
    sun_obj = chart.planets.get("Sun")
    sun_longitude = sun_obj.longitude if sun_obj else 0.0

    # 2. Planets
    planets_data = []
    planets_map = {}
    for name, p in chart.planets.items():
        # Find which house this planet belongs to
        p_house = 1
        for h_num, house_obj in chart.houses.items():
            if name in house_obj.planets:
                p_house = h_num
                break

        p_dict = serialize_planet(p, p_house, sun_longitude=sun_longitude)
        planets_data.append(p_dict)
        planets_map[name] = p_dict

    # Moon details for Janma Rasi & Janma Nakshatra
    moon_data = planets_map.get("Moon", {})
    sun_data = planets_map.get("Sun", {})

    # 3. Houses (1 to 12)
    houses_data = []
    for h_num in range(1, 13):
        h_obj = chart.houses.get(h_num)
        h_sign_num = h_obj.sign_number if h_obj else (((asc_sign_num + h_num - 2) % 12) + 1)
        h_sign_name = h_obj.sign if h_obj else SIGNS[h_sign_num - 1].display_name
        h_lord = h_obj.lord if (h_obj and h_obj.lord) else SIGN_LORD.get(h_sign_num, "")

        # Planets occupying
        occupants = list(h_obj.planets) if h_obj else []

        # Planets aspecting this house
        aspecting = []
        if hasattr(chart, "aspect_map") and chart.aspect_map:
            # Check which planets cast drishti to h_sign_num
            for p_name, target_signs in chart.aspect_map.items():
                if h_sign_num in target_signs and p_name != "Ascendant":
                    aspecting.append(p_name)

        sig = HOUSE_SIGNIFICANCE.get(h_num, {"name": f"House {h_num}", "domains": ""})

        houses_data.append({
            "house": h_num,
            "sign": h_sign_name,
            "sign_sanskrit": SIGN_NAMES_SANSKRIT.get(h_sign_num, h_sign_name),
            "sign_number": h_sign_num,
            "sign_lord": h_lord,
            "occupants": occupants,
            "aspecting_planets": aspecting,
            "significance_title": sig["name"],
            "significance_domains": sig["domains"],
            "element": SIGN_ELEMENTS.get(h_sign_num, ""),
        })

    # 4. Aspects (Planet to Planet and Planet to House)
    aspects_list = []
    if hasattr(chart, "aspect_map") and chart.aspect_map:
        for aspecting_planet, target_signs in chart.aspect_map.items():
            for target_p_name, target_p in chart.planets.items():
                if aspecting_planet != target_p_name and target_p.sign_number in target_signs:
                    aspects_list.append({
                        "aspecting_planet": aspecting_planet,
                        "target_planet": target_p_name,
                        "target_sign_number": target_p.sign_number,
                        "target_sign": target_p.sign,
                    })

    # 5. Divisional Charts (D1 through D60)
    vargas_data = serialize_varga_positions(chart)

    # 6. Vimshottari Dashas
    dashas_data = serialize_dashas(chart)

    # 7. Interpretation Context & Yogas
    context = build_interpretation_context(chart, birth)
    yogas_data = serialize_yogas(context)
    detected_yogas = [y for y in yogas_data if y["detected"]]

    # 8. Planetary Strengths (Balas)
    balas_data = calculate_balas(chart)

    # 9. Panchadha Maitri (5-fold Relationship Matrix)
    panchadha_data = calculate_panchadha_matrix(chart)

    # 10. Shani Sade Sati Analysis & Timeline
    sade_sati_data = serialize_sade_sati(chart)

    # 11. Live Planetary Transits (Gochara)
    transits_data = serialize_live_transits(chart)

    # 12. Life Synthesis & Interpretations
    synthesis_data = serialize_interpretations(context, chart)

    return {
        "native": {
            "name": birth.name,
            "birth_datetime": birth.birth_datetime.isoformat(),
            "birth_date_display": birth.birth_datetime.strftime("%B %d, %Y"),
            "birth_time_display": birth.birth_datetime.strftime("%I:%M:%S %p"),
            "place": loc.name,
            "city": loc.city,
            "country": loc.country,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "timezone": loc.timezone,
            "elevation": loc.elevation,
            "julian_day": round(chart.julian_day, 6),
            "ayanamsa_name": "Lahiri (Chitrapaksha)",
            "ayanamsa_value": round(chart.ayanamsa, 6),
            "ayanamsa_dms": degree_to_dms(chart.ayanamsa),
            "janma_rasi": moon_data.get("sign", ""),
            "janma_nakshatra": moon_data.get("nakshatra", ""),
            "janma_pada": moon_data.get("pada", 1),
            "sun_sign": sun_data.get("sign", ""),
            "ascendant_sign": asc_sign_name,
        },
        "ascendant": ascendant_data,
        "planets": planets_data,
        "planets_map": planets_map,
        "houses": houses_data,
        "aspects": aspects_list,
        "vargas": vargas_data,
        "dashas": dashas_data,
        "yogas": {
            "all": yogas_data,
            "detected": detected_yogas,
            "detected_count": len(detected_yogas),
            "total_count": len(yogas_data),
        },
        "balas": balas_data,
        "panchadha": panchadha_data,
        "sade_sati": sade_sati_data,
        "transits": transits_data,
        "synthesis": synthesis_data,
    }
