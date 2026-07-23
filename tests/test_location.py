from models.location import Location

location = Location(
    name="Kathmandu, Nepal",
    latitude=27.7172,
    longitude=85.3240,
    timezone="Asia/Kathmandu",
    elevation=1400,
    country="Nepal",
    city="Kathmandu",
)

print(location)
print(location.coordinates)
