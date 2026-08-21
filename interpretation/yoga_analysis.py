"""
interpretation/yoga_analysis.py

Parashari Yoga interpretation layer.

This module consumes structural YogaResult objects produced by the
yogas package and converts them into immutable interpretation-layer
objects.

It does NOT detect or calculate Yogas.

Responsibilities:
    - preserve structural Yoga detection results
    - classify interpretive status
    - attach general themes
    - attach interpretive cautions
    - preserve evidence
    - preserve involved planets and houses
    - provide filtering and reporting helpers

The structural Yoga detection remains the responsibility of the
yogas package.

Compatible with Python 3.9.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence

from yogas.base import YogaResult


# ============================================================
# YOGA THEMES
# ============================================================

YOGA_THEMES: Dict[str, List[str]] = {
    "Raja Yoga": [
        "leadership, authority and constructive life advancement",
        "integration of supportive kendra and trikona principles",
        "potential for recognition when the formation is sufficiently supported",
    ],

    "Dhana Yoga": [
        "wealth-building and financial resource development",
        "connection between wealth-producing houses and their lords",
        "capacity for material accumulation when supported by planetary strength",
    ],

    "Gaja Kesari Yoga": [
        "intelligence, judgment and social respect",
        "supportive relationship between Jupiter and the Moon",
        "potential for learning, counsel and constructive reputation",
    ],

    "Budha-Aditya Yoga": [
        "intellectual ability and communication",
        "analytical thinking and practical expression",
        "integration of solar authority with Mercurial intelligence",
    ],

    "Chandra-Mangala Yoga": [
        "initiative connected with emotional and material drives",
        "enterprise, resource management and practical action",
        "potential for financial activity when otherwise supported",
    ],

    "Neecha Bhanga Raja Yoga": [
        "structural cancellation of a planetary debilitation",
        "potential recovery or constructive development in areas represented by the involved planet",
        "transformation of weakness into a more productive expression when supporting factors are present",
    ],
}


# ============================================================
# YOGA CAUTIONS
# ============================================================

YOGA_CAUTIONS: Dict[str, List[str]] = {
    "Raja Yoga": [
        "Structural formation alone does not guarantee status, success or authority.",
        "Planetary strength, dignity, timing and supporting factors must be evaluated separately.",
    ],

    "Dhana Yoga": [
        "A structural wealth combination does not guarantee a specific amount of money.",
        "Financial outcomes require assessment of planetary strength, timing and supporting combinations.",
    ],

    "Gaja Kesari Yoga": [
        "The classical combination should not be interpreted as an automatic guarantee of fame or prosperity.",
        "Condition, dignity, affliction and timing materially affect its expression.",
    ],

    "Budha-Aditya Yoga": [
        "The conjunction alone does not guarantee exceptional intelligence or career success.",
        "Combustion, dignity, house placement and other influences require separate evaluation.",
    ],

    "Chandra-Mangala Yoga": [
        "The combination does not by itself guarantee financial success.",
        "Emotional volatility, affliction and planetary strength may significantly modify its expression.",
    ],

    "Neecha Bhanga Raja Yoga": [
        "Cancellation of debilitation is a structural condition and should not automatically be treated as a Raja Yoga outcome.",
        "The actual strength and dignity of the planet must be evaluated separately.",
    ],
}


# ============================================================
# FALLBACK INTERPRETATION
# ============================================================

FALLBACK_THEMES = [
    "interpretation depends on the specific Yoga formation",
]

FALLBACK_CAUTIONS = [
    "Structural Yoga formation should not be treated as a guaranteed prediction.",
]


# ============================================================
# DATA MODEL
# ============================================================

@dataclass(frozen=True)
class YogaInterpretation:
    """
    Immutable interpretation-layer representation of one Yoga.

    The object preserves the structural result while adding
    interpretive context. It does not modify or replace YogaResult.
    """

    name: str
    category: str
    detected: bool

    description: Optional[str]

    strength: Optional[str]

    involved_planets: List[str]
    involved_houses: List[int]

    conditions_met: List[str]
    conditions_failed: List[str]

    metadata: Dict[str, Any]

    evidence: List[str]

    themes: List[str]
    cautions: List[str]

    interpretive_status: str

    @property
    def is_present(self) -> bool:
        """
        Return whether the Yoga is structurally present.
        """

        return self.detected

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the interpretation into a detached dictionary.

        Mutable fields are copied so callers cannot mutate the
        internal state of this immutable dataclass.
        """

        return {
            "name": self.name,
            "category": self.category,
            "detected": self.detected,
            "description": self.description,
            "strength": self.strength,
            "involved_planets": list(
                self.involved_planets
            ),
            "involved_houses": list(
                self.involved_houses
            ),
            "conditions_met": list(
                self.conditions_met
            ),
            "conditions_failed": list(
                self.conditions_failed
            ),
            "metadata": dict(
                self.metadata
            ),
            "evidence": list(
                self.evidence
            ),
            "themes": list(
                self.themes
            ),
            "cautions": list(
                self.cautions
            ),
            "interpretive_status": (
                self.interpretive_status
            ),
            "is_present": self.is_present,
        }


