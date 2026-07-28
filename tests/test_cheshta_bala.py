"""
Tests for Cheshta Bala.
"""

from astronomy.cheshta_bala import (
    DIRECT_BALA,
    RETROGRADE_BALA,
    STATIONARY_BALA,
    cheshta_bala,
    cheshta_state,
)
from models.cheshta import CheshtaState


def test_direct_state():
    assert (
        cheshta_state(
            longitude_speed=1.25,
            retrograde=False,
        )
        is CheshtaState.DIRECT
    )


def test_retrograde_state():
    assert (
        cheshta_state(
            longitude_speed=-0.75,
            retrograde=True,
        )
        is CheshtaState.RETROGRADE
    )


def test_stationary_state():
    assert (
        cheshta_state(
            longitude_speed=0.0,
            retrograde=False,
        )
        is CheshtaState.STATIONARY
    )


def test_direct_bala():
    assert (
        cheshta_bala(
            longitude_speed=1.0,
            retrograde=False,
        )
        == DIRECT_BALA
    )


def test_retrograde_bala():
    assert (
        cheshta_bala(
            longitude_speed=-1.0,
            retrograde=True,
        )
        == RETROGRADE_BALA
    )


def test_stationary_bala():
    assert (
        cheshta_bala(
            longitude_speed=0.0,
            retrograde=False,
        )
        == STATIONARY_BALA
    )
