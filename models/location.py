"""
models/location.py

Location model for the Kundali Engine.

Stores the geographical information required for
astronomical calculations.

Version:
    2.0.0

Compatible with Python 3.9
"""

from dataclasses import dataclass


@dataclass
class Location:
    """
    Geographic location.

    Attributes
    ----------
    name : str
        Display name of the location.

    latitude : float
        Latitude in decimal degrees.
        North is positive.

    longitude : float
        Longitude in decimal degrees.
        East is positive.

    timezone : str
        IANA timezone name.
        Example:
            Asia/Kathmandu

    elevation : float
        Elevation above sea level in meters.

    country : str
        Country name.

    city : str
        City name.
    """

    name: str

    latitude: float

    longitude: float

    timezone: str

    elevation: float = 0.0

    country: str = ""

    city: str = ""

    @property
    def coordinates(self):
        """
        Returns latitude and longitude.

        Returns
        -------
        tuple
            (latitude, longitude)
        """

        return (self.latitude, self.longitude)

    def __str__(self):
        """
        Human-readable representation.
        """

        return self.name
