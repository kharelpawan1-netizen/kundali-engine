"""
astronomy/nakshatra.py

Mathematical Nakshatra calculations.

Compatible with Python 3.9
"""

NAKSHATRAS = [

    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),

    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshtha", "Mercury"),

    ("Mula", "Ketu"),
    ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury")
]


NAKSHATRA_SIZE = 13.333333333333334


def get_nakshatra(longitude):
    """
    Returns

    (name, pada, lord)
    """

    longitude %= 360.0

    index = int(longitude / NAKSHATRA_SIZE)

    name, lord = NAKSHATRAS[index]

    inside = longitude % NAKSHATRA_SIZE

    pada = int(inside / (NAKSHATRA_SIZE / 4)) + 1

    return (
        name,
        pada,
        lord
    )