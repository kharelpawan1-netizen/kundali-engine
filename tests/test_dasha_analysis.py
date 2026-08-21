"""
tests/test_dasha_analysis.py

Tests for interpretation/dasha_analysis.py.

These tests verify that the Dasha interpretation layer:

    - consumes already-calculated Dasha periods
    - produces conservative interpretive structures
    - preserves hierarchy correctly
    - extracts themes, evidence, and cautions
    - integrates with DashaContext-style objects
    - does not perform Dasha calculations
    - remains compatible with Python 3.9
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest

from interpretation.dasha_analysis import (
    DASHA_CAUTIONS,
    DASHA_THEMES,
    DashaHierarchyInterpretation,
    DashaInterpretation,
    active_dasha_lords,
    collect_dasha_cautions,
    collect_dasha_evidence,
    collect_dasha_themes,
    dasha_analysis_report,
    dasha_cautions,
    dasha_interpretations_involving_planet,
    dasha_themes,
    interpret_current_dasha,
    interpret_dasha,
    interpret_dasha_hierarchy,
    interpret_dasha_periods,
)


# ============================================================
# TEST FIXTURES
# ============================================================


@dataclass
class MockMahadasha:
    """Minimal calculation-layer Mahadasha substitute."""

    planet: str
    start: datetime
    end: datetime
    duration_years: float


@dataclass
class MockAntardasha:
    """Minimal calculation-layer Antardasha substitute."""

    mahadasha_lord: str
    antardasha_lord: str
    start: datetime
    end: datetime

    @property
    def planet(self):
        return self.antardasha_lord


@dataclass
class MockNamedPlanet:
    """Object exposing a name attribute."""

    name: str


@dataclass
class MockPlanetAttribute:
    """Object exposing a planet attribute."""

    planet: str


@dataclass
class MockDashaContext:
    """Minimal normalized Dasha context."""

    mahadasha: object = None
    antardasha: object = None
    pratyantardasha: object = None
    sookshma: object = None
    prana: object = None
    deha: object = None
    moment: datetime = None


@dataclass
class MockInterpretationContext:
    """Minimal InterpretationContext-style object."""

    dasha: object = None
    current_moment: datetime = None


@pytest.fixture
def birth_datetime():
    """Provide a timezone-naive test birth datetime."""

    return datetime(
        2000,
        1,
        1,
        12,
        0,
        0,
    )


@pytest.fixture
def mahadasha(birth_datetime):
    """Provide a simple mock Mahadasha."""

    return MockMahadasha(
        planet="Jupiter",
        start=birth_datetime,
        end=birth_datetime + timedelta(
            days=365.25 * 16
        ),
        duration_years=16.0,
    )


@pytest.fixture
def antardasha(birth_datetime):
    """Provide a simple mock Antardasha."""

    return MockAntardasha(
        mahadasha_lord="Jupiter",
        antardasha_lord="Saturn",
        start=birth_datetime,
        end=birth_datetime + timedelta(
            days=365.25 * 2.533333
        ),
    )


# ============================================================
# DATA MODEL TESTS
# ============================================================


def test_dasha_interpretation_defaults():
    """DashaInterpretation should initialize optional fields safely."""

    interpretation = DashaInterpretation(
        planet="Jupiter",
        level="mahadasha",
    )

    assert interpretation.planet == "Jupiter"
    assert interpretation.level == "mahadasha"
    assert interpretation.start is None
    assert interpretation.end is None
    assert interpretation.duration_years is None
    assert interpretation.parent_lord is None
    assert interpretation.themes == []
    assert interpretation.evidence == []
    assert interpretation.cautions == []
    assert interpretation.metadata == {}


def test_dasha_interpretation_duration_days():
    """Duration days should be calculated from start and end."""

    start = datetime(
        2020,
        1,
        1,
    )

    end = start + timedelta(
        days=10
    )

    interpretation = DashaInterpretation(
        planet="Sun",
        level="mahadasha",
        start=start,
        end=end,
    )

    assert interpretation.duration_days == 10.0


def test_dasha_interpretation_duration_days_without_dates():
    """Duration days should be None when dates are unavailable."""

    interpretation = DashaInterpretation(
        planet="Sun",
        level="mahadasha",
    )

    assert interpretation.duration_days is None


def test_dasha_interpretation_to_dict(mahadasha):
    """DashaInterpretation should serialize correctly."""

    interpretation = interpret_dasha(
        mahadasha
    )

    result = interpretation.to_dict()

    assert result["planet"] == "Jupiter"
    assert result["level"] == "mahadasha"
    assert result["start"] == mahadasha.start
    assert result["end"] == mahadasha.end
    assert result["duration_years"] == 16.0
    assert "themes" in result
    assert "evidence" in result
    assert "cautions" in result
    assert "metadata" in result


def test_hierarchy_defaults():
    """DashaHierarchyInterpretation should allow empty hierarchy."""

    hierarchy = DashaHierarchyInterpretation()

    assert hierarchy.mahadasha is None
    assert hierarchy.antardasha is None
    assert hierarchy.pratyantardasha is None
    assert hierarchy.sookshma is None
    assert hierarchy.prana is None
    assert hierarchy.deha is None
    assert hierarchy.moment is None
    assert hierarchy.themes == []
    assert hierarchy.evidence == []
    assert hierarchy.cautions == []


def test_hierarchy_to_dict():
    """Hierarchy serialization should include all hierarchy levels."""

    hierarchy = DashaHierarchyInterpretation(
        moment=datetime(
            2025,
            1,
            1,
        ),
    )

    result = hierarchy.to_dict()

    assert result["mahadasha"] is None
    assert result["antardasha"] is None
    assert result["pratyantardasha"] is None
    assert result["sookshma"] is None
    assert result["prana"] is None
    assert result["deha"] is None
    assert result["moment"] == datetime(
        2025,
        1,
        1,
    )


# ============================================================
# THEME TESTS
# ============================================================


@pytest.mark.parametrize(
    "planet",
    [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ],
)
def test_dasha_themes_known_planets(planet):
    """Every classical Vimshottari lord should have themes."""

    themes = dasha_themes(
        planet
    )

    assert themes
    assert themes == DASHA_THEMES[planet]


def test_dasha_themes_case_insensitive():
    """Planet matching should be case-insensitive."""

    assert dasha_themes(
        "jUpItEr"
    ) == DASHA_THEMES["Jupiter"]


def test_dasha_themes_unknown_planet():
    """Unknown planets should receive conservative fallback themes."""

    themes = dasha_themes(
        "UnknownPlanet"
    )

    assert len(themes) == 1
    assert "complete chart context" in themes[0]


def test_dasha_themes_empty_planet():
    """Empty planet names should return no themes."""

    assert dasha_themes("") == []


def test_dasha_themes_none():
    """None should return no themes."""

    assert dasha_themes(None) == []


@pytest.mark.parametrize(
    "planet",
    [
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    ],
)
def test_dasha_cautions_known_planets(planet):
    """Every classical lord should have conservative cautions."""

    cautions = dasha_cautions(
        planet
    )

    assert cautions
    assert cautions == DASHA_CAUTIONS[planet]


def test_dasha_cautions_case_insensitive():
    """Caution lookup should be case-insensitive."""

    assert dasha_cautions(
        "SATURN"
    ) == DASHA_CAUTIONS["Saturn"]


def test_dasha_cautions_unknown_planet():
    """Unknown planets should receive a generic caution."""

    cautions = dasha_cautions(
        "UnknownPlanet"
    )

    assert len(cautions) == 1
    assert "deterministic prediction" in cautions[0]


def test_dasha_cautions_empty_planet():
    """Empty planet names should return no cautions."""

    assert dasha_cautions("") == []


# ============================================================
# PLANET NORMALIZATION TESTS
# ============================================================


def test_interpret_dasha_accepts_planet_object(
    birth_datetime,
):
    """interpret_dasha should accept objects exposing planet."""

    period = MockPlanetAttribute(
        planet="Mars"
    )

    interpretation = interpret_dasha(
        period
    )

    assert interpretation.planet == "Mars"


def test_interpret_dasha_accepts_name_object(
    birth_datetime,
):
    """
    interpret_dasha should accept objects exposing name.

    This verifies compatibility with broader interpretation objects.
    """

    period = MockNamedPlanet(
        name="Venus"
    )

    interpretation = interpret_dasha(
        period
    )

    assert interpretation.planet == "Venus"


# ============================================================
# SINGLE DASHA INTERPRETATION TESTS
# ============================================================


def test_interpret_mahadasha(mahadasha):
    """A Mahadasha should produce a structural interpretation."""

    interpretation = interpret_dasha(
        mahadasha
    )

    assert interpretation.planet == "Jupiter"
    assert interpretation.level == "mahadasha"
    assert interpretation.start == mahadasha.start
    assert interpretation.end == mahadasha.end
    assert interpretation.duration_years == 16.0
    assert interpretation.parent_lord is None

    assert "learning" in interpretation.themes
    assert interpretation.evidence
    assert interpretation.cautions


def test_interpret_antardasha(
    antardasha,
):
    """An Antardasha should retain its Antardasha lord."""

    interpretation = interpret_dasha(
        antardasha,
        level="antardasha",
        parent_lord="Jupiter",
    )

    assert interpretation.planet == "Saturn"
    assert interpretation.level == "antardasha"
    assert interpretation.parent_lord == "Jupiter"
    assert interpretation.start == antardasha.start
    assert interpretation.end == antardasha.end


def test_interpret_dasha_level_is_normalized(
    mahadasha,
):
    """Dasha level should be normalized to lowercase."""

    interpretation = interpret_dasha(
        mahadasha,
        level="  MAHADASHA  ",
    )

    assert interpretation.level == "mahadasha"


def test_interpret_dasha_requires_period():
    """None period should be rejected."""

    with pytest.raises(
        ValueError,
        match="period must not be None",
    ):
        interpret_dasha(
            None
        )


def test_interpret_dasha_requires_planet():
    """A period without a usable lord should be rejected."""

    class InvalidPeriod:
        pass

    with pytest.raises(
        ValueError,
        match="must expose a planet or lord",
    ):
        interpret_dasha(
            InvalidPeriod()
        )


def test_interpret_dasha_requires_level(
    mahadasha,
):
    """Empty interpretation levels should be rejected."""

    with pytest.raises(
        ValueError,
        match="level must not be empty",
    ):
        interpret_dasha(
            mahadasha,
            level="",
        )


def test_interpret_dasha_extracts_duration(
    mahadasha,
):
    """Calculated duration should be preserved."""

    interpretation = interpret_dasha(
        mahadasha
    )

    assert interpretation.duration_years == 16.0


def test_interpret_dasha_handles_invalid_duration():
    """Invalid duration values should safely become None."""

    class InvalidDurationPeriod:
        planet = "Saturn"
        duration_years = "not-a-number"

    interpretation = interpret_dasha(
        InvalidDurationPeriod()
    )

    assert interpretation.duration_years is None


def test_interpret_dasha_evidence_contains_lord(
    mahadasha,
):
    """Evidence should identify the Dasha lord."""

    interpretation = interpret_dasha(
        mahadasha
    )

    assert any(
        "Jupiter" in item
        for item in interpretation.evidence
    )


def test_interpret_dasha_evidence_contains_dates(
    mahadasha,
):
    """Evidence should contain period dates when available."""

    interpretation = interpret_dasha(
        mahadasha
    )

    assert any(
        mahadasha.start.isoformat() in item
        for item in interpretation.evidence
    )

    assert any(
        mahadasha.end.isoformat() in item
        for item in interpretation.evidence
    )


def test_interpret_dasha_evidence_contains_duration(
    mahadasha,
):
    """Evidence should include the calculated duration."""

    interpretation = interpret_dasha(
        mahadasha
    )

    assert any(
        "16.000000" in item
        for item in interpretation.evidence
    )


def test_interpret_dasha_parent_lord_evidence(
    mahadasha,
):
    """Parent-lord relationships should be recorded as evidence."""

    interpretation = interpret_dasha(
        mahadasha,
        level="antardasha",
        parent_lord="Saturn",
    )

    assert interpretation.parent_lord == "Saturn"

    assert any(
        "Saturn" in item
        for item in interpretation.evidence
    )


# ============================================================
# PERIOD COLLECTION TESTS
# ============================================================


def test_interpret_dasha_periods(
    mahadasha,
    antardasha,
):
    """Multiple periods should preserve their original order."""

    interpretations = interpret_dasha_periods(
        [
            mahadasha,
            antardasha,
        ],
        level="mahadasha",
    )

    assert len(interpretations) == 2
    assert interpretations[0].planet == "Jupiter"
    assert interpretations[1].planet == "Saturn"


def test_interpret_dasha_periods_empty():
    """An empty period collection should produce an empty list."""

    assert interpret_dasha_periods(
        []
    ) == []


def test_interpret_dasha_periods_none():
    """None period collections should be rejected."""

    with pytest.raises(
        ValueError,
        match="periods must not be None",
    ):
        interpret_dasha_periods(
            None
        )


# ============================================================
# HIERARCHY TESTS
# ============================================================


def test_interpret_dasha_hierarchy_mahadasha_only(
    mahadasha,
):
    """Hierarchy should work with only Mahadasha supplied."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha
    )

    assert hierarchy.mahadasha is not None
    assert hierarchy.mahadasha.planet == "Jupiter"

    assert hierarchy.antardasha is None
    assert hierarchy.pratyantardasha is None
    assert hierarchy.sookshma is None
    assert hierarchy.prana is None
    assert hierarchy.deha is None


