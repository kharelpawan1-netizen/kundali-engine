"""
models/sign.py

Definitions for the twelve Rashis (zodiac signs) used
throughout the Kundali Engine.

Python Version:
    3.9+
"""

from __future__ import annotations

from enum import Enum


class Sign(Enum):
    """Enumeration of the twelve Vedic Rashis."""

    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"

    @property
    def display_name(self) -> str:
        """Human-readable name."""
        return self.value

    def __str__(self) -> str:
        return self.value