"""
Core data structures and contracts for the Vedic Yoga engine.

This module contains no specific Yoga rules.
It defines the common representation that every future Yoga detector
will use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class YogaResult:
    """
    Structured result for one Yoga evaluation.

    A Yoga detector should never merely return True/False.
    The engine needs enough evidence to explain why a Yoga was detected.
    """

    name: str
    detected: bool

    category: str = "general"

    strength: Optional[str] = None

    description: str = ""

    evidence: List[str] = field(
        default_factory=list
    )

    involved_planets: List[str] = field(
        default_factory=list
    )

    involved_houses: List[int] = field(
        default_factory=list
    )

    conditions_met: List[str] = field(
        default_factory=list
    )

    conditions_failed: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def is_present(self) -> bool:
        """Human-readable alias for detected."""

        return self.detected

    def to_dict(self) -> Dict[str, Any]:
        """Convert the result into a serializable dictionary."""

        return {
            "name": self.name,
            "detected": self.detected,
            "category": self.category,
            "strength": self.strength,
            "description": self.description,
            "evidence": list(self.evidence),
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
            "metadata": dict(self.metadata),
        }


class YogaRule:
    """
    Base contract for future Yoga detectors.

    Individual rules such as Gaja Kesari, Budha-Aditya,
    Raja Yoga, Dhana Yoga, etc. will implement this contract.
    """

    name: str = "Unnamed Yoga"
    category: str = "general"

    def evaluate(
        self,
        context: Any,
    ) -> YogaResult:
        """
        Evaluate the Yoga against an interpretation context.

        Subclasses must override this method.
        """

        raise NotImplementedError(
            "YogaRule subclasses must implement evaluate()."
        )