def test_interpret_dasha_hierarchy_two_levels(
    mahadasha,
    antardasha,
):
    """Mahadasha and Antardasha parent-child relationship should work."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    assert hierarchy.mahadasha.planet == "Jupiter"
    assert hierarchy.antardasha.planet == "Saturn"

    assert hierarchy.antardasha.parent_lord == "Jupiter"


def test_interpret_dasha_hierarchy_all_levels(
    mahadasha,
    birth_datetime,
):
    """All supported hierarchy levels should be interpreted."""

    base_start = birth_datetime

    periods = []

    planets = [
        "Saturn",
        "Mars",
        "Mercury",
        "Venus",
        "Sun",
    ]

    for index, planet in enumerate(
        planets
    ):
        start = (
            base_start
            + timedelta(
                days=index * 10
            )
        )

        end = (
            start
            + timedelta(
                days=10
            )
        )

        periods.append(
            MockMahadasha(
                planet=planet,
                start=start,
                end=end,
                duration_years=(
                    10.0 / 365.25
                ),
            )
        )

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=periods[0],
        pratyantardasha=periods[1],
        sookshma=periods[2],
        prana=periods[3],
        deha=periods[4],
    )

    assert hierarchy.mahadasha.planet == "Jupiter"
    assert hierarchy.antardasha.planet == "Saturn"
    assert hierarchy.pratyantardasha.planet == "Mars"
    assert hierarchy.sookshma.planet == "Mercury"
    assert hierarchy.prana.planet == "Venus"
    assert hierarchy.deha.planet == "Sun"

    assert hierarchy.antardasha.parent_lord == "Jupiter"
    assert hierarchy.pratyantardasha.parent_lord == "Saturn"
    assert hierarchy.sookshma.parent_lord == "Mars"
    assert hierarchy.prana.parent_lord == "Mercury"
    assert hierarchy.deha.parent_lord == "Venus"


def test_interpret_dasha_hierarchy_moment():
    """Hierarchy should preserve the supplied moment."""

    moment = datetime(
        2026,
        8,
        17,
        12,
        0,
    )

    hierarchy = interpret_dasha_hierarchy(
        moment=moment
    )

    assert hierarchy.moment == moment


def test_interpret_dasha_hierarchy_collects_themes(
    mahadasha,
    antardasha,
):
    """Hierarchy should aggregate themes from its levels."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    assert "learning" in hierarchy.themes
    assert "discipline" in hierarchy.themes


