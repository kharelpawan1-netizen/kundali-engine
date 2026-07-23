"""
models/planet.py

Planet model for the Kundali Engine.

Stores all computed astronomical and astrological
information for a single planet.

Version:
    2.0.0

Compatible with Python 3.9
"""

from dataclasses import dataclass


@dataclass
class Planet:
    """
    Planet information.
    """

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------

    name: str

    # ---------------------------------------------------------
    # Astronomical Values
    # ---------------------------------------------------------

    longitude: float

    latitude: float

    distance: float

    speed: float

    retrograde: bool = False

    # ---------------------------------------------------------
    # Zodiac
    # ---------------------------------------------------------

    sign: str = ""

    sign_number: int = 0

    sign_degree: float = 0.0

    # ---------------------------------------------------------
    # House
    # ---------------------------------------------------------

    house: int = 0

    # ---------------------------------------------------------
    # Nakshatra
    # ---------------------------------------------------------

    nakshatra: str = ""

    pada: int = 0

    nakshatra_lord: str = ""

    # ---------------------------------------------------------
    # Future Modules
    # ---------------------------------------------------------

    dignity: str = ""

    combustion: bool = False

    exalted: bool = False

    debilitated: bool = False

    own_sign: bool = False

    moolatrikona: bool = False

    # ---------------------------------------------------------

    @property
    def degree(self):
        """
        Alias for sign degree.
        """

        return self.sign_degree

    @property
    def absolute_degree(self):
        """
        0°–360° longitude.
        """

        return self.longitude

    def __str__(self):
        """
        Human-readable string.
        """

        return (
            f"{self.name}: "
            f"{self.sign} "
            f"{self.sign_degree:.2f}°"
        )