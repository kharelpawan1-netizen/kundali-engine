"""
interpretation/dasha_analysis.py

Interpretation layer for the Vimshottari Dasha system.

This module consumes already-calculated Dasha information from the
astrology calculation layer.

It does NOT:

    - calculate Vimshottari Dasha periods
    - calculate planetary positions
    - calculate houses
    - calculate planetary dignity
    - calculate aspects
    - detect Yogas
    - calculate Vargas
    - make deterministic predictions

Its responsibility is to provide a conservative interpretive
representation of existing Dasha periods.

The interpretation is intentionally structural and contextual.
Planetary results are described as interpretive themes rather than
guaranteed events.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence


# ============================================================
# DASHA THEMES
# ============================================================

DASHA_THEMES: Dict[str, List[str]] = {
    "Ketu": [
        "detachment",
        "introspection",
        "spiritual inquiry",
        "simplification",
        "letting go",
    ],
    "Venus": [
        "relationships",
        "comfort",
        "aesthetics",
        "resources",
        "social and material refinement",
    ],
    "Sun": [
        "identity",
        "authority",
        "leadership",
        "confidence",
        "responsibility",
    ],
    "Moon": [
        "emotional life",
        "mind",
        "nurturing",
        "adaptability",
        "public and family concerns",
    ],
    "Mars": [
        "initiative",
        "action",
        "courage",
        "competition",
        "assertion",
    ],
    "Rahu": [
        "ambition",
        "unconventional development",
        "intensification of desires",
        "foreign or unfamiliar influences",
        "experimentation",
    ],
    "Jupiter": [
        "learning",
        "wisdom",
        "guidance",
        "expansion",
        "ethics and meaning",
    ],
    "Saturn": [
        "discipline",
        "responsibility",
        "patience",
        "structure",
        "long-term development",
    ],
    "Mercury": [
        "learning",
        "communication",
        "analysis",
        "trade and transactions",
        "intellectual activity",
    ],
}


DASHA_CAUTIONS: Dict[str, List[str]] = {
    "Ketu": [
        "detachment should not automatically be interpreted as loss",
        "spiritual or inward themes should be interpreted alongside chart context",
    ],
    "Venus": [
        "comfort and relationship themes should be assessed with Venus dignity and house placement",
        "material or relational themes should not be treated as guaranteed outcomes",
    ],
    "Sun": [
        "authority themes should be assessed with the Sun's dignity, house, and associations",
        "confidence should not automatically be interpreted as status or success",
    ],
    "Moon": [
        "emotional themes should be assessed with the Moon's dignity and associations",
        "mental or family themes should not be interpreted independently of the complete chart",
    ],
    "Mars": [
        "increased activity should not automatically be interpreted as conflict",
        "assertive themes should be assessed with Mars dignity and associations",
    ],
    "Rahu": [
        "intensification and unconventional themes require careful chart-level context",
        "Rahu-related ambition should not be treated as inherently positive or negative",
    ],
    "Jupiter": [
        "expansion should be assessed together with Jupiter's dignity, house, and associations",
        "growth should not automatically be interpreted as guaranteed material success",
    ],
    "Saturn": [
        "delay or responsibility should not automatically be interpreted as failure",
        "Saturn themes should be assessed in relation to dignity, house, and associations",
    ],
    "Mercury": [
        "intellectual and commercial themes depend on Mercury's dignity and associations",
        "communication themes should not be interpreted independently of chart context",
    ],
}


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class DashaInterpretation:
    """
    Immutable interpretation of one Dasha period or hierarchy.

    The object describes the calculated Dasha structure and
    associated interpretive themes without making deterministic
    predictions.
    """

    planet: str

    level: str

    start: Optional[datetime] = None

    end: Optional[datetime] = None

    duration_years: Optional[float] = None

    parent_lord: Optional[str] = None

    themes: List[str] = field(
        default_factory=list
    )

    evidence: List[str] = field(
        default_factory=list
    )

    cautions: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def duration_days(self) -> Optional[float]:
        """Return the period duration in days when dates are available."""

        if self.start is None or self.end is None:
            return None

        return (
            self.end - self.start
        ).total_seconds() / 86400.0

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable copy of the interpretation."""

        return {
            "planet": self.planet,
            "level": self.level,
            "start": self.start,
            "end": self.end,
            "duration_years": self.duration_years,
            "parent_lord": self.parent_lord,
            "themes": list(
                self.themes
            ),
            "evidence": list(
                self.evidence
            ),
            "cautions": list(
                self.cautions
            ),
            "metadata": dict(
                self.metadata
            ),
        }