def test_interpret_dasha_hierarchy_collects_evidence(
    mahadasha,
    antardasha,
):
    """Hierarchy should aggregate evidence from its levels."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    assert hierarchy.evidence
    assert any(
        "Jupiter" in item
        for item in hierarchy.evidence
    )

    assert any(
        "Saturn" in item
        for item in hierarchy.evidence
    )


def test_interpret_dasha_hierarchy_collects_cautions(
    mahadasha,
    antardasha,
):
    """Hierarchy should aggregate cautions from its levels."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    assert hierarchy.cautions
    assert any(
        "Jupiter" in item
        or "expansion" in item
        for item in hierarchy.cautions
    )


# ============================================================
# COLLECTION HELPER TESTS
# ============================================================


def test_collect_dasha_themes():
    """Theme collection should preserve unique order."""

    first = DashaInterpretation(
        planet="Jupiter",
        level="mahadasha",
        themes=[
            "learning",
            "wisdom",
            "expansion",
        ],
    )

    second = DashaInterpretation(
        planet="Mercury",
        level="antardasha",
        themes=[
            "learning",
            "analysis",
            "communication",
        ],
    )

    result = collect_dasha_themes(
        [
            first,
            second,
        ]
    )

    assert result == [
        "learning",
        "wisdom",
        "expansion",
        "analysis",
        "communication",
    ]


