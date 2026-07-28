"""
Tests for Ascendant calculations.
"""

from astronomy.ascendant import calculate_ascendant
from models.ascendant import Ascendant
from models.location import Location


def test_calculate_ascendant():
    """
    Verify that the Ascendant engine returns a valid
    Ascendant object with internally consistent values.
    """

    location = Location(
        name="Kathmandu",
        latitude=27.7172,
        longitude=85.3240,
        timezone="Asia/Kathmandu",
        elevation=1400.0,
    )

    result = calculate_ascendant(
        2451545.0,
        location,
    )

    assert isinstance(result, Ascendant)

    assert 0.0 <= result.longitude < 360.0
    assert 0.0 <= result.degree_in_sign < 30.0

    assert result.sign is not None
    assert result.nakshatra is not None
    assert 1 <= result.pada <= 4

    # Verify consistency between longitude and sign.
    assert result.sign.number == int(result.longitude // 30) + 1
