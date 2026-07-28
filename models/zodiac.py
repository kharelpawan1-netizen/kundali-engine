"""
models/zodiac.py

Zodiac sign enumeration.

Python Version:
    3.9+

Author:
    Kundali Engine

License:
    MIT
"""

from enum import Enum

from models.element import Element


class ZodiacSign(Enum):
    """
    Twelve zodiac signs.
    """

    ARIES = ("Aries", 1, Element.FIRE)
    TAURUS = ("Taurus", 2, Element.EARTH)
    GEMINI = ("Gemini", 3, Element.AIR)
    CANCER = ("Cancer", 4, Element.WATER)
    LEO = ("Leo", 5, Element.FIRE)
    VIRGO = ("Virgo", 6, Element.EARTH)
    LIBRA = ("Libra", 7, Element.AIR)
    SCORPIO = ("Scorpio", 8, Element.WATER)
    SAGITTARIUS = ("Sagittarius", 9, Element.FIRE)
    CAPRICORN = ("Capricorn", 10, Element.EARTH)
    AQUARIUS = ("Aquarius", 11, Element.AIR)
    PISCES = ("Pisces", 12, Element.WATER)

    def __init__(
        self,
        display_name: str,
        number: int,
        element: Element,
    ):
        self.display_name = display_name
        self.number = number
        self.element = element

    def __str__(self) -> str:
        return self.display_name


def sign_from_number(number: int) -> ZodiacSign:
    """
    Return a ZodiacSign from its numerical value (1-12).

    Parameters
    ----------
    number
        Zodiac sign number.

    Returns
    -------
    ZodiacSign
    """

    for sign in ZodiacSign:
        if sign.number == number:
            return sign

    raise ValueError(f"Invalid zodiac sign number: {number}")