def test_collect_dasha_themes_none():
    """None should produce an empty theme collection."""

    assert collect_dasha_themes(
        None
    ) == []


def test_collect_dasha_evidence():
    """Evidence collection should remove duplicates."""

    first = DashaInterpretation(
        planet="Jupiter",
        level="mahadasha",
        evidence=[
            "Evidence A",
            "Evidence B",
        ],
    )

    second = DashaInterpretation(
        planet="Saturn",
        level="antardasha",
        evidence=[
            "Evidence B",
            "Evidence C",
        ],
    )

    result = collect_dasha_evidence(
        [
            first,
            second,
        ]
    )

    assert result == [
        "Evidence A",
        "Evidence B",
        "Evidence C",
    ]


def test_collect_dasha_evidence_none():
    """None should produce an empty evidence collection."""

    assert collect_dasha_evidence(
        None
    ) == []


def test_collect_dasha_cautions():
    """Caution collection should remove duplicates."""

    first = DashaInterpretation(
        planet="Jupiter",
        level="mahadasha",
        cautions=[
            "Caution A",
            "Caution B",
        ],
    )

    second = DashaInterpretation(
        planet="Saturn",
        level="antardasha",
        cautions=[
            "Caution B",
            "Caution C",
        ],
    )

    result = collect_dasha_cautions(
        [
            first,
            second,
        ]
    )

    assert result == [
        "Caution A",
        "Caution B",
        "Caution C",
    ]


