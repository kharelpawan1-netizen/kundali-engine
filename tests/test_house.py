from models.house import House

house = House(number=1, longitude=348.32, sign="Pisces", sign_number=12)

house.add_planet("Sun")
house.add_planet("Jupiter")

print(house)
print("Planets:", house.planets)
print("Lord:", house.lord)
print("Strength:", house.strength)
