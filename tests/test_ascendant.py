"""
Tests for Ascendant calculations.
"""

import pytest

from astronomy.ascendant import calculate_ascendant
from models.location import Location


def test_calculate_ascendant_placeholder():
    """
    Placeholder test until the Ascendant engine
    is fully implemented.
    """

    location = Location(
        name="Kathmandu",
        latitude=27.7172,
        longitude=85.3240,
        timezone="Asia/Kathmandu",
        elevation=1400.0,
    )

    with pytest.raises(NotImplementedError):
        calculate_ascendant(
            2451545.0,
            location,
        )
