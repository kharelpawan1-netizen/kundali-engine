"""
Chaturthamsa (D4) calculation.

According to Brihat Parashara Hora Shastra (BPHS Chapter 6).

Each sign is divided into four equal parts of 7°30' (7.5°).
The rulers / signs of the 4 parts are:
1st part (0° - 7.5°): The sign itself (1st from sign)
2nd part (7.5° - 15°): 4th sign from the sign
3rd part (15° - 22.5°): 7th sign from the sign
4th part (22.5° - 30°): 10th sign from the sign

Python Version:
    3.9+
"""

from __future__ import annotations

from models.chaturthamsa_position import ChaturthamsaPosition
from models.zodiac import sign_from_number

DIVISION_SIZE = 7.5


def chaturthamsa(
    longitude: float,
) -> ChaturthamsaPosition:
    """
    Compute Chaturthamsa (D4).

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    ChaturthamsaPosition
    """

    longitude %= 360.0

    sign_number = int(longitude // 30.0) + 1

    degree = longitude % 30.0

    division = int(degree // DIVISION_SIZE) + 1

    if division > 4:
        division = 4

    # The 4 divisions start from 1st, 4th, 7th, and 10th from the sign
    target = ((sign_number + (division - 1) * 3 - 1) % 12) + 1

    return ChaturthamsaPosition(
        sign=sign_from_number(target),
        division=division,
    )


__all__ = [
    "chaturthamsa",
]