@dataclass(frozen=True)
class DashaHierarchyInterpretation:
    """
    Immutable interpretation of an active Vimshottari hierarchy.

    The hierarchy can contain:

        Mahadasha
        Antardasha
        Pratyantardasha
        Sookshma
        Prana
        Deha

    Only levels actually supplied by the calculation layer are
    represented.
    """

    mahadasha: Optional[DashaInterpretation] = None

    antardasha: Optional[DashaInterpretation] = None

    pratyantardasha: Optional[DashaInterpretation] = None

    sookshma: Optional[DashaInterpretation] = None

    prana: Optional[DashaInterpretation] = None

    deha: Optional[DashaInterpretation] = None

    moment: Optional[datetime] = None

    themes: List[str] = field(
        default_factory=list
    )

    evidence: List[str] = field(
        default_factory=list
    )

    cautions: List[str] = field(
        default_factory=list
    )

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable hierarchy."""

        return {
            "mahadasha": (
                self.mahadasha.to_dict()
                if self.mahadasha is not None
                else None
            ),
            "antardasha": (
                self.antardasha.to_dict()
                if self.antardasha is not None
                else None
            ),
            "pratyantardasha": (
                self.pratyantardasha.to_dict()
                if self.pratyantardasha is not None
                else None
            ),
            "sookshma": (
                self.sookshma.to_dict()
                if self.sookshma is not None
                else None
            ),
            "prana": (
                self.prana.to_dict()
                if self.prana is not None
                else None
            ),
            "deha": (
                self.deha.to_dict()
                if self.deha is not None
                else None
            ),
            "moment": self.moment,
            "themes": list(
                self.themes
            ),
            "evidence": list(
                self.evidence
            ),
            "cautions": list(
                self.cautions
            ),
        }


# ============================================================
# NORMALIZATION
# ============================================================

def _text(
    value: Any,
) -> str:
    """Normalize a value to stripped text."""

    if value is None:
        return ""

    return str(
        value
    ).strip()


def _unique_preserve_order(
    values: Iterable[str],
) -> List[str]:
    """Remove duplicate text while preserving order."""

    result: List[str] = []
    seen = set()

    for value in values:

        normalized = _text(
            value
        )

        if not normalized:
            continue

        key = normalized.lower()

        if key in seen:
            continue

        seen.add(
            key
        )

        result.append(
            normalized
        )

    return result


def _normalize_planet(
    planet: Any,
) -> str:
    """
    Normalize a Dasha lord.

    Accepts either a string or an object exposing ``planet`` or
    ``name``.
    """

    if planet is None:
        return ""

    if isinstance(
        planet,
        str,
    ):
        return planet.strip()

    value = getattr(
        planet,
        "planet",
        None,
    )

    if value is None:
        value = getattr(
            planet,
            "name",
            None,
        )

    return _text(
        value
    )


# ============================================================
# PERIOD EXTRACTION
# ============================================================

def _period_start(
    period: Any,
) -> Optional[datetime]:
    """Return a Dasha period start when available."""

    value = getattr(
        period,
        "start",
        None,
    )

    if isinstance(
        value,
        datetime,
    ):
        return value

    return None


def _period_end(
    period: Any,
) -> Optional[datetime]:
    """Return a Dasha period end when available."""

    value = getattr(
        period,
        "end",
        None,
    )

    if isinstance(
        value,
        datetime,
    ):
        return value

    return None


def _period_duration_years(
    period: Any,
) -> Optional[float]:
    """Return calculated Dasha duration when available."""

    value = getattr(
        period,
        "duration_years",
        None,
    )

    if value is None:
        return None

    try:
        return float(
            value
        )

    except (
        TypeError,
        ValueError,
    ):
        return None


# ============================================================
# THEME / CAUTION ACCESS
# ============================================================

def dasha_themes(
    planet: str,
) -> List[str]:
    """
    Return the standard interpretive themes associated with a
    Dasha lord.

    Unknown lords receive a conservative fallback.
    """

    normalized = _normalize_planet(
        planet
    )

    if not normalized:
        return []

    for known_planet in DASHA_THEMES:

        if known_planet.lower() == normalized.lower():

            return list(
                DASHA_THEMES[
                    known_planet
                ]
            )

    return [
        "interpretation depends on the specific Dasha lord and complete chart context",
    ]


def dasha_cautions(
    planet: str,
) -> List[str]:
    """
    Return conservative interpretive cautions for a Dasha lord.
    """

    normalized = _normalize_planet(
        planet
    )

    if not normalized:
        return []

    for known_planet in DASHA_CAUTIONS:

        if known_planet.lower() == normalized.lower():

            return list(
                DASHA_CAUTIONS[
                    known_planet
                ]
            )

    return [
        "Dasha symbolism should not be treated as a deterministic prediction.",
    ]


# ============================================================
# SINGLE DASHA INTERPRETATION
# ============================================================

def interpret_dasha(
    period: Any,
    *,
    level: str = "mahadasha",
    parent_lord: Optional[str] = None,
) -> DashaInterpretation:
    """
    Interpret an already-calculated Dasha period.

    Parameters
    ----------
    period:
        Existing Mahadasha, Antardasha, or compatible period object.

    level:
        Interpretation level, such as ``mahadasha`` or
        ``antardasha``.

    parent_lord:
        Optional parent Dasha lord.

    Returns
    -------
    DashaInterpretation

    Notes
    -----
    No Dasha calculation occurs here.
    """

    if period is None:
        raise ValueError(
            "period must not be None."
        )

    planet = _normalize_planet(
        period
    )

    if not planet:
        raise ValueError(
            "Dasha period must expose a planet or lord."
        )

    normalized_level = _text(
        level
    ).lower()

    if not normalized_level:
        raise ValueError(
            "level must not be empty."
        )

    start = _period_start(
        period
    )

    end = _period_end(
        period
    )

    duration_years = _period_duration_years(
        period
    )

    themes = dasha_themes(
        planet
    )

    cautions = dasha_cautions(
        planet
    )

    evidence = [
        (
            f"{normalized_level} lord is {planet}."
        )
    ]

    if start is not None and end is not None:

        evidence.append(
            (
                f"{normalized_level.capitalize()} period "
                f"runs from {start.isoformat()} "
                f"to {end.isoformat()}."
            )
        )

    if duration_years is not None:

        evidence.append(
            (
                f"Calculated {normalized_level} "
                f"duration is {duration_years:.6f} years."
            )
        )

    if parent_lord:

        evidence.append(
            (
                f"The {normalized_level} operates within "
                f"the {parent_lord} Dasha."
            )
        )

    metadata = {
        "calculation_source": (
            type(period).__name__
        ),
        "interpretation_level": (
            normalized_level
        ),
    }

    return DashaInterpretation(
        planet=planet,
        level=normalized_level,
        start=start,
        end=end,
        duration_years=duration_years,
        parent_lord=(
            _normalize_planet(
                parent_lord
            )
            if parent_lord
            else None
        ),
        themes=themes,
        evidence=_unique_preserve_order(
            evidence
        ),
        cautions=_unique_preserve_order(
            cautions
        ),
        metadata=metadata,
    )


# ============================================================
# DASHA COLLECTION INTERPRETATION
# ============================================================

def interpret_dasha_periods(
    periods: Iterable[Any],
    *,
    level: str = "mahadasha",
    parent_lord: Optional[str] = None,
) -> List[DashaInterpretation]:
    """
    Interpret an iterable of already-calculated Dasha periods.

    The original order is preserved.
    """

    if periods is None:
        raise ValueError(
            "periods must not be None."
        )

    return [
        interpret_dasha(
            period,
            level=level,
            parent_lord=parent_lord,
        )
        for period in periods
    ]


# ============================================================
# HIERARCHY INTERPRETATION
# ============================================================

def _interpret_hierarchy_level(
    period: Any,
    level: str,
    parent_lord: Optional[str],
) -> Optional[DashaInterpretation]:
    """Interpret one optional hierarchy level."""

    if period is None:
        return None

    return interpret_dasha(
        period,
        level=level,
        parent_lord=parent_lord,
    )


def interpret_dasha_hierarchy(
    *,
    mahadasha: Any = None,
    antardasha: Any = None,
    pratyantardasha: Any = None,
    sookshma: Any = None,
    prana: Any = None,
    deha: Any = None,
    moment: Optional[datetime] = None,
) -> DashaHierarchyInterpretation:
    """
    Interpret an existing Vimshottari Dasha hierarchy.

    The caller supplies already-calculated periods.

    No period calculation or astronomical calculation occurs here.
    """

    md = _interpret_hierarchy_level(
        mahadasha,
        "mahadasha",
        None,
    )

    ad_parent = (
        md.planet
        if md is not None
        else None
    )

    ad = _interpret_hierarchy_level(
        antardasha,
        "antardasha",
        ad_parent,
    )

    pd_parent = (
        ad.planet
        if ad is not None
        else ad_parent
    )

    pd = _interpret_hierarchy_level(
        pratyantardasha,
        "pratyantardasha",
        pd_parent,
    )

    sd_parent = (
        pd.planet
        if pd is not None
        else pd_parent
    )

    sd = _interpret_hierarchy_level(
        sookshma,
        "sookshma",
        sd_parent,
    )

    prana_parent = (
        sd.planet
        if sd is not None
        else sd_parent
    )

    prana_result = _interpret_hierarchy_level(
        prana,
        "prana",
        prana_parent,
    )

    deha_parent = (
        prana_result.planet
        if prana_result is not None
        else prana_parent
    )

    deha_result = _interpret_hierarchy_level(
        deha,
        "deha",
        deha_parent,
    )

    interpretations = [
        interpretation
        for interpretation in (
            md,
            ad,
            pd,
            sd,
            prana_result,
            deha_result,
        )
        if interpretation is not None
    ]

    themes = collect_dasha_themes(
        interpretations
    )

    evidence = collect_dasha_evidence(
        interpretations
    )

    cautions = collect_dasha_cautions(
        interpretations
    )

    return DashaHierarchyInterpretation(
        mahadasha=md,
        antardasha=ad,
        pratyantardasha=pd,
        sookshma=sd,
        prana=prana_result,
        deha=deha_result,
        moment=moment,
        themes=themes,
        evidence=evidence,
        cautions=cautions,
    )


# ============================================================
# COLLECTION HELPERS
# ============================================================

def collect_dasha_themes(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique themes from Dasha interpretations.
    """

    if interpretations is None:
        return []

    themes: List[str] = []

    for interpretation in interpretations:

        values = getattr(
            interpretation,
            "themes",
            None,
        )

        if values is None:
            continue

        themes.extend(
            _text(value)
            for value in values
        )

    return _unique_preserve_order(
        themes
    )


