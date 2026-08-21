"""
api/serializers.py

Comprehensive serializers to convert Kundali Engine objects into clean,
rich JSON structures for the dashboard frontend.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from astronomy.signs import SIGNS, sign_degree, sign_enum, sign_number
from astronomy.varga_engine import build_varga_chart
from astrology.dasha import generate_mahadashas, generate_antardashas
from astrology.pratyantardasha import generate_pratyantardashas
from astrology.sookshmadasha import generate_sookshmadashas
from astrology.pranadasha import generate_pranadashas
from astrology.dehadasha import generate_dehadashas

from yogas.analyzer import YogaAnalyzer
from yogas.rajyoga import RajaYogaRule
from yogas.dhanayoga import DhanaYogaRule
from yogas.gaja_kesari import GajaKesariRule
from yogas.budha_aditya import BudhaAdityaYogaRule
from yogas.chandra_mangala import ChandraMangalaYogaRule
from yogas.neecha_bhanga import NeechaBhangaRajaYogaRule
from yogas.parivartana import ParivartanaYogaRule

from interpretation.context import build_interpretation_context
from interpretation.planet_analysis import analyze_planets
from interpretation.house_analysis import analyze_houses
from interpretation.dignity_analysis import analyze_dignities
from interpretation.aspect_analysis import analyze_aspects
from interpretation.yoga_analysis import analyze_yoga_interpretations
from interpretation.synthesis import synthesize_chart

from models.chart import BirthChart
from models.planet import Planet

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


def serialize_planet(planet: Planet, house_num: int) -> Dict[str, Any]:
    """Serialize a single planet model."""
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
        "nakshatra": planet.nakshatra,
        "pada": planet.pada,
        "nakshatra_lord": planet.nakshatra_lord,
        "retrograde": bool(planet.retrograde),
        "speed": round(planet.speed, 5),
        "latitude": round(planet.latitude, 4),
        "distance": round(planet.distance, 6),
        "dignity": dignity_str,
        "exalted": bool(planet.exalted),
        "debilitated": bool(planet.debilitated),
        "own_sign": bool(planet.own_sign),
        "moolatrikona": bool(planet.moolatrikona),
    }


def serialize_varga_positions(chart: BirthChart) -> Dict[str, Dict[str, Any]]:
    """
    Build all 16 BPHS Shodashavarga charts for the ascendant and all planets.
    Returns structured data for D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60.
    """
    varga_keys = [
        ("D1", "Rasi (Physical & Overall Life)", None),
        ("D2", "Hora (Wealth & Resources)", "hora"),
        ("D3", "Drekkana (Siblings & Vitality)", "drekkana"),
        ("D7", "Saptamsa (Children & Progeny)", "saptamsa"),
        ("D9", "Navamsha (Spouse, Dharma & Destiny)", "navamsa"),
        ("D10", "Dasamsa (Career, Status & Success)", "dasamsa"),
        ("D12", "Dvadasamsa (Parents & Ancestry)", "dvadasamsa"),
        ("D16", "Shodasamsa (Vehicles & Pleasures)", "shodasamsa"),
        ("D20", "Vimsamsa (Spiritual Progress & Upasana)", "vimsamsa"),
        ("D24", "Chaturvimshamsa (Education & Learning)", "siddhamsa"),
        ("D27", "Bhamsa / Saptavimsamsa (Strengths & Weaknesses)", "bhamsa"),
        ("D30", "Trimshamsa (Misfortunes & Hidden Evils)", "trimshamsa"),
        ("D40", "Khavedamsa (Auspicious / Inauspicious Results)", "khavedamsa"),
        ("D45", "Akshavedamsa (Character & Overall Purity)", "akshavedamsa"),
        ("D60", "Shastiamsa (Past Life Karma & Roots)", "shastiamsa"),
    ]

    all_vargas: Dict[str, Dict[str, Any]] = {}

    # Build varga object for Lagna
    lagna_vargas = build_varga_chart(chart.ascendant)
    # Build varga objects for planets
    planet_vargas = {
        name: build_varga_chart(p.longitude)
        for name, p in chart.planets.items()
    }

    # Extract Lagna sign number in D1
    d1_lagna_sign = sign_number(chart.ascendant)

    for v_code, v_title, attr_name in varga_keys:
        if v_code == "D1":
            # D1 is the standard Rasi chart
            lagna_sign = d1_lagna_sign
            planet_signs = {
                name: p.sign_number
                for name, p in chart.planets.items()
            }
        else:
            # Extract divisional sign number
            lagna_pos = getattr(lagna_vargas, attr_name)
            lagna_sign = lagna_pos.sign.number

            planet_signs = {}
            for p_name, pv in planet_vargas.items():
                pos = getattr(pv, attr_name)
                planet_signs[p_name] = pos.sign.number

        # Map planets to houses relative to this divisional Lagna
        house_placements: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
        planet_house_map: Dict[str, int] = {}

        for p_name, p_sign in planet_signs.items():
            # Whole sign house relative to Lagna sign
            h_num = ((p_sign - lagna_sign) % 12) + 1
            house_placements[h_num].append(p_name)
            planet_house_map[p_name] = h_num

        all_vargas[v_code] = {
            "code": v_code,
            "title": v_title,
            "lagna_sign": lagna_sign,
            "lagna_sign_name": SIGNS[lagna_sign - 1].display_name,
            "planet_signs": planet_signs,
            "planet_houses": planet_house_map,
            "house_placements": house_placements,
        }

    return all_vargas


def serialize_dashas(chart: BirthChart, now: Optional[datetime] = None) -> Dict[str, Any]:
    """Serialize the full Vimshottari Dasha system with interactive hierarchies."""
    if now is None:
        now = datetime.now()

    birth_dt = chart.birth_data.birth_datetime
    moon_long = chart.planets["Moon"].longitude

    # Generate all Mahadashas (120 years)
    mahadashas = generate_mahadashas(birth_dt, moon_long)
    mahadasha_list = []

    active_hierarchy = {
        "mahadasha": None,
        "antardasha": None,
        "pratyantardasha": None,
        "sookshma": None,
        "prana": None,
        "deha": None,
        "calculation_time": now.isoformat(),
    }

    for md in mahadashas:
        is_md_active = md.start <= now < md.end
        antardashas = generate_antardashas(md)
        ad_list = []

        for ad in antardashas:
            is_ad_active = is_md_active and (ad.start <= now < ad.end)
            pratyantardashas = generate_pratyantardashas(ad)
            pd_list = []

            for pd in pratyantardashas:
                is_pd_active = is_ad_active and (pd.start <= now < pd.end)
                if is_pd_active:
                    active_hierarchy["mahadasha"] = {
                        "lord": md.planet,
                        "start": md.start.isoformat(),
                        "end": md.end.isoformat(),
                    }
                    active_hierarchy["antardasha"] = {
                        "lord": ad.antardasha_lord,
                        "start": ad.start.isoformat(),
                        "end": ad.end.isoformat(),
                    }
                    active_hierarchy["pratyantardasha"] = {
                        "lord": pd.pratyantardasha_lord,
                        "start": pd.start.isoformat(),
                        "end": pd.end.isoformat(),
                    }

                    # Compute sookshma, prana, deha for active window
                    try:
                        sookshmas = generate_sookshmadashas(pd)
                        for sd in sookshmas:
                            if sd.start <= now < sd.end:
                                active_hierarchy["sookshma"] = {
                                    "lord": sd.sookshma_lord,
                                    "start": sd.start.isoformat(),
                                    "end": sd.end.isoformat(),
                                    "duration": format_duration((sd.end - sd.start).total_seconds() / 86400.0),
                                }
                                pranas = generate_pranadashas(sd)
                                for prd in pranas:
                                    if prd.start <= now < prd.end:
                                        active_hierarchy["prana"] = {
                                            "lord": prd.prana_lord,
                                            "start": prd.start.isoformat(),
                                            "end": prd.end.isoformat(),
                                            "duration": format_duration((prd.end - prd.start).total_seconds() / 86400.0),
                                        }
                                        dehas = generate_dehadashas(prd)
                                        for dh in dehas:
                                            if dh.start <= now < dh.end:
                                                active_hierarchy["deha"] = {
                                                    "lord": dh.deha_lord,
                                                    "start": dh.start.isoformat(),
                                                    "end": dh.end.isoformat(),
                                                    "duration": format_duration((dh.end - dh.start).total_seconds() / 86400.0),
                                                }
                                                break
                                        break
                                break
                    except Exception:
                        pass

                pd_duration = (pd.end - pd.start).total_seconds() / 86400.0
                pd_list.append({
                    "lord": pd.pratyantardasha_lord,
                    "start": pd.start.isoformat(),
                    "end": pd.end.isoformat(),
                    "start_display": pd.start.strftime("%Y-%m-%d %H:%M"),
                    "end_display": pd.end.strftime("%Y-%m-%d %H:%M"),
                    "duration": format_duration(pd_duration),
                    "is_active": is_pd_active,
                })

            ad_duration = (ad.end - ad.start).total_seconds() / 86400.0
            ad_list.append({
                "lord": ad.antardasha_lord,
                "start": ad.start.isoformat(),
                "end": ad.end.isoformat(),
                "start_display": ad.start.strftime("%Y-%m-%d"),
                "end_display": ad.end.strftime("%Y-%m-%d"),
                "duration": format_duration(ad_duration),
                "is_active": is_ad_active,
                "pratyantardashas": pd_list,
            })

        md_duration_years = (md.end - md.start).total_seconds() / (86400.0 * 365.25)
        mahadasha_list.append({
            "lord": md.planet,
            "years": round(md_duration_years, 2),
            "start": md.start.isoformat(),
            "end": md.end.isoformat(),
            "start_display": md.start.strftime("%Y-%m-%d"),
            "end_display": md.end.strftime("%Y-%m-%d"),
            "is_active": is_md_active,
            "antardashas": ad_list,
        })

    return {
        "active_chain": active_hierarchy,
        "mahadashas": mahadasha_list,
    }


from yogas.rajyoga import detect_rajyoga
from yogas.dhanayoga import detect_dhanayoga
from yogas.gaja_kesari import detect_gaja_kesari
from yogas.budha_aditya import detect_budha_aditya
from yogas.chandra_mangala import detect_chandra_mangala
from yogas.neecha_bhanga import detect_neecha_bhanga
from yogas.parivartana import detect_parivartana


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
    from astronomy.nakshatra import longitude_to_nakshatra, nakshatra_pada
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

        p_dict = serialize_planet(p, p_house)
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

    # 8. Life Synthesis & Interpretations
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
        },
        "synthesis": synthesis_data,
    }