def test_collect_dasha_cautions_none():
    """None should produce an empty caution collection."""

    assert collect_dasha_cautions(
        None
    ) == []


# ============================================================
# CURRENT DASHA CONTEXT TESTS
# ============================================================


def test_interpret_current_dasha_direct_attributes(
    mahadasha,
    antardasha,
):
    """Current Dasha should be read from direct context attributes."""

    class Context:
        current_mahadasha = mahadasha
        current_antardasha = antardasha
        current_pratyantardasha = None
        current_sookshmadasha = None
        current_pranadasha = None
        current_dehadasha = None
        current_moment = datetime(
            2026,
            1,
            1,
        )

    result = interpret_current_dasha(
        Context()
    )

    assert result.mahadasha.planet == "Jupiter"
    assert result.antardasha.planet == "Saturn"
    assert result.moment == datetime(
        2026,
        1,
        1,
    )


def test_interpret_current_dasha_normalized_context(
    mahadasha,
    antardasha,
):
    """Current Dasha should support context.dasha hierarchy."""

    moment = datetime(
        2026,
        5,
        1,
    )

    dasha_context = MockDashaContext(
        mahadasha=mahadasha,
        antardasha=antardasha,
        moment=moment,
    )

    context = MockInterpretationContext(
        dasha=dasha_context
    )

    result = interpret_current_dasha(
        context
    )

    assert result.mahadasha.planet == "Jupiter"
    assert result.antardasha.planet == "Saturn"
    assert result.moment == moment


