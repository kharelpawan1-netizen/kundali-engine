"""
yogas/analyzer.py

Central analyzer for the structural Vedic Yoga engine.

This module evaluates configured YogaRule objects and returns
structured YogaResult objects.

Architecture:

    InterpretationContext
            ↓
        YogaRule
            ↓
        YogaResult
            ↓
        YogaAnalyzer
            ↓
    Yoga interpretation layer

This module does NOT:
    - calculate planetary positions
    - calculate houses
    - calculate Vargas
    - calculate Dashas
    - perform independent Yoga detection
    - interpret the final life results of a Yoga

Each YogaRule remains responsible for its own structural
formation logic.

Compatible with Python 3.9.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from .base import YogaResult, YogaRule


# ============================================================
# YOGA ANALYZER
# ============================================================

class YogaAnalyzer:
    """
    Central structural Yoga analyzer.

    The analyzer stores a configured collection of YogaRule
    instances and evaluates them against an interpretation
    context.

    The analyzer itself contains no Yoga-specific formation
    logic.
    """

    def __init__(
        self,
        rules: Optional[
            Iterable[YogaRule]
        ] = None,
    ) -> None:
        """
        Initialize the analyzer.

        Parameters
        ----------
        rules:
            Optional iterable of YogaRule instances.
        """

        self.rules: List[YogaRule] = []

        if rules is not None:

            for rule in rules:

                self.add_rule(
                    rule
                )

    # ========================================================
    # RULE MANAGEMENT
    # ========================================================

    def add_rule(
        self,
        rule: YogaRule,
    ) -> None:
        """
        Add one YogaRule to the analyzer.

        Raises
        ------
        TypeError
            If the supplied object is not a YogaRule.
        """

        if not isinstance(
            rule,
            YogaRule,
        ):
            raise TypeError(
                "rule must be an instance of YogaRule."
            )

        self.rules.append(
            rule
        )

    # ========================================================
    # EVALUATION
    # ========================================================

    def evaluate(
        self,
        context: Any,
        *,
        detected_only: bool = False,
    ) -> List[YogaResult]:
        """
        Evaluate every configured YogaRule.

        Parameters
        ----------
        context:
            InterpretationContext or compatible context object.

        detected_only:
            If True, return only structurally detected Yogas.

        Returns
        -------
        List[YogaResult]
            Structured results from every configured rule.
        """

        results: List[YogaResult] = []

        for rule in self.rules:

            result = rule.evaluate(
                context
            )

            if not isinstance(
                result,
                YogaResult,
            ):
                raise TypeError(
                    f"Yoga rule '{rule.name}' "
                    "must return YogaResult."
                )

            if (
                detected_only
                and not result.detected
            ):
                continue

            results.append(
                result
            )

        return results

    # ========================================================
    # DETECTED YOGAS
    # ========================================================

    def detected(
        self,
        context: Any,
    ) -> List[YogaResult]:
        """
        Evaluate all rules and return detected Yogas only.
        """

        return self.evaluate(
            context,
            detected_only=True,
        )


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def analyze_yogas(
    context: Any,
    rules: Optional[
        Iterable[YogaRule]
    ] = None,
) -> List[YogaResult]:
    """
    Evaluate the configured Yoga rules.

    Parameters
    ----------
    context:
        InterpretationContext.

    rules:
        Optional iterable of YogaRule instances.

    Returns
    -------
    List[YogaResult]
        Results for all configured Yoga rules.

    Important
    ---------
    No implicit Yoga rules are created when ``rules`` is None.

    This preserves explicit configuration of the Yoga engine.
    """

    analyzer = YogaAnalyzer(
        rules
    )

    return analyzer.evaluate(
        context
    )


def detected_yogas(
    context: Any,
    rules: Optional[
        Iterable[YogaRule]
    ] = None,
) -> List[YogaResult]:
    """
    Evaluate the configured Yoga rules and return only
    structurally detected Yogas.
    """

    analyzer = YogaAnalyzer(
        rules
    )

    return analyzer.detected(
        context
    )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "YogaAnalyzer",
    "analyze_yogas",
    "detected_yogas",
]