"""
Yoga analysis orchestration.

The analyzer executes registered Yoga rules and returns structured
results. Individual classical Yoga definitions belong in separate
modules.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from .base import (
    YogaResult,
    YogaRule,
)


class YogaAnalyzer:
    """
    Execute a collection of Yoga rules.
    """

    def __init__(
        self,
        rules: Optional[
            Iterable[YogaRule]
        ] = None,
    ) -> None:

        self.rules = list(
            rules or []
        )

    def add_rule(
        self,
        rule: YogaRule,
    ) -> None:
        """Register one Yoga rule."""

        if not isinstance(
            rule,
            YogaRule,
        ):
            raise TypeError(
                "rule must be an instance "
                "of YogaRule."
            )

        self.rules.append(rule)

    def evaluate(
        self,
        context: Any,
        *,
        detected_only: bool = False,
    ) -> List[YogaResult]:
        """
        Evaluate every registered Yoga rule.

        Parameters
        ----------
        context:
            InterpretationContext.

        detected_only:
            If True, return only detected Yogas.
        """

        results = []

        for rule in self.rules:

            result = rule.evaluate(
                context
            )

            if not isinstance(
                result,
                YogaResult,
            ):
                raise TypeError(
                    f"{rule.__class__.__name__}.evaluate() "
                    "must return YogaResult."
                )

            if (
                detected_only
                and not result.detected
            ):
                continue

            results.append(result)

        return results

    def detected(
        self,
        context: Any,
    ) -> List[YogaResult]:
        """Return only detected Yogas."""

        return self.evaluate(
            context,
            detected_only=True,
        )


def analyze_yogas(
    context: Any,
    rules: Optional[
        Iterable[YogaRule]
    ] = None,
) -> List[YogaResult]:
    """
    Convenience function for evaluating Yoga rules.
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
    Convenience function returning detected Yogas only.
    """

    analyzer = YogaAnalyzer(
        rules
    )

    return analyzer.detected(
        context
    )