def test_interpret_current_dasha_direct_attributes_override_nested_context(
    mahadasha,
    antardasha,
):
    """Direct context values should take precedence over nested values."""

    nested_mahadasha = MockMahadasha(
        planet="Saturn",
        start=mahadasha.start,
        end=mahadasha.end,
        duration_years=19.0,
    )

    nested = MockDashaContext(
        mahadasha=nested_mahadasha,
        antardasha=antardasha,
    )

    class Context:
        current_mahadasha = mahadasha
        current_antardasha = None
        current_pratyantardasha = None
        current_sookshmadasha = None
        current_pranadasha = None
        current_dehadasha = None
        current_moment = None
        dasha = nested

    result = interpret_current_dasha(
        Context()
    )

    assert result.mahadasha.planet == "Jupiter"


def test_interpret_current_dasha_invalid_context():
    """None context should be rejected."""

    with pytest.raises(
        ValueError,
        match="context must not be None",
    ):
        interpret_current_dasha(
            None
        )


def test_interpret_current_dasha_invalid_moment_is_ignored(
    mahadasha,
):
    """Non-datetime moments should not be propagated."""

    class Context:
        current_mahadasha = mahadasha
        current_antardasha = None
        current_pratyantardasha = None
        current_sookshmadasha = None
        current_pranadasha = None
        current_dehadasha = None
        current_moment = "not-a-datetime"

    result = interpret_current_dasha(
        Context()
    )

    assert result.moment is None


# ============================================================
# ACCESSOR TESTS
# ============================================================


def test_active_dasha_lords(
    mahadasha,
    antardasha,
):
    """Active lords should be returned from highest to lowest."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    assert active_dasha_lords(
        hierarchy
    ) == [
        "Jupiter",
        "Saturn",
    ]


def test_active_dasha_lords_empty():
    """Empty hierarchy should return no active lords."""

    hierarchy = DashaHierarchyInterpretation()

    assert active_dasha_lords(
        hierarchy
    ) == []


def test_active_dasha_lords_requires_interpretation():
    """None hierarchy should be rejected."""

    with pytest.raises(
        ValueError,
        match="interpretation must not be None",
    ):
        active_dasha_lords(
            None
        )


def test_dasha_interpretations_involving_planet():
    """Planet filtering should be case-insensitive."""

    interpretations = [
        DashaInterpretation(
            planet="Jupiter",
            level="mahadasha",
        ),
        DashaInterpretation(
            planet="Saturn",
            level="antardasha",
        ),
        DashaInterpretation(
            planet="Jupiter",
            level="pratyantardasha",
        ),
    ]

    result = dasha_interpretations_involving_planet(
        interpretations,
        "jUpItEr",
    )

    assert len(result) == 2
    assert result[0].planet == "Jupiter"
    assert result[1].planet == "Jupiter"


def test_dasha_interpretations_involving_planet_no_match():
    """No matching planet should produce an empty list."""

    interpretations = [
        DashaInterpretation(
            planet="Jupiter",
            level="mahadasha",
        )
    ]

    assert dasha_interpretations_involving_planet(
        interpretations,
        "Saturn",
    ) == []


def test_dasha_interpretations_involving_planet_requires_interpretations():
    """None interpretations should be rejected."""

    with pytest.raises(
        ValueError,
        match="interpretations must not be None",
    ):
        dasha_interpretations_involving_planet(
            None,
            "Jupiter",
        )


def test_dasha_interpretations_involving_planet_requires_planet():
    """None planet should be rejected."""

    interpretations = [
        DashaInterpretation(
            planet="Jupiter",
            level="mahadasha",
        )
    ]

    with pytest.raises(
        ValueError,
        match="planet must not be None",
    ):
        dasha_interpretations_involving_planet(
            interpretations,
            None,
        )


def test_dasha_interpretations_involving_planet_empty_planet():
    """Empty planet should be rejected."""

    interpretations = [
        DashaInterpretation(
            planet="Jupiter",
            level="mahadasha",
        )
    ]

    with pytest.raises(
        ValueError,
        match="planet must not be empty",
    ):
        dasha_interpretations_involving_planet(
            interpretations,
            "",
        )


# ============================================================
# REPORT TESTS
# ============================================================


def test_dasha_analysis_report_empty():
    """Empty hierarchy should produce an empty report."""

    hierarchy = DashaHierarchyInterpretation()

    assert dasha_analysis_report(
        hierarchy
    ) == []


def test_dasha_analysis_report_mahadasha(
    mahadasha,
):
    """Report should include Mahadasha information."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha
    )

    report = dasha_analysis_report(
        hierarchy
    )

    assert any(
        line.startswith(
            "Mahadasha: Jupiter"
        )
        for line in report
    )

    assert any(
        "start=" in line
        for line in report
    )

    assert any(
        "end=" in line
        for line in report
    )


