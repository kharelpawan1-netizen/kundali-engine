import swisseph as swe

print("Swiss Ephemeris version:")
print(swe.version)

jd = swe.julday(2000, 1, 1, 12.0)

print("Julian Day:", jd)

planet = swe.calc_ut(jd, swe.SUN)

print("Sun:")
print(planet)