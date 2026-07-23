from models.chart import BirthChart
from models.house import House
from models.planet import Planet

chart = BirthChart()

chart.add_planet(
    Planet(name="Sun", longitude=256.2, latitude=0, distance=1, speed=0.98)
)

chart.add_house(House(number=1, longitude=348.3, sign="Pisces", sign_number=12))

print(chart)

print(chart.get_planet("Sun"))

print(chart.get_house(1))
