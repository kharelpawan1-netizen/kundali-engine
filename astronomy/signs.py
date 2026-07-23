"""
Zodiac sign utilities.
"""

SIGNS = [
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


def get_sign(longitude):
    """
    Return sign name and degree within sign.

    Parameters
    ----------
    longitude : float

    Returns
    -------
    tuple
        (sign_name, sign_number, degree)
    """

    longitude = longitude % 360.0

    sign_number = int(longitude // 30)

    sign_degree = longitude % 30

    return (SIGNS[sign_number], sign_number + 1, sign_degree)
