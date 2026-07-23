"""
models/location.py

Location model.
Compatible with Python 3.9
"""

from dataclasses import dataclass


@dataclass
class Location:
    """
    Geographic location.
    """

    latitude: float
    longitude: float

    elevation: float = 0.0

    timezone: str = "UTC"

    country: str = ""

    city: str = ""