"""
Cheshta Bala.

Motion strength according to BPHS.

Python Version:
    3.9+

Author:
    Kundali Engine
"""

from __future__ import annotations

from models.cheshta import CheshtaState

RETROGRADE_BALA = 60.0

DIRECT_BALA = 30.0

STATIONARY_BALA = 15.0


def cheshta_state(
    longitude_speed: float,
    retrograde: bool,
) -> CheshtaState:
    """
    Determine planetary motion state.
    """

    if abs(longitude_speed) < 0.01:
        return CheshtaState.STATIONARY

    if retrograde:
        return CheshtaState.RETROGRADE

    return CheshtaState.DIRECT


def cheshta_bala(
    longitude_speed: float,
    retrograde: bool,
) -> float:
    """
    Return simplified BPHS Cheshta Bala.
    """

    state = cheshta_state(
        longitude_speed,
        retrograde,
    )

    if state is CheshtaState.RETROGRADE:
        return RETROGRADE_BALA

    if state is CheshtaState.STATIONARY:
        return STATIONARY_BALA

    return DIRECT_BALA


__all__ = [
    "RETROGRADE_BALA",
    "DIRECT_BALA",
    "STATIONARY_BALA",
    "cheshta_state",
    "cheshta_bala",
]