def test_dasha_analysis_report_hierarchy(
    mahadasha,
    antardasha,
):
    """Report should contain supplied hierarchy levels."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    report = dasha_analysis_report(
        hierarchy
    )

    assert any(
        line.startswith(
            "Mahadasha: Jupiter"
        )
        for line in report
    )

    assert any(
        line.startswith(
            "Antardasha: Saturn"
        )
        for line in report
    )


def test_dasha_analysis_report_themes(
    mahadasha,
):
    """Report should include aggregated themes."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha
    )

    report = dasha_analysis_report(
        hierarchy
    )

    assert any(
        line.startswith(
            "Themes:"
        )
        for line in report
    )


def test_dasha_analysis_report_cautions(
    mahadasha,
):
    """Report should include aggregated cautions."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha
    )

    report = dasha_analysis_report(
        hierarchy
    )

    assert any(
        line.startswith(
            "Cautions:"
        )
        for line in report
    )


def test_dasha_analysis_report_requires_interpretation():
    """None hierarchy should be rejected by report generation."""

    with pytest.raises(
        ValueError,
        match="interpretation must not be None",
    ):
        dasha_analysis_report(
            None
        )


# ============================================================
# PUBLIC API SANITY TESTS
# ============================================================


def test_classical_dasha_theme_coverage():
    """All nine classical Vimshottari planets should be covered."""

    expected = {
        "Ketu",
        "Venus",
        "Sun",
        "Moon",
        "Mars",
        "Rahu",
        "Jupiter",
        "Saturn",
        "Mercury",
    }

    assert set(
        DASHA_THEMES.keys()
    ) == expected

    assert set(
        DASHA_CAUTIONS.keys()
    ) == expected


def test_interpretation_is_structural_not_predictive(
    mahadasha,
):
    """
    The interpretation should contain themes and evidence,
    not deterministic prediction fields.
    """

    interpretation = interpret_dasha(
        mahadasha
    )

    result = interpretation.to_dict()

    assert "themes" in result
    assert "evidence" in result
    assert "cautions" in result

    assert "prediction" not in result
    assert "event" not in result
    assert "guarantee" not in result


def test_hierarchy_is_structural_not_predictive(
    mahadasha,
    antardasha,
):
    """Hierarchy should remain interpretive rather than predictive."""

    hierarchy = interpret_dasha_hierarchy(
        mahadasha=mahadasha,
        antardasha=antardasha,
    )

    result = hierarchy.to_dict()

    assert "themes" in result
    assert "evidence" in result
    assert "cautions" in result

    assert "prediction" not in result
    assert "guaranteed_event" not in result