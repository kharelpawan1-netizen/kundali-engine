from types import SimpleNamespace

import pytest

from yogas.gaja_kesari import (
    GAJA_KESARI_NAME,
    jupiter_kendra_from_moon,
    detect_gaja_kesari,
)


def make_context(moon_house, jupiter_house):
    return SimpleNamespace(
        planets={
            "Moon": SimpleNamespace(
                name="Moon",
                house=moon_house,
            ),
            "Jupiter": SimpleNamespace(
                name="Jupiter",
                house=jupiter_house,
            ),
        }
    )


# ============================================================
# Jupiter Kendra from Moon
# ============================================================

@pytest.mark.parametrize(
    "moon_house,jupiter_house",
    [
        # Jupiter in 1st from Moon
        (1, 1),
        (5, 5),

        # Jupiter in 4th from Moon
        (1, 4),
        (5, 8),

        # Jupiter in 7th from Moon
        (1, 7),
        (5, 11),

        # Jupiter in 10th from Moon
        (1, 10),
        (5, 2),
    ],
)
def test_gaja_kesari_detected_in_kendra(
    moon_house,
    jupiter_house,
):
    context = make_context(
        moon_house,
        jupiter_house,
    )

    assert (
        jupiter_kendra_from_moon(
            context
        )
        is True
    )


# ============================================================
# Non-Kendra placements
# ============================================================

@pytest.mark.parametrize(
    "moon_house,jupiter_house",
    [
        # 2nd from Moon
        (1, 2),

        # 3rd from Moon
        (1, 3),

        # 5th from Moon
        (1, 5),

        # 6th from Moon
        (1, 6),

        # 8th from Moon
        (1, 8),

        # 9th from Moon
        (1, 9),

        # 11th from Moon
        (1, 11),

        # 12th from Moon
        (1, 12),
    ],
)
def test_gaja_kesari_not_detected_outside_kendra(
    moon_house,
    jupiter_house,
):
    context = make_context(
        moon_house,
        jupiter_house,
    )

    assert (
        jupiter_kendra_from_moon(
            context
        )
        is False
    )


# ============================================================
# Missing Moon
# ============================================================

def test_gaja_kesari_missing_moon():
    context = SimpleNamespace(
        planets={
            "Jupiter": SimpleNamespace(
                name="Jupiter",
                house=1,
            )
        }
    )

    assert (
        jupiter_kendra_from_moon(
            context
        )
        is False
    )


# ============================================================
# Missing Jupiter
# ============================================================

def test_gaja_kesari_missing_jupiter():
    context = SimpleNamespace(
        planets={
            "Moon": SimpleNamespace(
                name="Moon",
                house=1,
            )
        }
    )

    assert (
        jupiter_kendra_from_moon(
            context
        )
        is False
    )


# ============================================================
# Both planets missing
# ============================================================

def test_gaja_kesari_missing_both_planets():
    context = SimpleNamespace(
        planets={}
    )

    assert (
        jupiter_kendra_from_moon(
            context
        )
        is False
    )


# ============================================================
# Detection
# ============================================================

@pytest.mark.parametrize(
    "moon_house,jupiter_house",
    [
        (1, 1),
        (1, 4),
        (1, 7),
        (1, 10),
        (5, 5),
        (5, 8),
        (5, 11),
        (5, 2),
    ],
)
def test_detect_gaja_kesari(
    moon_house,
    jupiter_house,
):
    context = make_context(
        moon_house,
        jupiter_house,
    )

    result = detect_gaja_kesari(
        context
    )

    assert result is not None
    assert result.name == GAJA_KESARI_NAME


def test_detect_gaja_kesari_returns_none_when_not_present():
    context = make_context(
        moon_house=1,
        jupiter_house=2,
    )

    result = detect_gaja_kesari(
        context
    )

    assert result is None