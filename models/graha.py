"""
models/graha.py

Definitions for the Navagraha used throughout the Kundali Engine.

Python Version:
    3.9+
"""

from __future__ import annotations

from enum import Enum


class Graha(Enum):
    """Enumeration of the nine Vedic Grahas."""

    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"

    @property
    def display_name(self) -> str:
        """Human-readable name."""
        return self.value

    def __str__(self) -> str:
        return self.value
