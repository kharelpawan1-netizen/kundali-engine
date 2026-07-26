"""
models/sign_info.py

Immutable SignInfo dataclass.

Python Version:
    3.9+

Author:
    Kundali Engine

License:
    MIT
"""

from dataclasses import dataclass

from models.element import Element
from models.zodiac import ZodiacSign


@dataclass(frozen=True)
class SignInfo:
    """
    Zodiac sign information.
    """

    number: int

    sign: ZodiacSign

    degree: float

    start_degree: float

    end_degree: float

    element: Element
