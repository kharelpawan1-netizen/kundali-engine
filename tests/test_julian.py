"""
tests/test_julian.py
"""

from datetime import datetime

from astronomy.julian import datetime_to_julian, julian_to_datetime

dt = datetime(2000, 1, 1, 12, 0, 0)

jd = datetime_to_julian(dt)

print("Original datetime:")
print(dt)

print()

print("Julian Day:")
print(jd)

print()

print("Converted back:")
print(julian_to_datetime(jd))