def collect_dasha_evidence(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique evidence statements from Dasha
    interpretations.
    """

    if interpretations is None:
        return []

    evidence: List[str] = []

    for interpretation in interpretations:

        values = getattr(
            interpretation,
            "evidence",
            None,
        )

        if values is None:
            continue

        evidence.extend(
            _text(value)
            for value in values
        )

    return _unique_preserve_order(
        evidence
    )


def collect_dasha_cautions(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique cautions from Dasha interpretations.
    """

    if interpretations is None:
        return []

    cautions: List[str] = []

    for interpretation in interpretations:

        values = getattr(
            interpretation,
            "cautions",
            None,
        )

        if values is None:
            continue

        cautions.extend(
            _text(value)
            for value in values
        )

    return _unique_preserve_order(
        cautions
    )


# ============================================================
# CURRENT DASHA CONTEXT
# ============================================================

def interpret_current_dasha(
    context: Any,
) -> DashaHierarchyInterpretation:
    """
    Interpret the current Dasha hierarchy from an existing
    interpretation/calculation context.

    Supported context attributes are:

        current_mahadasha
        current_antardasha
        current_pratyantardasha
        current_sookshmadasha
        current_pranadasha
        current_dehadasha
        current_moment

    The function also accepts the normalized ``DashaContext``
    structure used by ``interpretation.context``.

    No Dasha periods are recalculated.
    """

    if context is None:
        raise ValueError(
            "context must not be None."
        )

    md = getattr(
        context,
        "current_mahadasha",
        None,
    )

    ad = getattr(
        context,
        "current_antardasha",
        None,
    )

    pd = getattr(
        context,
        "current_pratyantardasha",
        None,
    )

    sd = getattr(
        context,
        "current_sookshmadasha",
        None,
    )

    prana = getattr(
        context,
        "current_pranadasha",
        None,
    )

    deha = getattr(
        context,
        "current_dehadasha",
        None,
    )

    moment = getattr(
        context,
        "current_moment",
        None,
    )

    # The normalized InterpretationContext stores the hierarchy
    # under ``context.dasha``.
    dasha_context = getattr(
        context,
        "dasha",
        None,
    )

    if dasha_context is not None:

        if md is None:
            md = getattr(
                dasha_context,
                "mahadasha",
                None,
            )

        if ad is None:
            ad = getattr(
                dasha_context,
                "antardasha",
                None,
            )

        if pd is None:
            pd = getattr(
                dasha_context,
                "pratyantardasha",
                None,
            )

        if sd is None:
            sd = getattr(
                dasha_context,
                "sookshma",
                None,
            )

        if prana is None:
            prana = getattr(
                dasha_context,
                "prana",
                None,
            )

        if deha is None:
            deha = getattr(
                dasha_context,
                "deha",
                None,
            )

        if moment is None:
            moment = getattr(
                dasha_context,
                "moment",
                None,
            )

    return interpret_dasha_hierarchy(
        mahadasha=md,
        antardasha=ad,
        pratyantardasha=pd,
        sookshma=sd,
        prana=prana,
        deha=deha,
        moment=(
            moment
            if isinstance(
                moment,
                datetime,
            )
            else None
        ),
    )


# ============================================================
# DASHA ACCESSORS
# ============================================================

def active_dasha_lords(
    interpretation: DashaHierarchyInterpretation,
) -> List[str]:
    """
    Return active Dasha lords from highest to lowest hierarchy.
    """

    if interpretation is None:
        raise ValueError(
            "interpretation must not be None."
        )

    result: List[str] = []

    for period in (
        interpretation.mahadasha,
        interpretation.antardasha,
        interpretation.pratyantardasha,
        interpretation.sookshma,
        interpretation.prana,
        interpretation.deha,
    ):

        if period is None:
            continue

        if period.planet:
            result.append(
                period.planet
            )

    return result


def dasha_interpretations_involving_planet(
    interpretations: Iterable[DashaInterpretation],
    planet: str,
) -> List[DashaInterpretation]:
    """
    Return Dasha interpretations belonging to a specified lord.

    Planet comparison is case-insensitive.
    """

    if interpretations is None:
        raise ValueError(
            "interpretations must not be None."
        )

    if planet is None:
        raise ValueError(
            "planet must not be None."
        )

    normalized = _text(
        planet
    ).lower()

    if not normalized:
        raise ValueError(
            "planet must not be empty."
        )

    return [
        interpretation
        for interpretation in interpretations
        if interpretation.planet.strip().lower()
        == normalized
    ]


# ============================================================
# REPORT
# ============================================================

def dasha_analysis_report(
    interpretation: DashaHierarchyInterpretation,
) -> List[str]:
    """
    Produce a concise evidence-oriented Dasha report.
    """

    if interpretation is None:
        raise ValueError(
            "interpretation must not be None."
        )

    report: List[str] = []

    periods = (
        (
            "Mahadasha",
            interpretation.mahadasha,
        ),
        (
            "Antardasha",
            interpretation.antardasha,
        ),
        (
            "Pratyantardasha",
            interpretation.pratyantardasha,
        ),
        (
            "Sookshma",
            interpretation.sookshma,
        ),
        (
            "Prana",
            interpretation.prana,
        ),
        (
            "Deha",
            interpretation.deha,
        ),
    )

    for label, period in periods:

        if period is None:
            continue

        line = (
            f"{label}: {period.planet}"
        )

        if period.start is not None:

            line += (
                f"; start={period.start.isoformat()}"
            )

        if period.end is not None:

            line += (
                f"; end={period.end.isoformat()}"
            )

        report.append(
            line
        )

    if interpretation.themes:

        report.append(
            "Themes: "
            + ", ".join(
                interpretation.themes
            )
            + "."
        )

    if interpretation.cautions:

        report.append(
            "Cautions: "
            + " | ".join(
                interpretation.cautions
            )
            + "."
        )

    return report


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "DASHA_THEMES",
    "DASHA_CAUTIONS",
    "DashaInterpretation",
    "DashaHierarchyInterpretation",
    "dasha_themes",
    "dasha_cautions",
    "interpret_dasha",
    "interpret_dasha_periods",
    "interpret_dasha_hierarchy",
    "interpret_current_dasha",
    "collect_dasha_themes",
    "collect_dasha_evidence",
    "collect_dasha_cautions",
    "active_dasha_lords",
    "dasha_interpretations_involving_planet",
    "dasha_analysis_report",
]