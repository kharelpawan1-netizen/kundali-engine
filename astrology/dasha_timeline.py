"""
astrology/dasha_timeline.py

Vimshottari Dasha timeline integration engine.

This module provides a single authoritative interface for traversing
the complete Vimshottari Dasha hierarchy:

    Mahadasha
        ↓
    Antardasha
        ↓
    Pratyantardasha
        ↓
    Sookshma Dasha
        ↓
    Prana Dasha
        ↓
    Deha Dasha

The lower-level calculations remain delegated to their respective
modules:

    astrology.dasha
    astrology.pratyantardasha
    astrology.sookshmadasha
    astrology.pranadasha
    astrology.dehadasha

This module does not duplicate the mathematical calculations of those
engines. Its purpose is to assemble them into a coherent timeline and
provide a single current-Dasha resolver.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from astrology.dasha import (
    Antardasha,
    Mahadasha,
    current_antardasha,
    current_mahadasha,
    generate_antardashas,
    generate_mahadashas,
)

from astrology.pratyantardasha import (
    Pratyantardasha,
    current_pratyantardasha,
    generate_pratyantardashas,
)

from astrology.sookshmadasha import (
    SookshmaDasha,
    current_sookshmadasha,
    generate_sookshmadashas,
)

from astrology.pranadasha import (
    PranaDasha,
    current_pranadasha,
    generate_pranadashas,
)

from astrology.dehadasha import (
    DehaDasha,
    current_dehadasha,
    generate_dehadashas,
)


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class DashaChain:
    """
    Complete active Vimshottari Dasha hierarchy.

    The chain represents one exact point in time:

        Mahadasha
            ↓
        Antardasha
            ↓
        Pratyantardasha
            ↓
        Sookshma Dasha
            ↓
        Prana Dasha
            ↓
        Deha Dasha
    """

    mahadasha: Mahadasha
    antardasha: Antardasha
    pratyantardasha: Pratyantardasha
    sookshma: SookshmaDasha
    prana: PranaDasha
    deha: DehaDasha

    @property
    def mahadasha_lord(self) -> str:
        """Return the active Mahadasha lord."""
        return self.mahadasha.planet

    @property
    def antardasha_lord(self) -> str:
        """Return the active Antardasha lord."""
        return self.antardasha.antardasha_lord

    @property
    def pratyantardasha_lord(self) -> str:
        """Return the active Pratyantardasha lord."""
        return self.pratyantardasha.pratyantardasha_lord

    @property
    def sookshma_lord(self) -> str:
        """Return the active Sookshma Dasha lord."""
        return self.sookshma.sookshma_lord

    @property
    def prana_lord(self) -> str:
        """Return the active Prana Dasha lord."""
        return self.prana.prana_lord

    @property
    def deha_lord(self) -> str:
        """Return the active Deha Dasha lord."""
        return self.deha.deha_lord

    @property
    def lords(self) -> tuple:
        """
        Return all active Dasha lords in hierarchical order.
        """
        return (
            self.mahadasha_lord,
            self.antardasha_lord,
            self.pratyantardasha_lord,
            self.sookshma_lord,
            self.prana_lord,
            self.deha_lord,
        )

    @property
    def start(self) -> datetime:
        """
        Return the start of the current Deha Dasha.

        This represents the most specific active period.
        """
        return self.deha.start

    @property
    def end(self) -> datetime:
        """
        Return the end of the current Deha Dasha.

        This represents the most specific active period.
        """
        return self.deha.end

    def contains(self, moment: datetime) -> bool:
        """
        Return True when the supplied moment falls inside
        the complete active Deha interval.
        """
        return self.deha.contains(moment)


# ============================================================
# Validation
# ============================================================

def _validate_birth_datetime(
    birth_datetime: datetime,
) -> None:
    """Validate the birth datetime."""
    if not isinstance(birth_datetime, datetime):
        raise TypeError(
            "birth_datetime must be a datetime."
        )


def _validate_moment(
    moment: datetime,
) -> None:
    """Validate an evaluation datetime."""
    if not isinstance(moment, datetime):
        raise TypeError(
            "moment must be a datetime."
        )


def _validate_chain(
    chain: DashaChain,
) -> None:
    """
    Validate the structural consistency of a Dasha chain.

    Every child period must belong to its immediate parent,
    and all hierarchical lords must agree.
    """

    if not isinstance(chain, DashaChain):
        raise TypeError(
            "chain must be a DashaChain instance."
        )

    if (
        chain.antardasha.mahadasha_lord
        != chain.mahadasha.planet
    ):
        raise ValueError(
            "Antardasha Mahadasha lord does not match "
            "the parent Mahadasha."
        )

    if (
        chain.pratyantardasha.mahadasha_lord
        != chain.mahadasha.planet
    ):
        raise ValueError(
            "Pratyantardasha Mahadasha lord does not "
            "match the parent Mahadasha."
        )

    if (
        chain.pratyantardasha.antardasha_lord
        != chain.antardasha.antardasha_lord
    ):
        raise ValueError(
            "Pratyantardasha Antardasha lord does not "
            "match the parent Antardasha."
        )

    if (
        chain.sookshma.mahadasha_lord
        != chain.mahadasha.planet
    ):
        raise ValueError(
            "Sookshma Mahadasha lord does not match "
            "the parent Mahadasha."
        )

    if (
        chain.sookshma.antardasha_lord
        != chain.antardasha.antardasha_lord
    ):
        raise ValueError(
            "Sookshma Antardasha lord does not match "
            "the parent Antardasha."
        )

    if (
        chain.sookshma.pratyantardasha_lord
        != chain.pratyantardasha.pratyantardasha_lord
    ):
        raise ValueError(
            "Sookshma Pratyantardasha lord does not "
            "match the parent Pratyantardasha."
        )

    if (
        chain.prana.mahadasha_lord
        != chain.mahadasha.planet
    ):
        raise ValueError(
            "Prana Mahadasha lord does not match "
            "the parent Mahadasha."
        )

    if (
        chain.prana.antardasha_lord
        != chain.antardasha.antardasha_lord
    ):
        raise ValueError(
            "Prana Antardasha lord does not match "
            "the parent Antardasha."
        )

    if (
        chain.prana.pratyantardasha_lord
        != chain.pratyantardasha.pratyantardasha_lord
    ):
        raise ValueError(
            "Prana Pratyantardasha lord does not match "
            "the parent Pratyantardasha."
        )

    if (
        chain.prana.sookshma_lord
        != chain.sookshma.sookshma_lord
    ):
        raise ValueError(
            "Prana Sookshma lord does not match "
            "the parent Sookshma Dasha."
        )

    if (
        chain.deha.mahadasha_lord
        != chain.mahadasha.planet
    ):
        raise ValueError(
            "Deha Mahadasha lord does not match "
            "the parent Mahadasha."
        )

    if (
        chain.deha.antardasha_lord
        != chain.antardasha.antardasha_lord
    ):
        raise ValueError(
            "Deha Antardasha lord does not match "
            "the parent Antardasha."
        )

    if (
        chain.deha.pratyantardasha_lord
        != chain.pratyantardasha.pratyantardasha_lord
    ):
        raise ValueError(
            "Deha Pratyantardasha lord does not match "
            "the parent Pratyantardasha."
        )

    if (
        chain.deha.sookshma_lord
        != chain.sookshma.sookshma_lord
    ):
        raise ValueError(
            "Deha Sookshma lord does not match "
            "the parent Sookshma Dasha."
        )

    if (
        chain.deha.prana_lord
        != chain.prana.prana_lord
    ):
        raise ValueError(
            "Deha Prana lord does not match "
            "the parent Prana Dasha."
        )

    if not (
        chain.mahadasha.start
        <= chain.antardasha.start
        <= chain.antardasha.end
        <= chain.mahadasha.end
    ):
        raise ValueError(
            "Antardasha interval is outside its "
            "Mahadasha interval."
        )

    if not (
        chain.antardasha.start
        <= chain.pratyantardasha.start
        <= chain.pratyantardasha.end
        <= chain.antardasha.end
    ):
        raise ValueError(
            "Pratyantardasha interval is outside its "
            "Antardasha interval."
        )

    if not (
        chain.pratyantardasha.start
        <= chain.sookshma.start
        <= chain.sookshma.end
        <= chain.pratyantardasha.end
    ):
        raise ValueError(
            "Sookshma interval is outside its "
            "Pratyantardasha interval."
        )

    if not (
        chain.sookshma.start
        <= chain.prana.start
        <= chain.prana.end
        <= chain.sookshma.end
    ):
        raise ValueError(
            "Prana interval is outside its "
            "Sookshma Dasha interval."
        )

    if not (
        chain.prana.start
        <= chain.deha.start
        <= chain.deha.end
        <= chain.prana.end
    ):
        raise ValueError(
            "Deha interval is outside its "
            "Prana Dasha interval."
        )


# ============================================================
# Mahadasha Timeline
# ============================================================

def generate_dasha_timeline(
    birth_datetime: datetime,
    moon_longitude: float,
    count: int = 9,
) -> List[Mahadasha]:
    """
    Generate the Mahadasha timeline.

    This is a thin integration wrapper around
    astrology.dasha.generate_mahadashas().
    """

    _validate_birth_datetime(
        birth_datetime
    )

    return generate_mahadashas(
        birth_datetime,
        moon_longitude,
        count=count,
    )


# ============================================================
# Complete Hierarchy for One Mahadasha
# ============================================================

def generate_complete_dasha_timeline(
    mahadasha: Mahadasha,
) -> List[DashaChain]:
    """
    Generate complete six-level Dasha chains for one Mahadasha.

    Each returned DashaChain represents one Deha Dasha and
    contains its complete parent hierarchy.

    Therefore, a single Mahadasha produces:

        9 Antardashas
        81 Pratyantardashas
        729 Sookshma Dashas
        6561 Prana Dashas
        59049 Deha Dashas

    Returns
    -------
    List[DashaChain]
        Complete flattened hierarchy for the supplied
        Mahadasha.
    """

    if not isinstance(mahadasha, Mahadasha):
        raise TypeError(
            "mahadasha must be a Mahadasha instance."
        )

    chains: List[DashaChain] = []

    antardashas = generate_antardashas(
        mahadasha
    )

    for antardasha in antardashas:

        pratyantardashas = (
            generate_pratyantardashas(
                antardasha
            )
        )

        for pratyantardasha in (
            pratyantardashas
        ):

            sookshmadashas = (
                generate_sookshmadashas(
                    pratyantardasha
                )
            )

            for sookshma in sookshmadashas:

                pranadashas = (
                    generate_pranadashas(
                        sookshma
                    )
                )

                for prana in pranadashas:

                    dehadashas = (
                        generate_dehadashas(
                            prana
                        )
                    )

                    for deha in dehadashas:

                        chain = DashaChain(
                            mahadasha=mahadasha,
                            antardasha=antardasha,
                            pratyantardasha=(
                                pratyantardasha
                            ),
                            sookshma=sookshma,
                            prana=prana,
                            deha=deha,
                        )

                        _validate_chain(
                            chain
                        )

                        chains.append(
                            chain
                        )

    return chains


# ============================================================
# Complete Timeline
# ============================================================

def generate_full_dasha_timeline(
    birth_datetime: datetime,
    moon_longitude: float,
    count: int = 9,
) -> List[DashaChain]:
    """
    Generate the complete flattened Vimshottari hierarchy.

    Each item represents one Deha Dasha together with all
    five parent levels.

    Warning
    -------
    A nine-Mahadasha timeline produces a very large number
    of nested periods. Use a smaller count when only a
    limited historical/future range is required.
    """

    _validate_birth_datetime(
        birth_datetime
    )

    mahadashas = generate_mahadashas(
        birth_datetime,
        moon_longitude,
        count=count,
    )

    chains: List[DashaChain] = []

    for mahadasha in mahadashas:

        chains.extend(
            generate_complete_dasha_timeline(
                mahadasha
            )
        )

    return chains


# ============================================================
# Current Dasha Chain
# ============================================================

def current_dasha_chain(
    birth_datetime: datetime,
    moon_longitude: float,
    moment: Optional[datetime] = None,
) -> DashaChain:
    """
    Resolve the complete active Vimshottari Dasha chain.

    Parameters
    ----------
    birth_datetime:
        Birth datetime.

    moon_longitude:
        Sidereal Moon longitude in degrees.

    moment:
        Datetime to evaluate.

        If omitted, the current system time is used with
        the timezone attached to birth_datetime.

    Returns
    -------
    DashaChain
        Complete active hierarchy:

            Mahadasha
            Antardasha
            Pratyantardasha
            Sookshma
            Prana
            Deha
    """

    _validate_birth_datetime(
        birth_datetime
    )

    if moment is None:

        moment = datetime.now(
            tz=birth_datetime.tzinfo
        )

    _validate_moment(
        moment
    )

    mahadasha = current_mahadasha(
        birth_datetime,
        moon_longitude,
        moment,
    )

    antardasha = current_antardasha(
        birth_datetime,
        moon_longitude,
        moment,
    )

    pratyantardasha = current_pratyantardasha(
        antardasha,
        moment,
    )

    sookshma = current_sookshmadasha(
        pratyantardasha,
        moment,
    )

    prana = current_pranadasha(
        sookshma,
        moment,
    )

    deha = current_dehadasha(
        prana,
        moment,
    )

    chain = DashaChain(
        mahadasha=mahadasha,
        antardasha=antardasha,
        pratyantardasha=pratyantardasha,
        sookshma=sookshma,
        prana=prana,
        deha=deha,
    )

    _validate_chain(
        chain
    )

    return chain


# ============================================================
# Current Lords
# ============================================================

def current_dasha_lords(
    birth_datetime: datetime,
    moon_longitude: float,
    moment: Optional[datetime] = None,
) -> dict:
    """
    Return the active Dasha lords as a dictionary.

    Keys:

        mahadasha
        antardasha
        pratyantardasha
        sookshma
        prana
        deha
    """

    chain = current_dasha_chain(
        birth_datetime,
        moon_longitude,
        moment,
    )

    return {
        "mahadasha": chain.mahadasha_lord,
        "antardasha": chain.antardasha_lord,
        "pratyantardasha": (
            chain.pratyantardasha_lord
        ),
        "sookshma": chain.sookshma_lord,
        "prana": chain.prana_lord,
        "deha": chain.deha_lord,
    }


# ============================================================
# Public API
# ============================================================

__all__ = [
    "DashaChain",
    "generate_dasha_timeline",
    "generate_complete_dasha_timeline",
    "generate_full_dasha_timeline",
    "current_dasha_chain",
    "current_dasha_lords",
]