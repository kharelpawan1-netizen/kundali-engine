"""
interpretation/synthesis.py

Chart-level synthesis layer for the Vedic interpretation engine.

This module combines already-computed interpretation evidence from:

    - planet_analysis.py
    - house_analysis.py
    - dignity_analysis.py
    - aspect_analysis.py
    - yoga_analysis.py

It does NOT:

    - calculate planetary positions
    - calculate houses
    - calculate dignity
    - calculate aspects
    - detect Yogas
    - calculate Dashas
    - calculate Vargas
    - generate deterministic predictions

The purpose of this module is evidence aggregation.

Architecture:

    Calculation Engine
            |
            v
    Interpretation Modules
            |
            v
        synthesis.py
            |
            v
    ChartInterpretation

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class ChartInterpretation:
    """
    Unified chart-level interpretation.

    This object contains evidence collected from the existing
    interpretation modules. It deliberately avoids converting
    evidence into deterministic predictions.
    """

    planetary: Dict[str, Any] = field(
        default_factory=dict
    )

    houses: Dict[int, Any] = field(
        default_factory=dict
    )

    dignities: Dict[str, Any] = field(
        default_factory=dict
    )

    aspects: Dict[str, Dict[int, Any]] = field(
        default_factory=dict
    )

    yogas: List[Any] = field(
        default_factory=list
    )

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
    def planet_count(self) -> int:
        """Return the number of planetary interpretations."""

        return len(
            self.planetary
        )

    @property
    def house_count(self) -> int:
        """Return the number of house interpretations."""

        return len(
            self.houses
        )

    @property
    def dignity_count(self) -> int:
        """Return the number of dignity interpretations."""

        return len(
            self.dignities
        )

    @property
    def aspect_count(self) -> int:
        """Return the total number of planetary aspects."""

        return sum(
            len(targets)
            for targets in self.aspects.values()
        )

    @property
    def detected_yoga_count(self) -> int:
        """Return the number of structurally detected Yogas."""

        return sum(
            1
            for yoga in self.yogas
            if bool(
                getattr(
                    yoga,
                    "detected",
                    False,
                )
            )
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the synthesis into a serializable dictionary.

        Nested interpretation objects are converted through
        to_dict() when that method is available.
        """

        return {
            "planetary": _serialize_mapping(
                self.planetary
            ),
            "houses": _serialize_mapping(
                self.houses
            ),
            "dignities": _serialize_mapping(
                self.dignities
            ),
            "aspects": _serialize_nested_mapping(
                self.aspects
            ),
            "yogas": _serialize_sequence(
                self.yogas
            ),
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


# ============================================================
# SERIALIZATION
# ============================================================

def _serialize_value(
    value: Any,
) -> Any:
    """
    Serialize an interpretation object when possible.
    """

    to_dict = getattr(
        value,
        "to_dict",
        None,
    )

    if callable(to_dict):
        return to_dict()

    if isinstance(
        value,
        dict,
    ):
        return {
            key: _serialize_value(item)
            for key, item in value.items()
        }

    if isinstance(
        value,
        (list, tuple),
    ):
        return [
            _serialize_value(item)
            for item in value
        ]

    return value


def _serialize_mapping(
    values: Dict[Any, Any],
) -> Dict[Any, Any]:
    """Serialize a mapping recursively."""

    return {
        key: _serialize_value(value)
        for key, value in values.items()
    }


def _serialize_nested_mapping(
    values: Dict[Any, Dict[Any, Any]],
) -> Dict[Any, Dict[Any, Any]]:
    """Serialize a two-level mapping."""

    return {
        outer_key: {
            inner_key: _serialize_value(
                inner_value
            )
            for inner_key, inner_value
            in inner_values.items()
        }
        for outer_key, inner_values
        in values.items()
    }


def _serialize_sequence(
    values: Sequence[Any],
) -> List[Any]:
    """Serialize a sequence recursively."""

    return [
        _serialize_value(value)
        for value in values
    ]


# ============================================================
# NORMALIZATION
# ============================================================

def _text(
    value: Any,
) -> str:
    """Return normalized text representation."""

    if value is None:
        return ""

    return str(
        value
    ).strip()


def _unique_preserve_order(
    values: Iterable[str],
) -> List[str]:
    """
    Remove duplicate strings while preserving their order.
    """

    result = []
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


# ============================================================
# THEME EXTRACTION
# ============================================================

def _themes_from_interpretation(
    interpretation: Any,
) -> List[str]:
    """
    Extract themes from one interpretation object.
    """

    themes = getattr(
        interpretation,
        "themes",
        None,
    )

    if themes is None:
        return []

    return [
        _text(theme)
        for theme in themes
        if _text(theme)
    ]


def collect_themes(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique themes from interpretation objects.

    Existing interpretation modules remain responsible for
    defining the themes.
    """

    themes = []

    for interpretation in interpretations:

        themes.extend(
            _themes_from_interpretation(
                interpretation
            )
        )

    return _unique_preserve_order(
        themes
    )


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================

def _evidence_from_interpretation(
    interpretation: Any,
) -> List[str]:
    """Extract evidence from one interpretation object."""

    evidence = getattr(
        interpretation,
        "evidence",
        None,
    )

    if evidence is None:
        return []

    return [
        _text(item)
        for item in evidence
        if _text(item)
    ]


def collect_evidence(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique evidence statements.

    Evidence remains descriptive rather than predictive.
    """

    evidence = []

    for interpretation in interpretations:

        evidence.extend(
            _evidence_from_interpretation(
                interpretation
            )
        )

    return _unique_preserve_order(
        evidence
    )


# ============================================================
# CAUTION EXTRACTION
# ============================================================

def _cautions_from_interpretation(
    interpretation: Any,
) -> List[str]:
    """Extract cautions from one interpretation object."""

    cautions = getattr(
        interpretation,
        "cautions",
        None,
    )

    if cautions is None:
        return []

    return [
        _text(caution)
        for caution in cautions
        if _text(caution)
    ]


def collect_cautions(
    interpretations: Iterable[Any],
) -> List[str]:
    """
    Collect unique interpretive cautions.
    """

    cautions = []

    for interpretation in interpretations:

        cautions.extend(
            _cautions_from_interpretation(
                interpretation
            )
        )

    return _unique_preserve_order(
        cautions
    )


# ============================================================
# PLANETARY SYNTHESIS
# ============================================================

def synthesize_planets(
    interpretations: Iterable[Any],
) -> Dict[str, Any]:
    """
    Build a planetary interpretation mapping.

    Planetary interpretation objects are expected to expose
    a ``planet`` attribute.
    """

    result = {}

    for interpretation in interpretations:

        name = _text(
            getattr(
                interpretation,
                "planet",
                "",
            )
        )

        if not name:
            continue

        result[name] = interpretation

    return result


# ============================================================
# HOUSE SYNTHESIS
# ============================================================

def synthesize_houses(
    interpretations: Iterable[Any],
) -> Dict[int, Any]:
    """
    Build a house interpretation mapping.

    House interpretation objects are expected to expose
    a ``house`` attribute.
    """

    result = {}

    for interpretation in interpretations:

        house = getattr(
            interpretation,
            "house",
            None,
        )

        if house is None:
            continue

        try:
            house = int(
                house
            )
        except (
            TypeError,
            ValueError,
        ):
            continue

        if not 1 <= house <= 12:
            continue

        result[house] = interpretation

    return result


# ============================================================
# DIGNITY SYNTHESIS
# ============================================================

def synthesize_dignities(
    interpretations: Iterable[Any],
) -> Dict[str, Any]:
    """
    Build a planetary dignity mapping.

    The function accepts interpretation objects exposing either
    ``planet`` or ``name``.
    """

    result = {}

    for interpretation in interpretations:

        name = _text(
            getattr(
                interpretation,
                "planet",
                None,
            )
        )

        if not name:

            name = _text(
                getattr(
                    interpretation,
                    "name",
                    "",
                )
            )

        if not name:
            continue

        result[name] = interpretation

    return result


# ============================================================
# ASPECT NORMALIZATION
# ============================================================

def _flatten_aspect_interpretations(
    interpretations: Any,
) -> List[Any]:
    """
    Normalize aspect input into a flat sequence.

    ``analyze_aspects()`` returns:

        {
            planet: {
                target_house: AspectInterpretation
            }
        }

    The synthesis layer also accepts a flat iterable of
    AspectInterpretation objects for compatibility with callers
    that already flattened the results.
    """

    if interpretations is None:
        return []

    if isinstance(
        interpretations,
        dict,
    ):

        flattened = []

        for value in interpretations.values():

            if isinstance(
                value,
                dict,
            ):

                flattened.extend(
                    value.values()
                )

            else:

                flattened.append(
                    value
                )

        return flattened

    return list(
        interpretations
    )


# ============================================================
# ASPECT SYNTHESIS
# ============================================================

def synthesize_aspects(
    interpretations: Any,
) -> Dict[str, Dict[int, Any]]:
    """
    Build an aspect mapping indexed by planet and target house.

    Accepted input forms:

        1. Flat iterable of AspectInterpretation objects.

        2. Nested mapping returned directly by
           ``analyze_aspects()``:

            {
                "Mars": {
                    4: AspectInterpretation(...),
                    7: AspectInterpretation(...),
                    8: AspectInterpretation(...),
                }
            }

    Aspect interpretation objects are expected to expose:

        planet
        target_house
    """

    result = {}

    for interpretation in _flatten_aspect_interpretations(
        interpretations
    ):

        planet = _text(
            getattr(
                interpretation,
                "planet",
                "",
            )
        )

        target_house = getattr(
            interpretation,
            "target_house",
            None,
        )

        if not planet:
            continue

        if target_house is None:
            continue

        try:
            target_house = int(
                target_house
            )
        except (
            TypeError,
            ValueError,
        ):
            continue

        if not 1 <= target_house <= 12:
            continue

        result.setdefault(
            planet,
            {}
        )[target_house] = interpretation

    return result


# ============================================================
# YOGA SYNTHESIS
# ============================================================

def synthesize_yogas(
    interpretations: Iterable[Any],
) -> List[Any]:
    """
    Preserve Yoga interpretations in their existing order.

    Yoga detection remains the responsibility of yoga_analysis.py.
    """

    if interpretations is None:
        return []

    return list(
        interpretations
    )


# ============================================================
# COMPLETE SYNTHESIS
# ============================================================

def synthesize_chart(
    *,
    planetary: Optional[
        Iterable[Any]
    ] = None,
    houses: Optional[
        Iterable[Any]
    ] = None,
    dignities: Optional[
        Iterable[Any]
    ] = None,
    aspects: Optional[
        Iterable[Any]
    ] = None,
    yogas: Optional[
        Iterable[Any]
    ] = None,
    metadata: Optional[
        Dict[str, Any]
    ] = None,
) -> ChartInterpretation:
    """
    Combine existing interpretation results into one chart-level
    interpretation.

    No calculation or Yoga detection occurs here.

    Parameters
    ----------
    planetary:
        PlanetInterpretation objects.

    houses:
        HouseInterpretation objects.

    dignities:
        DignityInterpretation objects.

    aspects:
        AspectInterpretation objects, either as a flat iterable
        or as the nested mapping returned by analyze_aspects().

    yogas:
        YogaInterpretation objects.

    metadata:
        Optional caller-supplied metadata.
    """

    planetary_list = list(
        planetary
        if planetary is not None
        else []
    )

    house_list = list(
        houses
        if houses is not None
        else []
    )

    dignity_list = list(
        dignities
        if dignities is not None
        else []
    )

    normalized_aspects = _flatten_aspect_interpretations(
        aspects
    )

    yoga_list = list(
        yogas
        if yogas is not None
        else []
    )

    all_interpretations = (
        planetary_list
        + house_list
        + dignity_list
        + normalized_aspects
        + yoga_list
    )

    themes = collect_themes(
        all_interpretations
    )

    evidence = collect_evidence(
        all_interpretations
    )

    cautions = collect_cautions(
        all_interpretations
    )

    return ChartInterpretation(
        planetary=synthesize_planets(
            planetary_list
        ),

        houses=synthesize_houses(
            house_list
        ),

        dignities=synthesize_dignities(
            dignity_list
        ),

        aspects=synthesize_aspects(
            normalized_aspects
        ),

        yogas=synthesize_yogas(
            yoga_list
        ),

        themes=themes,

        evidence=evidence,

        cautions=cautions,

        metadata=dict(
            metadata
            if metadata is not None
            else {}
        ),
    )


# ============================================================
# DETECTED YOGA ACCESSOR
# ============================================================

def detected_yogas(
    synthesis: ChartInterpretation,
) -> List[Any]:
    """
    Return only structurally detected Yoga interpretations.
    """

    if synthesis is None:
        raise ValueError(
            "synthesis must not be None."
        )

    return [
        yoga
        for yoga in synthesis.yogas
        if bool(
            getattr(
                yoga,
                "detected",
                False,
            )
        )
    ]


# ============================================================
# REPORT
# ============================================================

def synthesis_report(
    synthesis: ChartInterpretation,
) -> List[str]:
    """
    Produce a concise chart-level evidence report.

    This report intentionally avoids deterministic prediction.
    """

    if synthesis is None:
        raise ValueError(
            "synthesis must not be None."
        )

    report = []

    report.append(
        f"Planetary interpretations: "
        f"{synthesis.planet_count}."
    )

    report.append(
        f"House interpretations: "
        f"{synthesis.house_count}."
    )

    report.append(
        f"Dignity interpretations: "
        f"{synthesis.dignity_count}."
    )

    report.append(
        f"Planetary aspects: "
        f"{synthesis.aspect_count}."
    )

    report.append(
        f"Structurally detected Yogas: "
        f"{synthesis.detected_yoga_count}."
    )

    if synthesis.themes:

        report.append(
            "Themes: "
            + ", ".join(
                synthesis.themes
            )
            + "."
        )

    return report


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "ChartInterpretation",
    "collect_themes",
    "collect_evidence",
    "collect_cautions",
    "synthesize_planets",
    "synthesize_houses",
    "synthesize_dignities",
    "synthesize_aspects",
    "synthesize_yogas",
    "synthesize_chart",
    "detected_yogas",
    "synthesis_report",
]