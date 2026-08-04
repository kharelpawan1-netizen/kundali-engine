"""
interpretation/context.py

Normalized interpretation context for the Vedic interpretation layer.

This module does NOT calculate planetary positions, houses, dashas,
or Vargas. It consumes the already-tested calculation engine.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any


# ============================================================
# Planet Context
# ============================================================

@dataclass(frozen=True)
class PlanetContext:
    """Normalized planetary information for interpretation."""

    name: str
    sign: str
    sign_degree: float
    house: int
    nakshatra: str
    pada: int

    # These are intentionally optional because different
    # calculation modules may expose these attributes later.
    longitude: Optional[float] = None
    retrograde: Optional[bool] = None
    dignity: Optional[str] = None


# ============================================================
# Dasha Context
# ============================================================

@dataclass(frozen=True)
class DashaContext:
    """Current active Vimshottari hierarchy."""

    mahadasha: Optional[str]
    antardasha: Optional[str]
    pratyantardasha: Optional[str]
    sookshma: Optional[str]
    prana: Optional[str]
    deha: Optional[str]

    moment: Optional[datetime] = None


# ============================================================
# Chart Interpretation Context
# ============================================================

@dataclass(frozen=True)
class InterpretationContext:
    """
    Read-only normalized context used by interpretation modules.

    The interpretation layer should depend on this object rather
    than directly manipulating the calculation engine.
    """

    name: str

    birth_datetime: datetime

    place: str
    latitude: float
    longitude: float
    timezone: str

    ascendant_sign: str
    ascendant_degree: float

    planets: Dict[str, PlanetContext]

    dasha: DashaContext

    houses: Dict[int, Any]


# ============================================================
# Safe Attribute Utility
# ============================================================

def _get_attr(
    obj: Any,
    name: str,
    default: Any = None,
) -> Any:
    """
    Safely retrieve an attribute.

    This prevents the interpretation layer from failing merely
    because an optional calculation attribute is unavailable.
    """

    return getattr(
        obj,
        name,
        default,
    )


# ============================================================
# Planet Normalization
# ============================================================

def _normalize_planet(
    planet: Any,
) -> PlanetContext:
    """
    Convert an engine Planet object into PlanetContext.
    """

    return PlanetContext(
        name=str(
            _get_attr(
                planet,
                "name",
                "",
            )
        ),

        sign=str(
            _get_attr(
                planet,
                "sign",
                "",
            )
        ),

        sign_degree=float(
            _get_attr(
                planet,
                "sign_degree",
                0.0,
            )
        ),

        house=int(
            _get_attr(
                planet,
                "house",
                0,
            )
        ),

        nakshatra=str(
            _get_attr(
                planet,
                "nakshatra",
                "",
            )
        ),

        pada=int(
            _get_attr(
                planet,
                "pada",
                0,
            )
        ),

        longitude=_get_attr(
            planet,
            "longitude",
        ),

        retrograde=_get_attr(
            planet,
            "retrograde",
        ),

        dignity=_get_attr(
            planet,
            "dignity",
        ),
    )


# ============================================================
# Dasha Normalization
# ============================================================

def _normalize_dasha(
    chart: Any,
) -> DashaContext:
    """
    Extract the currently active Vimshottari hierarchy.
    """

    md = _get_attr(
        chart,
        "current_mahadasha",
    )

    ad = _get_attr(
        chart,
        "current_antardasha",
    )

    pd = _get_attr(
        chart,
        "current_pratyantardasha",
    )

    sd = _get_attr(
        chart,
        "current_sookshmadasha",
    )

    prana = _get_attr(
        chart,
        "current_pranadasha",
    )

    deha = _get_attr(
        chart,
        "current_dehadasha",
    )

    return DashaContext(
        mahadasha=(
            _get_attr(md, "planet")
            if md is not None
            else None
        ),

        antardasha=(
            _get_attr(
                ad,
                "antardasha_lord",
            )
            if ad is not None
            else None
        ),

        pratyantardasha=(
            _get_attr(
                pd,
                "pratyantardasha_lord",
            )
            if pd is not None
            else None
        ),

        sookshma=(
            _get_attr(
                sd,
                "sookshma_lord",
            )
            if sd is not None
            else None
        ),

        prana=(
            _get_attr(
                prana,
                "prana_lord",
            )
            if prana is not None
            else None
        ),

        deha=(
            _get_attr(
                deha,
                "deha_lord",
            )
            if deha is not None
            else None
        ),

        moment=datetime.now(),
    )


# ============================================================
# Build Context
# ============================================================

def build_interpretation_context(
    chart: Any,
    birth: Any,
) -> InterpretationContext:
    """
    Build the normalized interpretation context.

    Parameters
    ----------
    chart:
        Existing calculated Chart object.

    birth:
        Existing BirthData object.

    Returns
    -------
    InterpretationContext
        Immutable interpretation-ready context.
    """

    if chart is None:
        raise ValueError(
            "chart must not be None."
        )

    if birth is None:
        raise ValueError(
            "birth must not be None."
        )

    location = _get_attr(
        birth,
        "location",
    )

    if location is None:
        raise ValueError(
            "birth.location must not be None."
        )

    ascendant = float(
        _get_attr(
            chart,
            "ascendant",
            0.0,
        )
    )

    # Import locally to keep this module's dependency surface
    # small and avoid unnecessary import-time coupling.
    from astronomy.signs import (
        sign_degree,
        sign_enum,
    )

    asc_sign = sign_enum(
        ascendant
    )

    planets: Dict[
        str,
        PlanetContext,
    ] = {}

    chart_planets = _get_attr(
        chart,
        "planets",
        {},
    )

    for name, planet in chart_planets.items():

        normalized = _normalize_planet(
            planet
        )

        planets[str(name)] = normalized

    houses = dict(
        _get_attr(
            chart,
            "houses",
            {},
        )
    )

    return InterpretationContext(
        name=str(
            _get_attr(
                birth,
                "name",
                "",
            )
        ),

        birth_datetime=_get_attr(
            birth,
            "birth_datetime",
        ),

        place=str(
            _get_attr(
                location,
                "name",
                "",
            )
        ),

        latitude=float(
            _get_attr(
                location,
                "latitude",
                0.0,
            )
        ),

        longitude=float(
            _get_attr(
                location,
                "longitude",
                0.0,
            )
        ),

        timezone=str(
            _get_attr(
                location,
                "timezone",
                "",
            )
        ),

        ascendant_sign=(
            asc_sign.display_name
        ),

        ascendant_degree=float(
            sign_degree(
                ascendant
            )
        ),

        planets=planets,

        dasha=_normalize_dasha(
            chart
        ),

        houses=houses,
    )


# ============================================================
# Convenience Accessors
# ============================================================

def get_planet(
    context: InterpretationContext,
    planet_name: str,
) -> PlanetContext:
    """Return one planet from the interpretation context."""

    try:
        return context.planets[
            planet_name
        ]

    except KeyError as exc:

        raise KeyError(
            f"Planet '{planet_name}' "
            f"not found in interpretation context."
        ) from exc


def get_planets_in_house(
    context: InterpretationContext,
    house_number: int,
) -> List[PlanetContext]:
    """Return all planets occupying a particular house."""

    if not 1 <= house_number <= 12:
        raise ValueError(
            "house_number must be between 1 and 12."
        )

    return [
        planet
        for planet in context.planets.values()
        if planet.house == house_number
    ]


def get_planets_in_sign(
    context: InterpretationContext,
    sign_name: str,
) -> List[PlanetContext]:
    """Return all planets occupying a particular sign."""

    return [
        planet
        for planet in context.planets.values()
        if planet.sign.lower()
        == sign_name.lower()
    ]


# ============================================================
# Public API
# ============================================================

__all__ = [
    "PlanetContext",
    "DashaContext",
    "InterpretationContext",
    "build_interpretation_context",
    "get_planet",
    "get_planets_in_house",
    "get_planets_in_sign",
]