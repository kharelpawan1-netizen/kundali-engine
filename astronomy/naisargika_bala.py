"""
Naisargika Bala.

Natural planetary strength according to BPHS.
"""

from __future__ import annotations

from models.graha import Graha

NAISARGIKA_BALA = {
    Graha.SUN: 60.0,
    Graha.MOON: 51.43,
    Graha.VENUS: 42.86,
    Graha.JUPITER: 34.29,
    Graha.MERCURY: 25.71,
    Graha.MARS: 17.14,
    Graha.SATURN: 8.57,
}


def naisargika_bala(
    graha: Graha,
) -> float:
    """
    Return the BPHS natural strength of a planet.
    """

    return NAISARGIKA_BALA[graha]


__all__ = [
    "NAISARGIKA_BALA",
    "naisargika_bala",
]
