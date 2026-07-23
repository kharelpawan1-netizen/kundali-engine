"""
models/birth_data.py

Birth data model.
Compatible with Python 3.9
"""

from dataclasses import dataclass
from datetime import datetime

from models.location import Location


@dataclass
class BirthData:
    """
    Complete birth information.
    """

    name: str

    birth_datetime: datetime

    location: Location

    notes: str = ""