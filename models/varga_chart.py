"""
Unified Varga chart container.

Python Version:
    3.9+
"""

from __future__ import annotations

from dataclasses import dataclass

from models.akshavedamsa_position import AkshavedamsaPosition
from models.bhamsa_position import BhamsaPosition
from models.chaturvimshamsa_position import ChaturvimshamsaPosition
from models.dasamsa_position import DasamsaPosition
from models.dvadasamsa_position import DvadasamsaPosition
from models.hora_position import HoraPosition
from models.khavedamsa_position import KhavedamsaPosition
from models.navamsa_position import NavamsaPosition
from models.saptamsa_position import SaptamsaPosition
from models.shastiamsa_position import ShastiamsaPosition
from models.shodasamsa_position import ShodasamsaPosition
from models.trimshamsa_position import TrimshamsaPosition
from models.varga_position import VargaPosition
from models.vimsamsa_position import VimsamsaPosition


@dataclass(frozen=True)
class VargaChart:
    """
    All BPHS Vargas for one planet.
    """

    hora: HoraPosition
    drekkana: VargaPosition
    saptamsa: SaptamsaPosition
    navamsa: NavamsaPosition
    dasamsa: DasamsaPosition
    dvadasamsa: DvadasamsaPosition
    shodasamsa: ShodasamsaPosition
    vimsamsa: VimsamsaPosition
    siddhamsa: ChaturvimshamsaPosition
    bhamsa: BhamsaPosition
    trimshamsa: TrimshamsaPosition
    khavedamsa: KhavedamsaPosition
    akshavedamsa: AkshavedamsaPosition
    shastiamsa: ShastiamsaPosition