# ============================================================
# VALIDATION
# ============================================================

def _validate_yoga_result(
    result: Any,
) -> YogaResult:
    """
    Validate that the supplied object is a YogaResult.

    The interpretation layer must not silently accept arbitrary
    objects because doing so can conceal structural analysis
    errors.
    """

    if not isinstance(
        result,
        YogaResult,
    ):
        raise TypeError(
            "result must be a YogaResult."
        )

    return result


def _normalize_text(
    value: Any,
) -> Optional[str]:
    """
    Normalize optional textual values.
    """

    if value is None:
        return None

    return str(value)


def _normalize_string_list(
    values: Any,
) -> List[str]:
    """
    Normalize an optional iterable of values into strings.
    """

    if values is None:
        return []

    if isinstance(
        values,
        str,
    ):
        return [values]

    try:
        return [
            str(value)
            for value in values
        ]

    except TypeError:
        return [str(values)]


def _normalize_house_list(
    values: Any,
) -> List[int]:
    """
    Normalize an optional iterable of house numbers.
    """

    if values is None:
        return []

    if isinstance(
        values,
        int,
    ):
        return [values]

    try:
        return [
            int(value)
            for value in values
        ]

    except TypeError:
        return [int(values)]


# ============================================================
# THEME / CAUTION RESOLUTION
# ============================================================

def _copy_mapping_values(
    mapping: Dict[str, List[str]],
    key: str,
) -> List[str]:
    """
    Return a detached copy of a mapped list.
    """

    values = mapping.get(
        key
    )

    if values is None:
        return []

    return list(values)


def _resolve_themes(
    result: YogaResult,
) -> List[str]:
    """
    Resolve interpretive themes.

    Priority:

        1. Exact Yoga name
        2. Yoga category
        3. Generic fallback
    """

    themes = _copy_mapping_values(
        YOGA_THEMES,
        result.name,
    )

    if themes:
        return themes

    themes = _copy_mapping_values(
        YOGA_THEMES,
        result.category,
    )

    if themes:
        return themes

    return list(
        FALLBACK_THEMES
    )


def _resolve_cautions(
    result: YogaResult,
) -> List[str]:
    """
    Resolve interpretive cautions.

    Priority:

        1. Exact Yoga name
        2. Yoga category
        3. Generic fallback
    """

    cautions = _copy_mapping_values(
        YOGA_CAUTIONS,
        result.name,
    )

    if cautions:
        return cautions

    cautions = _copy_mapping_values(
        YOGA_CAUTIONS,
        result.category,
    )

    if cautions:
        return cautions

    return list(
        FALLBACK_CAUTIONS
    )


# ============================================================
# EVIDENCE
# ============================================================

