"""
Unified BPHS Varga engine.

Python Version:
    3.9+
"""

from __future__ import annotations

from astronomy.akshavedamsa import akshavedamsa
from astronomy.bhamsa import bhamsa
from astronomy.chaturvimshamsa import chaturvimshamsa
from astronomy.dasamsa import dasamsa
from astronomy.drekkana import drekkana
from astronomy.dvadasamsa import dvadasamsa
from astronomy.hora import hora
from astronomy.khavedamsa import khavedamsa
from astronomy.navamsa import navamsa
from astronomy.saptamsa import saptamsa
from astronomy.shastiamsa import shastiamsa
from astronomy.shodasamsa import shodasamsa
from astronomy.trimshamsa import trimshamsa
from astronomy.vimsamsa import vimsamsa
from models.varga_chart import VargaChart


def build_varga_chart(
    longitude: float,
) -> VargaChart:
    """
    Compute every BPHS divisional chart for one longitude.

    Parameters
    ----------
    longitude
        Sidereal longitude.

    Returns
    -------
    VargaChart
    """

    # Normalize to 0° <= longitude < 360°
    longitude = longitude % 360.0

    return VargaChart(
        hora=hora(longitude),
        drekkana=drekkana(longitude),
        saptamsa=saptamsa(longitude),
        navamsa=navamsa(longitude),
        dasamsa=dasamsa(longitude),
        dvadasamsa=dvadasamsa(longitude),
        shodasamsa=shodasamsa(longitude),
        vimsamsa=vimsamsa(longitude),
        siddhamsa=chaturvimshamsa(longitude),
        bhamsa=bhamsa(longitude),
        trimshamsa=trimshamsa(longitude),
        khavedamsa=khavedamsa(longitude),
        akshavedamsa=akshavedamsa(longitude),
        shastiamsa=shastiamsa(longitude),
    )
