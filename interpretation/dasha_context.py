"""
interpretation/dasha_context.py

Interpretation-facing integration for the complete Vimshottari
Dasha hierarchy.

This module consumes the authoritative DashaChain produced by:

    astrology.dasha_timeline

It does NOT:
    - calculate Dasha periods
    - regenerate Dasha hierarchies
    - determine planetary strength
    - evaluate yogas
    - make predictions
    - alter the calculation engine

Its sole responsibility is to expose the complete active
Mahadasha → Antardasha → Pratyantardasha → Sookshma →
Prana → Deha hierarchy in a normalized interpretation-facing
form.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from astrology.dasha_timeline import DashaChain


# ============================================================
# Data Model
# ============================================================

@dataclass(frozen=True)
class DashaHierarchyContext:
    """
    Normalized interpretation context for the complete active
    Vimshottari Dasha hierarchy.

    The hierarchy represents one exact evaluation moment:

        Mahadasha
            ↓
        Antardasha
            ↓
        Pratyantardasha
            ↓
        Sookshma
            ↓
        Prana
            ↓
        Deha
    """

    mahadasha: str
    antardasha: str
    pratyantardasha: str
    sookshma: str
    prana: str
    deha: str

    start: datetime
    end: datetime

    moment: Optional[datetime] = None

    @property
    def lords(self) -> tuple:
        """
        Return all active Dasha lords in hierarchical order.
        """

        return (
            self.mahadasha,
            self.antardasha,
            self.pratyantardasha,
            self.sookshma,
            self.prana,
            self.deha,
        )

    @property
    def depth(self) -> int:
        """
        Return the number of active Dasha levels.

        A complete hierarchy always contains six levels.
        """

        return 6

    @property
    def most_specific_lord(self) -> str:
        """
        Return the lord of the most specific active period.

        The most specific level is Deha Dasha.
        """

        return self.deha

    @property
    def broadest_lord(self) -> str:
        """
        Return the lord of the broadest active period.

        The broadest level is Mahadasha.
        """

        return self.mahadasha

    def contains(
        self,
        moment: datetime,
    ) -> bool:
        """
        Return True when the supplied moment falls inside
        the active Deha interval represented by this context.
        """

        if not isinstance(
            moment,
            datetime,
        ):
            raise TypeError(
                "moment must be a datetime."
            )

        return (
            self.start
            <= moment
            < self.end
        )


# ============================================================
# Validation
# ============================================================

def _validate_chain(
    chain: DashaChain,
) -> None:
    """
    Validate the supplied DashaChain.

    The calculation engine already performs structural
    validation. This validation exists at the interpretation
    boundary so invalid objects cannot silently enter the
    interpretation layer.
    """

    if not isinstance(
        chain,
        DashaChain,
    ):
        raise TypeError(
            "chain must be a DashaChain instance."
        )


def _validate_moment(
    moment: Optional[datetime],
) -> None:
    """Validate an optional evaluation moment."""

    if moment is not None and not isinstance(
        moment,
        datetime,
    ):
        raise TypeError(
            "moment must be a datetime or None."
        )


# ============================================================
# Context Construction
# ============================================================

def build_dasha_hierarchy_context(
    chain: DashaChain,
    moment: Optional[datetime] = None,
) -> DashaHierarchyContext:
    """
    Convert an authoritative DashaChain into a normalized
    interpretation-facing DashaHierarchyContext.

    Parameters
    ----------
    chain:
        Complete active DashaChain produced by
        astrology.dasha_timeline.current_dasha_chain().

    moment:
        Optional evaluation moment associated with the context.

        If supplied, it must be a datetime and must fall inside
        the represented active Deha interval.

        If omitted, the context does not invent a new evaluation
        time.

    Returns
    -------
    DashaHierarchyContext
        Immutable interpretation-facing Dasha hierarchy.

    Notes
    -----
    This function performs no Dasha calculation.

    All planetary lords and period boundaries are copied directly
    from the authoritative DashaChain.
    """

    _validate_chain(
        chain
    )

    _validate_moment(
        moment
    )

    if moment is not None:

        if not (
            chain.start
            <= moment
            < chain.end
        ):
            raise ValueError(
                "moment falls outside the active "
                "Deha Dasha interval."
            )

    return DashaHierarchyContext(
        mahadasha=chain.mahadasha_lord,

        antardasha=chain.antardasha_lord,

        pratyantardasha=(
            chain.pratyantardasha_lord
        ),

        sookshma=chain.sookshma_lord,

        prana=chain.prana_lord,

        deha=chain.deha_lord,

        start=chain.start,

        end=chain.end,

        moment=moment,
    )


# ============================================================
# Convenience Accessors
# ============================================================

def get_dasha_lord(
    context: DashaHierarchyContext,
    level: str,
) -> str:
    """
    Return the active lord at a requested Dasha level.

    Supported levels:

        mahadasha
        antardasha
        pratyantardasha
        sookshma
        prana
        deha

    Parameters
    ----------
    context:
        Normalized DashaHierarchyContext.

    level:
        Name of the requested Dasha level.

    Returns
    -------
    str
        Active planetary lord.
    """

    if not isinstance(
        context,
        DashaHierarchyContext,
    ):
        raise TypeError(
            "context must be a "
            "DashaHierarchyContext instance."
        )

    if not isinstance(
        level,
        str,
    ):
        raise TypeError(
            "level must be a string."
        )

    normalized_level = (
        level.strip().lower()
    )

    levels = {
        "mahadasha": context.mahadasha,
        "antardasha": context.antardasha,
        "pratyantardasha": (
            context.pratyantardasha
        ),
        "sookshma": context.sookshma,
        "prana": context.prana,
        "deha": context.deha,
    }

    try:
        return levels[
            normalized_level
        ]

    except KeyError as exc:
        raise ValueError(
            "Unknown Dasha level: "
            f"{level}. Supported levels are: "
            "mahadasha, antardasha, "
            "pratyantardasha, sookshma, "
            "prana, deha."
        ) from exc


def get_dasha_chain(
    context: DashaHierarchyContext,
) -> tuple:
    """
    Return the complete active Dasha hierarchy as a tuple.

    The order is:

        Mahadasha
        Antardasha
        Pratyantardasha
        Sookshma
        Prana
        Deha
    """

    if not isinstance(
        context,
        DashaHierarchyContext,
    ):
        raise TypeError(
            "context must be a "
            "DashaHierarchyContext instance."
        )

    return context.lords


# ============================================================
# Integration with Existing InterpretationContext
# ============================================================

def attach_dasha_context(
    interpretation_context: object,
    dasha_context: DashaHierarchyContext,
) -> object:
    """
    Attach the normalized Dasha hierarchy to an existing
    InterpretationContext without modifying its public API.

    This function intentionally returns a new object rather than
    mutating the supplied interpretation context.

    The existing InterpretationContext is a frozen dataclass, so
    dataclasses.replace() is used when the supplied object is the
    expected InterpretationContext type.

    Parameters
    ----------
    interpretation_context:
        Existing interpretation.InterpretationContext.

    dasha_context:
        Normalized DashaHierarchyContext.

    Returns
    -------
    InterpretationContext
        A copy containing the supplied Dasha hierarchy.

    Notes
    -----
    The current InterpretationContext already contains a
    DashaContext field. Therefore this adapter maps the normalized
    hierarchy into that existing public structure rather than
    introducing a competing field.

    The original DashaContext moment is preserved only when the
    normalized hierarchy does not provide an explicit moment.
    """

    if interpretation_context is None:
        raise ValueError(
            "interpretation_context must not be None."
        )

    if not isinstance(
        dasha_context,
        DashaHierarchyContext,
    ):
        raise TypeError(
            "dasha_context must be a "
            "DashaHierarchyContext instance."
        )

    from dataclasses import replace

    try:
        from interpretation.context import (
            DashaContext,
            InterpretationContext,
        )
    except ImportError as exc:
        raise ImportError(
            "Could not import the existing interpretation "
            "context API."
        ) from exc

    if not isinstance(
        interpretation_context,
        InterpretationContext,
    ):
        raise TypeError(
            "interpretation_context must be an "
            "InterpretationContext instance."
        )

    existing_moment = getattr(
        interpretation_context.dasha,
        "moment",
        None,
    )

    moment = (
        dasha_context.moment
        if dasha_context.moment is not None
        else existing_moment
    )

    normalized_dasha = DashaContext(
        mahadasha=dasha_context.mahadasha,
        antardasha=dasha_context.antardasha,
        pratyantardasha=(
            dasha_context.pratyantardasha
        ),
        sookshma=dasha_context.sookshma,
        prana=dasha_context.prana,
        deha=dasha_context.deha,
        moment=moment,
    )

    return replace(
        interpretation_context,
        dasha=normalized_dasha,
    )


# ============================================================
# Public API
# ============================================================

__all__ = [
    "DashaHierarchyContext",
    "build_dasha_hierarchy_context",
    "get_dasha_lord",
    "get_dasha_chain",
    "attach_dasha_context",
]