def _interpretive_evidence(
    result: YogaResult,
) -> List[str]:
    """
    Preserve structural evidence and add a concise interpretation
    status statement.

    Existing evidence is never discarded.
    """

    evidence = _normalize_string_list(
        getattr(
            result,
            "evidence",
            [],
        )
    )

    if result.detected:
        evidence.append(
            "Yoga is structurally present according to the evaluated rule."
        )
    else:
        evidence.append(
            "Yoga is not structurally detected according to the evaluated rule."
        )

    return evidence


# ============================================================
# SINGLE YOGA INTERPRETATION
# ============================================================

def interpret_yoga(
    result: YogaResult,
) -> YogaInterpretation:
    """
    Convert one structural YogaResult into a YogaInterpretation.

    No Yoga detection occurs here.

    The supplied YogaResult is preserved as the source of truth for:
        - name
        - category
        - detection state
        - strength
        - description
        - evidence
        - involved planets
        - involved houses
        - conditions
        - metadata
    """

    result = _validate_yoga_result(
        result
    )

    detected = bool(
        result.detected
    )

    interpretive_status = (
        "structurally_present"
        if detected
        else "not_detected"
    )

    return YogaInterpretation(
        name=str(
            result.name
        ),

        category=str(
            result.category
        ),

        detected=detected,

        description=_normalize_text(
            getattr(
                result,
                "description",
                None,
            )
        ),

        strength=_normalize_text(
            getattr(
                result,
                "strength",
                None,
            )
        ),

        involved_planets=_normalize_string_list(
            getattr(
                result,
                "involved_planets",
                [],
            )
        ),

        involved_houses=_normalize_house_list(
            getattr(
                result,
                "involved_houses",
                [],
            )
        ),

        conditions_met=_normalize_string_list(
            getattr(
                result,
                "conditions_met",
                [],
            )
        ),

        conditions_failed=_normalize_string_list(
            getattr(
                result,
                "conditions_failed",
                [],
            )
        ),

        metadata=dict(
            getattr(
                result,
                "metadata",
                {},
            )
            or {}
        ),

        evidence=_interpretive_evidence(
            result
        ),

        themes=_resolve_themes(
            result
        ),

        cautions=_resolve_cautions(
            result
        ),

        interpretive_status=(
            interpretive_status
        ),
    )


# ============================================================
# COLLECTION INTERPRETATION
# ============================================================

def interpret_yoga_results(
    results: Iterable[YogaResult],
) -> List[YogaInterpretation]:
    """
    Interpret a collection of YogaResult objects.

    Order is preserved.

    Non-detected YogaResult objects are intentionally preserved.
    """

    if results is None:
        raise ValueError(
            "results must not be None."
        )

    return [
        interpret_yoga(
            result
        )
        for result in results
    ]


# ============================================================
# CHART YOGA ANALYSIS
# ============================================================

def analyze_yoga_interpretations(
    context: Any,
    rules: Optional[
        Sequence[Any]
    ] = None,
    detected_only: bool = False,
) -> List[YogaInterpretation]:
    """
    Evaluate supplied Yoga rules and interpret their results.

    Parameters
    ----------
    context:
        Interpretation/calculation context passed unchanged to
        each YogaRule.

    rules:
        Sequence of YogaRule instances.

        If omitted, no implicit Yoga rules are created. This keeps
        the interpretation layer independent from the project's
        structural Yoga registry.

    detected_only:
        If True, return only structurally detected Yogas.

    Returns
    -------
    list[YogaInterpretation]
    """

    if rules is None:
        return []

    interpretations = []

    for rule in rules:

        if not hasattr(
            rule,
            "evaluate",
        ):
            raise TypeError(
                "Each Yoga rule must expose an evaluate() method."
            )

        result = rule.evaluate(
            context
        )

        interpretation = interpret_yoga(
            result
        )

        if (
            detected_only
            and not interpretation.detected
        ):
            continue

        interpretations.append(
            interpretation
        )

    return interpretations


