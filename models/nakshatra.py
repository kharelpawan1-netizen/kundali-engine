"""
models/nakshatra.py

Immutable Nakshatra information.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NakshatraInfo:
    """
    Immutable information describing a Nakshatra position.
    """

    number: int

    name: str

    lord: str

    pada: int

    degree: float

    start_degree: float

    end_degree: float
