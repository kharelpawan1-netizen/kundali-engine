"""
models/ascendant.py

Ascendant (Lagna) model.

Version:
    1.1.0
"""

from __future__ import annotations

from dataclasses import dataclass

from models.nakshatra import NakshatraInfo
from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class Ascendant:
    """
    Immutable representation of the Ascendant (Lagna).

    Attributes
    ----------
    longitude
        Sidereal longitude (0°–360°).

    sign
        Zodiac sign containing the Ascendant.

    degree_in_sign
        Degrees traversed within the sign (0°–30°).

    nakshatra
        Nakshatra occupied by the Ascendant.

    pada
        Pada (1–4) occupied by the Ascendant.
    """

    longitude: float

    sign: ZodiacSign

    degree_in_sign: float

    nakshatra: NakshatraInfo

    pada: int
