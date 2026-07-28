from datetime import datetime

from astronomy.ascendant import calculate_ascendant
from astronomy.julian import datetime_to_julian
from astronomy.swiss import (
    Ayanamsha,
    set_ayanamsha,
    set_ephemeris_path,
)
from models.location import Location

set_ephemeris_path(r"D:\kundali\ephe")
set_ayanamsha(Ayanamsha.LAHIRI)

location = Location(
    name="Kathmandu",
    latitude=27.7172,
    longitude=85.3240,
    timezone="Asia/Kathmandu",
)

jd = datetime_to_julian(datetime(2000, 1, 1, 12, 0, 0))

lagna = calculate_ascendant(
    jd,
    location,
)

print("=" * 60)
print("ASCENDANT")
print("=" * 60)
print(lagna)
print("=" * 60)
