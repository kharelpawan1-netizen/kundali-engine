"""
tests/test_constants.py
"""

from astronomy.constants import *

print("Zodiac Signs:", ZODIAC_SIGNS)

print("Degrees Per Sign:", DEGREES_PER_SIGN)

print("Nakshatra Size:", NAKSHATRA_SIZE)

print("Pada Size:", PADA_SIZE)

print("Planets:")

for name in PLANETS:
    print("-", name)