# ============================================================
# DETECTED YOGA ACCESSOR
# ============================================================

def detected_yoga_interpretations(
    context: Any,
    rules: Optional[
        Sequence[Any]
    ] = None,
) -> List[YogaInterpretation]:
    """
    Return only structurally detected Yoga interpretations.
    """

    return analyze_yoga_interpretations(
        context,
        rules,
        detected_only=True,
    )


# ============================================================
# CATEGORY FILTER
# ============================================================

def yoga_interpretations_by_category(
    interpretations: Iterable[
        YogaInterpretation
    ],
    category: str,
) -> List[YogaInterpretation]:
    """
    Return interpretations belonging to a category.

    Category comparison is case-insensitive.
    """

    if category is None:
        raise ValueError(
            "category must not be None."
        )

    normalized_category = str(
        category
    ).strip().lower()

    return [
        interpretation
        for interpretation in interpretations
        if interpretation.category.strip().lower()
        == normalized_category
    ]


# ============================================================
# PLANET FILTER
# ============================================================

def yoga_interpretations_involving_planet(
    interpretations: Iterable[
        YogaInterpretation
    ],
    planet: str,
) -> List[YogaInterpretation]:
    """
    Return interpretations involving a specified planet.

    Planet comparison is case-insensitive.
    """

    if planet is None:
        raise ValueError(
            "planet must not be None."
        )

    normalized_planet = str(
        planet
    ).strip().lower()

    return [
        interpretation
        for interpretation in interpretations
        if any(
            str(involved).strip().lower()
            == normalized_planet
            for involved
            in interpretation.involved_planets
        )
    ]


# ============================================================
# HOUSE FILTER
# ============================================================

def yoga_interpretations_involving_house(
    interpretations: Iterable[
        YogaInterpretation
    ],
    house: int,
) -> List[YogaInterpretation]:
    """
    Return interpretations involving a specified house.
    """

    if not isinstance(
        house,
        int,
    ):
        raise ValueError(
            "house must be an integer between 1 and 12."
        )

    if not 1 <= house <= 12:
        raise ValueError(
            "house must be between 1 and 12."
        )

    return [
        interpretation
        for interpretation in interpretations
        if house in interpretation.involved_houses
    ]


# ============================================================
# REPORT
# ============================================================

def _format_optional(
    value: Optional[Any],
) -> str:
    """
    Format an optional report value.
    """

    if value is None:
        return "none"

    return str(value)


def yoga_analysis_report(
    context: Any,
    rules: Optional[
        Sequence[Any]
    ] = None,
    detected_only: bool = True,
) -> List[str]:
    """
    Produce a concise textual Yoga analysis report.

    By default only detected Yogas are included.
    """

    interpretations = analyze_yoga_interpretations(
        context,
        rules,
        detected_only=detected_only,
    )

    report = []

    for interpretation in interpretations:

        status = (
            "detected"
            if interpretation.detected
            else "not detected"
        )

        planets = (
            ", ".join(
                interpretation.involved_planets
            )
            if interpretation.involved_planets
            else "none"
        )

        houses = (
            ", ".join(
                str(house)
                for house
                in interpretation.involved_houses
            )
            if interpretation.involved_houses
            else "none"
        )

        report.append(
            f"{interpretation.name}: "
            f"{status}; "
            f"category={interpretation.category}; "
            f"planets={planets}; "
            f"houses={houses}; "
            f"strength={_format_optional(interpretation.strength)}."
        )

    return report


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "YOGA_THEMES",
    "YOGA_CAUTIONS",
    "YogaInterpretation",
    "interpret_yoga",
    "interpret_yoga_results",
    "analyze_yoga_interpretations",
    "detected_yoga_interpretations",
    "yoga_interpretations_by_category",
    "yoga_interpretations_involving_planet",
    "yoga_interpretations_involving_house",
    "yoga_analysis_report",
]