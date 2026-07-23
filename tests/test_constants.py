"""
tests/test_constants.py

Tests for astronomy.constants
"""

from astronomy.constants import (
    DEGREES_PER_SIGN,
    NAKSHATRA_SIZE,
    PADA_SIZE,
    PLANETS,
    ZODIAC_SIGNS,
)


def main():
    print("Zodiac Signs:", ZODIAC_SIGNS)

    print("Degrees Per Sign:", DEGREES_PER_SIGN)

    print("Nakshatra Size:", NAKSHATRA_SIZE)

    print("Pada Size:", PADA_SIZE)

    print("Planets:")

    for name in PLANETS:
        print("-", name)


if __name__ == "__main__":
    main()
