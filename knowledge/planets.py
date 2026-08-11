"""
knowledge/planets.py

Permanent BPHS planetary knowledge database.

This module contains immutable knowledge for the Navagraha.
No chart calculations are performed here.

Compatible with Python 3.9.
"""

from __future__ import annotations

from knowledge.planet import PlanetFacts
from models.graha import Graha

PLANETS = {

    # ==========================================================
    # SUN
    # ==========================================================

    Graha.SUN: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Sun",
        sanskrit_name="Surya",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=False,

        gender="Male",
        element="Fire",
        guna="Sattva",
        caste="Kshatriya",
        temperament="Cruel",
        dosha="Pitta",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="East",
        color="Deep Red",
        metal="Copper",
        gemstone="Ruby",
        deity="Surya",
        weekday="Sunday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Leo",
        ),

        exaltation_sign="Aries",
        exaltation_degree=10.0,

        debilitation_sign="Libra",
        debilitation_degree=10.0,

        moolatrikona_sign="Leo",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Moon",
            "Mars",
            "Jupiter",
        ),

        enemies=(
            "Venus",
            "Saturn",
        ),

        neutrals=(
            "Mercury",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Soul",
            "Father",
            "Authority",
            "Government",
            "Power",
            "Leadership",
            "Fame",
            "Status",
            "Self-esteem",
            "Vitality",
            "Honor",
            "Royalty",
            "Administration",
            "Politics",

        ),

        natural_houses=(
            1,
            9,
            10,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Heart",
            "Bones",
            "Right Eye",
            "Head",
            "Brain",
            "Blood Circulation",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Heart Disease",
            "High Fever",
            "Blood Pressure",
            "Eye Disorders",
            "Headache",
            "Heat Stroke",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Government",
            "Politics",
            "Administration",
            "Leadership",
            "Military",
            "Medicine",
            "Executive",
            "Judge",
            "Royal Service",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "authority",
            "power",
            "confidence",
            "ego",
            "leadership",
            "status",
            "recognition",
            "father",
            "government",
            "honor",
            "willpower",
            "royalty",

        ),

    ),

    # ==========================================================
    # MOON
    # ==========================================================

    Graha.MOON: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Moon",
        sanskrit_name="Chandra",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=True,

        gender="Female",
        element="Water",
        guna="Sattva",
        caste="Vaishya",
        temperament="Gentle",
        dosha="Kapha",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="North-West",
        color="White",
        metal="Silver",
        gemstone="Pearl",
        deity="Chandra",
        weekday="Monday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Cancer",
        ),

        exaltation_sign="Taurus",
        exaltation_degree=3.0,

        debilitation_sign="Scorpio",
        debilitation_degree=3.0,

        moolatrikona_sign="Taurus",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Sun",
            "Mercury",
        ),

        enemies=(),

        neutrals=(
            "Mars",
            "Jupiter",
            "Venus",
            "Saturn",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Mind",
            "Mother",
            "Emotions",
            "Happiness",
            "Public",
            "Memory",
            "Imagination",
            "Nourishment",
            "Travel",
            "Water",
            "Sleep",
            "Mental Peace",
            "Sensitivity",
            "Receptivity",

        ),

        natural_houses=(
            4,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Mind",
            "Brain Fluids",
            "Breasts",
            "Chest",
            "Lungs",
            "Left Eye",
            "Blood Plasma",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Mental Disorders",
            "Depression",
            "Cold",
            "Cough",
            "Water Retention",
            "Insomnia",
            "Chest Disorders",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Hospitality",
            "Nursing",
            "Public Relations",
            "Travel",
            "Shipping",
            "Dairy",
            "Food Industry",
            "Psychology",
            "Counselling",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "mind",
            "mother",
            "emotion",
            "care",
            "compassion",
            "peace",
            "memory",
            "imagination",
            "public",
            "nourishment",
            "home",
            "comfort",

        ),

    ),
        # ==========================================================
    # MARS
    # ==========================================================

    Graha.MARS: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Mars",
        sanskrit_name="Mangala",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=False,

        gender="Male",
        element="Fire",
        guna="Tamas",
        caste="Kshatriya",
        temperament="Cruel",
        dosha="Pitta",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="South",
        color="Red",
        metal="Copper",
        gemstone="Red Coral",
        deity="Skanda",
        weekday="Tuesday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Aries",
            "Scorpio",
        ),

        exaltation_sign="Capricorn",
        exaltation_degree=28.0,

        debilitation_sign="Cancer",
        debilitation_degree=28.0,

        moolatrikona_sign="Aries",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Sun",
            "Moon",
            "Jupiter",
        ),

        enemies=(
            "Mercury",
        ),

        neutrals=(
            "Venus",
            "Saturn",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Courage",
            "Valor",
            "Strength",
            "Energy",
            "Brothers",
            "Land",
            "Property",
            "Weapons",
            "Military",
            "Engineering",
            "Competition",
            "Initiative",
            "Accidents",
            "Surgery",

        ),

        natural_houses=(
            3,
            6,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Blood",
            "Bone Marrow",
            "Muscles",
            "Head",
            "Nose",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Fever",
            "Inflammation",
            "Blood Disorders",
            "Burns",
            "Cuts",
            "Accidents",
            "High Blood Pressure",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Military",
            "Police",
            "Engineering",
            "Civil Engineering",
            "Mechanical Engineering",
            "Construction",
            "Surgeon",
            "Athlete",
            "Firefighter",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "courage",
            "action",
            "strength",
            "discipline",
            "competition",
            "initiative",
            "warrior",
            "engineering",
            "land",
            "property",
            "brothers",
            "energy",

        ),

    ),
        # ==========================================================
    # MERCURY
    # ==========================================================

    Graha.MERCURY: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Mercury",
        sanskrit_name="Budha",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=True,

        gender="Neuter",
        element="Earth",
        guna="Rajas",
        caste="Vaishya",
        temperament="Gentle",
        dosha="Tridosha",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="North",
        color="Green",
        metal="Bronze",
        gemstone="Emerald",
        deity="Vishnu",
        weekday="Wednesday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Gemini",
            "Virgo",
        ),

        exaltation_sign="Virgo",
        exaltation_degree=15.0,

        debilitation_sign="Pisces",
        debilitation_degree=15.0,

        moolatrikona_sign="Virgo",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Sun",
            "Venus",
        ),

        enemies=(
            "Moon",
        ),

        neutrals=(
            "Mars",
            "Jupiter",
            "Saturn",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Intelligence",
            "Speech",
            "Communication",
            "Education",
            "Writing",
            "Mathematics",
            "Commerce",
            "Business",
            "Logic",
            "Analysis",
            "Learning",
            "Memory",
            "Humor",
            "Youth",

        ),

        natural_houses=(
            2,
            6,
            10,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Skin",
            "Nervous System",
            "Tongue",
            "Hands",
            "Arms",
            "Respiratory System",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Skin Disorders",
            "Nervous Disorders",
            "Speech Disorders",
            "Memory Problems",
            "Anxiety",
            "Respiratory Diseases",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Teacher",
            "Writer",
            "Journalist",
            "Accountant",
            "Programmer",
            "Software Engineer",
            "Data Analyst",
            "Business Consultant",
            "Lawyer",
            "Auditor",
            "Statistician",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "intelligence",
            "communication",
            "learning",
            "logic",
            "analysis",
            "business",
            "commerce",
            "writing",
            "technology",
            "calculation",
            "adaptability",
            "curiosity",

        ),

    ),
        # ==========================================================
    # JUPITER
    # ==========================================================

    Graha.JUPITER: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Jupiter",
        sanskrit_name="Brihaspati",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=True,

        gender="Male",
        element="Ether",
        guna="Sattva",
        caste="Brahmin",
        temperament="Gentle",
        dosha="Kapha",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="North-East",
        color="Yellow",
        metal="Gold",
        gemstone="Yellow Sapphire",
        deity="Brihaspati",
        weekday="Thursday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Sagittarius",
            "Pisces",
        ),

        exaltation_sign="Cancer",
        exaltation_degree=5.0,

        debilitation_sign="Capricorn",
        debilitation_degree=5.0,

        moolatrikona_sign="Sagittarius",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Sun",
            "Moon",
            "Mars",
        ),

        enemies=(
            "Mercury",
            "Venus",
        ),

        neutrals=(
            "Saturn",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Wisdom",
            "Knowledge",
            "Spirituality",
            "Religion",
            "Children",
            "Teacher",
            "Guru",
            "Wealth",
            "Prosperity",
            "Justice",
            "Dharma",
            "Charity",
            "Higher Education",
            "Good Fortune",

        ),

        natural_houses=(
            2,
            5,
            9,
            11,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Liver",
            "Fat",
            "Thighs",
            "Arterial System",
            "Growth",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Liver Disorders",
            "Obesity",
            "Diabetes",
            "Tumors",
            "Fat Metabolism Disorders",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Teacher",
            "Professor",
            "Judge",
            "Priest",
            "Guru",
            "Philosopher",
            "Lawyer",
            "Financial Advisor",
            "Banker",
            "Counsellor",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "wisdom",
            "knowledge",
            "dharma",
            "children",
            "wealth",
            "teacher",
            "faith",
            "expansion",
            "fortune",
            "guidance",
            "ethics",
            "prosperity",

        ),

    ),
        # ==========================================================
    # VENUS
    # ==========================================================

    Graha.VENUS: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Venus",
        sanskrit_name="Shukra",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=True,

        gender="Female",
        element="Water",
        guna="Rajas",
        caste="Brahmin",
        temperament="Gentle",
        dosha="Kapha",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="South-East",
        color="White",
        metal="Silver",
        gemstone="Diamond",
        deity="Shukracharya",
        weekday="Friday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Taurus",
            "Libra",
        ),

        exaltation_sign="Pisces",
        exaltation_degree=27.0,

        debilitation_sign="Virgo",
        debilitation_degree=27.0,

        moolatrikona_sign="Libra",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Mercury",
            "Saturn",
        ),

        enemies=(
            "Sun",
            "Moon",
        ),

        neutrals=(
            "Mars",
            "Jupiter",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Marriage",
            "Spouse",
            "Love",
            "Romance",
            "Beauty",
            "Luxury",
            "Comfort",
            "Arts",
            "Music",
            "Poetry",
            "Jewellery",
            "Vehicles",
            "Pleasure",
            "Semen",

        ),

        natural_houses=(
            7,
            12,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Kidneys",
            "Reproductive Organs",
            "Face",
            "Skin",
            "Eyes",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Kidney Disorders",
            "Diabetes",
            "Venereal Diseases",
            "Reproductive Disorders",
            "Urinary Disorders",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Artist",
            "Musician",
            "Actor",
            "Fashion Designer",
            "Jeweller",
            "Beautician",
            "Interior Designer",
            "Diplomat",
            "Hotel Industry",
            "Luxury Business",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "love",
            "beauty",
            "marriage",
            "luxury",
            "comfort",
            "art",
            "music",
            "wealth",
            "relationships",
            "pleasure",
            "refinement",
            "harmony",

        ),

    ),
        # ==========================================================
    # SATURN
    # ==========================================================

    Graha.SATURN: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Saturn",
        sanskrit_name="Shani",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=False,

        gender="Neuter",
        element="Air",
        guna="Tamas",
        caste="Shudra",
        temperament="Cruel",
        dosha="Vata",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="West",
        color="Black",
        metal="Iron",
        gemstone="Blue Sapphire",
        deity="Shani",
        weekday="Saturday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(
            "Capricorn",
            "Aquarius",
        ),

        exaltation_sign="Libra",
        exaltation_degree=20.0,

        debilitation_sign="Aries",
        debilitation_degree=20.0,

        moolatrikona_sign="Aquarius",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Mercury",
            "Venus",
        ),

        enemies=(
            "Sun",
            "Moon",
        ),

        neutrals=(
            "Mars",
            "Jupiter",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Longevity",
            "Discipline",
            "Delay",
            "Hard Work",
            "Patience",
            "Sorrow",
            "Old Age",
            "Servants",
            "Labor",
            "Justice",
            "Karma",

        ),

        natural_houses=(
            8,
            10,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Bones",
            "Teeth",
            "Knees",
            "Legs",
            "Nerves",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Arthritis",
            "Chronic Diseases",
            "Joint Disorders",
            "Paralysis",
            "Nervous Disorders",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Judge",
            "Laborer",
            "Miner",
            "Engineer",
            "Farmer",
            "Factory Worker",
            "Auditor",
            "Administrator",
            "Construction",
            "Metal Industry",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "discipline",
            "karma",
            "delay",
            "patience",
            "longevity",
            "justice",
            "hard work",
            "responsibility",
            "endurance",
            "limitations",
            "maturity",
            "perseverance",

        ),

    ),
        # ==========================================================
    # RAHU
    # ==========================================================

    Graha.RAHU: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Rahu",
        sanskrit_name="Rahu",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=False,

        gender="Neuter",
        element="Air",
        guna="Tamas",
        caste="Chandala",
        temperament="Cruel",
        dosha="Vata",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="South-West",
        color="Smoky",
        metal="Lead",
        gemstone="Hessonite",
        deity="Sarpa",
        weekday="Saturday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(),

        exaltation_sign="Taurus",
        exaltation_degree=20.0,

        debilitation_sign="Scorpio",
        debilitation_degree=20.0,

        moolatrikona_sign="",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Mercury",
            "Venus",
            "Saturn",
        ),

        enemies=(
            "Sun",
            "Moon",
            "Mars",
        ),

        neutrals=(
            "Jupiter",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Foreign Lands",
            "Foreign Travel",
            "Obsession",
            "Material Desires",
            "Politics",
            "Diplomacy",
            "Mass Influence",
            "Technology",
            "Innovation",
            "Illusion",
            "Poison",
            "Smoke",

        ),

        natural_houses=(
            11,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Feet",
            "Nervous System",
            "Skin",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Addiction",
            "Mental Disorders",
            "Poisoning",
            "Skin Diseases",
            "Phobias",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Politician",
            "Scientist",
            "Researcher",
            "Foreign Trade",
            "Pilot",
            "Intelligence",
            "Cyber Security",
            "Technology",
            "Film Industry",
            "Digital Media",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "illusion",
            "foreign",
            "technology",
            "innovation",
            "obsession",
            "ambition",
            "politics",
            "unconventional",
            "mystery",
            "desire",
            "mass influence",
            "smoke",

        ),

    ),

        # ==========================================================
    # KETU
    # ==========================================================

    Graha.KETU: PlanetFacts(

        # ------------------------------------------------------
        # Identity
        # ------------------------------------------------------

        name="Ketu",
        sanskrit_name="Ketu",

        # ------------------------------------------------------
        # Natural Nature
        # ------------------------------------------------------

        is_benefic=False,

        gender="Neuter",
        element="Fire",
        guna="Tamas",
        caste="Mleccha",
        temperament="Cruel",
        dosha="Pitta",

        # ------------------------------------------------------
        # Traditional Correspondences
        # ------------------------------------------------------

        direction="North-West",
        color="Multi-Colored",
        metal="Mixed Metals",
        gemstone="Cat's Eye",
        deity="Ganesha",
        weekday="Tuesday",

        # ------------------------------------------------------
        # Sign Ownership
        # ------------------------------------------------------

        own_signs=(),

        exaltation_sign="Scorpio",
        exaltation_degree=20.0,

        debilitation_sign="Taurus",
        debilitation_degree=20.0,

        moolatrikona_sign="",

        # ------------------------------------------------------
        # Natural Friendships
        # ------------------------------------------------------

        friends=(
            "Mars",
            "Jupiter",
        ),

        enemies=(
            "Sun",
            "Moon",
        ),

        neutrals=(
            "Mercury",
            "Venus",
            "Saturn",
        ),

        # ------------------------------------------------------
        # Natural Significations (Karakatwas)
        # ------------------------------------------------------

        karakatwas=(

            "Liberation",
            "Spirituality",
            "Detachment",
            "Renunciation",
            "Mysticism",
            "Occult",
            "Intuition",
            "Past Life Karma",
            "Enlightenment",
            "Asceticism",
            "Sudden Separation",

        ),

        natural_houses=(
            12,
        ),

        # ------------------------------------------------------
        # Body Parts
        # ------------------------------------------------------

        body_parts=(

            "Spine",
            "Nervous System",

        ),

        # ------------------------------------------------------
        # Diseases
        # ------------------------------------------------------

        diseases=(

            "Unknown Diseases",
            "Autoimmune Disorders",
            "Accidents",
            "Psychological Disorders",

        ),

        # ------------------------------------------------------
        # Professional Significations
        # ------------------------------------------------------

        professions=(

            "Spiritual Teacher",
            "Researcher",
            "Monk",
            "Astrologer",
            "Mystic",
            "Occult Practitioner",
            "Surgeon",
            "Investigator",

        ),

        # ------------------------------------------------------
        # Keywords
        # ------------------------------------------------------

        keywords=(

            "moksha",
            "detachment",
            "spirituality",
            "intuition",
            "renunciation",
            "occult",
            "liberation",
            "past karma",
            "enlightenment",
            "mysticism",
            "isolation",

        ),

    ),
}

def get_planet(name: Graha) -> PlanetFacts:
    return PLANETS[name]


def all_planets():
    return PLANETS.values()


__all__ = [
    "PLANETS",
    "get_planet",
    "all_planets",
]