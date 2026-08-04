"""
Tests for house and Bhava calculations.
"""

from datetime import datetime

from astronomy.houses import (
    bhava_cusps,
    cusp_houses,
    house_from_longitude,
    normalize_longitude,
    whole_sign_houses,
)
from astronomy.julian import datetime_to_julian
from astronomy.swiss import (
    Ayanamsha,
    set_ayanamsha,
    set_ephemeris_path,
)
from models.house import House
from models.zodiac import ZodiacSign

set_ephemeris_path(r"D:\kundali\ephe")
set_ayanamsha(Ayanamsha.LAHIRI)


def test_normalize_longitude():
    """Longitude should wrap into [0, 360)."""

    assert normalize_longitude(0.0) == 0.0
    assert normalize_longitude(360.0) == 0.0
    assert normalize_longitude(361.0) == 1.0
    assert normalize_longitude(-1.0) == 359.0


def test_whole_sign_house_count():
    """Whole Sign system must produce twelve houses."""

    houses = whole_sign_houses(0.0)

    assert len(houses) == 12
    assert set(houses) == set(range(1, 13))


def test_whole_sign_aries_ascendant():
    """Aries Ascendant should produce Aries as first house."""

    houses = whole_sign_houses(10.0)

    assert houses[1].sign == ZodiacSign.ARIES.display_name
    assert houses[1].sign_number == ZodiacSign.ARIES.number
    assert houses[2].sign == ZodiacSign.TAURUS.display_name
    assert houses[12].sign == ZodiacSign.PISCES.display_name

def test_whole_sign_cancer_ascendant():
    """Cancer Ascendant should produce Cancer as first house."""

    houses = whole_sign_houses(100.0)

    assert houses[1].sign == ZodiacSign.CANCER.display_name
    assert houses[4].sign == ZodiacSign.LIBRA.display_name
    assert houses[7].sign == ZodiacSign.CAPRICORN.display_name
    assert houses[10].sign == ZodiacSign.ARIES.display_name


def test_whole_sign_wraparound():
    """Whole Sign houses should wrap after Pisces."""

    houses = whole_sign_houses(350.0)

    assert houses[1].sign == ZodiacSign.PISCES.display_name
    assert houses[2].sign == ZodiacSign.ARIES.display_name
    assert houses[3].sign == ZodiacSign.TAURUS.display_name
    assert houses[12].sign == ZodiacSign.AQUARIUS.display_name


def test_whole_sign_house_longitudes():
    """Whole Sign house beginnings should occur at sign boundaries."""

    houses = whole_sign_houses(10.0)

    assert houses[1].longitude == 0.0
    assert houses[2].longitude == 30.0
    assert houses[12].longitude == 330.0


def test_house_objects():
    """Whole Sign houses should contain House objects."""

    houses = whole_sign_houses(10.0)

    for house in houses.values():
        assert isinstance(house, House)


def test_bhava_cusps_return_twelve():
    """Swiss Ephemeris should return twelve normalized cusps."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    cusps, ascendant = bhava_cusps(
        jd,
        27.7172,
        85.3240,
    )

    assert len(cusps) == 12
    assert 0.0 <= ascendant < 360.0

    for cusp in cusps:
        assert 0.0 <= cusp < 360.0


def test_cusp_houses_return_twelve():
    """Cusp-based house construction should return twelve houses."""

    jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

    houses = cusp_houses(
        jd,
        27.7172,
        85.3240,
    )

    assert len(houses) == 12
    assert set(houses) == set(range(1, 13))

    for number, house in houses.items():
        assert number == house.number
        assert 0.0 <= house.longitude < 360.0


def test_house_from_longitude_whole_sign():
    """Planetary longitude should map correctly in Whole Sign houses."""

    houses = whole_sign_houses(10.0)

    assert house_from_longitude(10.0, houses) == 1
    assert house_from_longitude(29.999, houses) == 1
    assert house_from_longitude(30.0, houses) == 2
    assert house_from_longitude(359.999, houses) == 12


def test_house_from_longitude_wraparound():
    """House lookup must handle the 360° boundary."""

    houses = {
        1: House(1, 350.0, "Pisces", 12),
        2: House(2, 20.0, "Aries", 1),
        3: House(3, 50.0, "Taurus", 2),
        4: House(4, 80.0, "Gemini", 3),
        5: House(5, 110.0, "Cancer", 4),
        6: House(6, 140.0, "Leo", 5),
        7: House(7, 170.0, "Virgo", 6),
        8: House(8, 200.0, "Libra", 7),
        9: House(9, 230.0, "Scorpio", 8),
        10: House(10, 260.0, "Sagittarius", 9),
        11: House(11, 290.0, "Capricorn", 10),
        12: House(12, 320.0, "Aquarius", 11),
    }

    assert house_from_longitude(359.999, houses) == 1
    assert house_from_longitude(0.0, houses) == 1
    assert house_from_longitude(19.999, houses) == 1
    assert house_from_longitude(20.0, houses) == 2
