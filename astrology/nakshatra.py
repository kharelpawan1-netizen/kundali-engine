"""
astrology/nakshatra.py

Vedic astrology information for all 27 Nakshatras.

This module contains interpretation data only.
No mathematical calculations are performed here.
Compatible with Python 3.9
"""

from dataclasses import dataclass


@dataclass
class NakshatraInfo:
    """
    Information about a Nakshatra.
    """

    name: str
    lord: str
    deity: str
    symbol: str
    gana: str
    yoni: str
    element: str
    motivation: str
    nature: str


NAKSHATRAS = {

    "Ashwini": NakshatraInfo(
        name="Ashwini",
        lord="Ketu",
        deity="Ashwini Kumaras",
        symbol="Horse Head",
        gana="Deva",
        yoni="Horse",
        element="Earth",
        motivation="Dharma",
        nature="Swift"
    ),

    "Bharani": NakshatraInfo(
        name="Bharani",
        lord="Venus",
        deity="Yama",
        symbol="Yoni",
        gana="Manushya",
        yoni="Elephant",
        element="Earth",
        motivation="Artha",
        nature="Fierce"
    ),

    "Krittika": NakshatraInfo(
        name="Krittika",
        lord="Sun",
        deity="Agni",
        symbol="Knife",
        gana="Rakshasa",
        yoni="Sheep",
        element="Fire",
        motivation="Kama",
        nature="Sharp"
    ),

    "Rohini": NakshatraInfo(
        name="Rohini",
        lord="Moon",
        deity="Brahma",
        symbol="Chariot",
        gana="Manushya",
        yoni="Serpent",
        element="Earth",
        motivation="Moksha",
        nature="Fixed"
    ),

    "Mrigashira": NakshatraInfo(
        name="Mrigashira",
        lord="Mars",
        deity="Soma",
        symbol="Deer's Head",
        gana="Deva",
        yoni="Serpent",
        element="Earth",
        motivation="Moksha",
        nature="Soft"
    ),

    "Ardra": NakshatraInfo(
        name="Ardra",
        lord="Rahu",
        deity="Rudra",
        symbol="Teardrop",
        gana="Manushya",
        yoni="Dog",
        element="Water",
        motivation="Kama",
        nature="Sharp"
    ),

    "Punarvasu": NakshatraInfo(
        name="Punarvasu",
        lord="Jupiter",
        deity="Aditi",
        symbol="Quiver of Arrows",
        gana="Deva",
        yoni="Cat",
        element="Water",
        motivation="Artha",
        nature="Movable"
    ),

    "Pushya": NakshatraInfo(
        name="Pushya",
        lord="Saturn",
        deity="Brihaspati",
        symbol="Cow's Udder",
        gana="Deva",
        yoni="Goat",
        element="Water",
        motivation="Dharma",
        nature="Light"
    ),

    "Ashlesha": NakshatraInfo(
        name="Ashlesha",
        lord="Mercury",
        deity="Nagas",
        symbol="Coiled Serpent",
        gana="Rakshasa",
        yoni="Cat",
        element="Water",
        motivation="Dharma",
        nature="Sharp"
    ),

    # ------------------------------------------------------------------
    # TODO:
    # Continue the remaining 18 Nakshatras
    # (Magha → Revati)
    # We'll complete them in the next phase.
    # ------------------------------------------------------------------

}


def get_info(name):
    """
    Returns NakshatraInfo object.

    Example
    -------
    >>> get_info("Ashwini")
    """

    return NAKSHATRAS.get(name)