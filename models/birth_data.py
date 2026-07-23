"""
models/birth_data.py

Birth data model for the Kundali Engine.

Stores all information required to calculate
a horoscope.

Version:
    2.0.0

Compatible with Python 3.9
"""

from dataclasses import dataclass
from datetime import datetime

from models.location import Location


@dataclass
class BirthData:
    """
    Complete birth information.

    Attributes
    ----------
    name : str
        Native's name.

    birth_datetime : datetime
        Local birth date and time.

    location : Location
        Birth location.

    notes : str
        Optional notes.
    """

    name: str

    birth_datetime: datetime

    location: Location

    notes: str = ""

    @property
    def year(self) -> int:
        return self.birth_datetime.year

    @property
    def month(self) -> int:
        return self.birth_datetime.month

    @property
    def day(self) -> int:
        return self.birth_datetime.day

    @property
    def hour(self) -> int:
        return self.birth_datetime.hour

    @property
    def minute(self) -> int:
        return self.birth_datetime.minute

    @property
    def second(self) -> int:
        return self.birth_datetime.second

    @property
    def decimal_hour(self) -> float:
        """
        Returns time in decimal hours.

        Example:
        10:30:00 -> 10.5
        """

        return (
            self.hour +
            self.minute / 60.0 +
            self.second / 3600.0
        )

    def __str__(self):
        return (
            f"{self.name} "
            f"({self.birth_datetime})"
        )