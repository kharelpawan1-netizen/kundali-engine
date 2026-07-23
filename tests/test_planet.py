from models.planet import Planet

planet = Planet(
    name="Sun",
    longitude=256.27,
    latitude=0.0,
    distance=1.0,
    speed=0.98,
    retrograde=False,
    sign="Sagittarius",
    sign_number=9,
    sign_degree=16.27,
    house=10,
    nakshatra="Purva Ashadha",
    pada=1,
    nakshatra_lord="Venus",
)

print(planet)

print("Longitude :", planet.absolute_degree)
print("Degree    :", planet.degree)
print("House     :", planet.house)
print("Retrograde:", planet.retrograde)
