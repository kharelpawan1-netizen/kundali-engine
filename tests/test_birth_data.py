from datetime import datetime

from models.birth_data import BirthData
from models.location import Location

location = Location(
    name="Kathmandu, Nepal",
    latitude=27.7172,
    longitude=85.3240,
    timezone="Asia/Kathmandu",
)

birth = BirthData(
    name="Test User", birth_datetime=datetime(2000, 1, 1, 12, 30, 0), location=location
)

print(birth)

print("Year :", birth.year)
print("Month:", birth.month)
print("Day  :", birth.day)

print("Hour :", birth.hour)
print("Min  :", birth.minute)

print("Decimal Hour:", birth.decimal_hour)
