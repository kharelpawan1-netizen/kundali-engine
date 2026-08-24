"""
tests/test_sade_sati.py

Tests for Shani Sade Sati calculation engine.
"""

from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from astrology.sade_sati import (
    DAYS_PER_YEAR,
    MOON,
    PEAK_PHASE,
    RISING_PHASE,
    SADE_SATI_NAME,
    SADE_SATI_PHASES,
    SADE_SATI_TOTAL_YEARS,
    SATURN,
    SATURN_PHASE_YEARS,
    SETTING_PHASE,
    ZODIAC_SIGNS,
    SadeSatiPeriod,
    current_sade_sati_period,
    detect_sade_sati_from_context,
    generate_sade_sati_periods,
    house_from_moon,
    is_sade_sati_active,
    moon_and_saturn_signs_from_context,
    sade_sati_evidence,
    sade_sati_phase_name,
    sade_sati_signs,
    sign_from_index,
    sign_index,
)


# ============================================================
# CONSTANTS & VALIDATION TESTS
# ============================================================

def test_constants():
    assert SADE_SATI_NAME == "Shani Sade Sati"
    assert MOON == "Moon"
    assert SATURN == "Saturn"
    assert len(ZODIAC_SIGNS) == 12
    assert SATURN_PHASE_YEARS == 2.5
    assert SADE_SATI_TOTAL_YEARS == 7.5
    assert SADE_SATI_PHASES == (RISING_PHASE, PEAK_PHASE, SETTING_PHASE)


def test_sign_indexing():
    assert sign_index("Aries") == 0
    assert sign_index("Pisces") == 11
    assert sign_from_index(0) == "Aries"
    assert sign_from_index(12) == "Aries"
    assert sign_from_index(-1) == "Pisces"


def test_invalid_sign_raises():
    with pytest.raises(TypeError):
        sign_index(123)

    with pytest.raises(ValueError):
        sign_index("Ophiuchus")


# ============================================================
# HOUSE FROM MOON & PHASE DETECTION
# ============================================================

def test_house_from_moon():
    # Moon in Taurus (index 1)
    assert house_from_moon("Taurus", "Taurus") == 1
    assert house_from_moon("Taurus", "Gemini") == 2
    assert house_from_moon("Taurus", "Aries") == 12
    assert house_from_moon("Taurus", "Leo") == 4
    assert house_from_moon("Taurus", "Scorpio") == 7


def test_sade_sati_signs():
    # Moon in Aries: 12th is Pisces, 1st is Aries, 2nd is Taurus
    assert sade_sati_signs("Aries") == ["Pisces", "Aries", "Taurus"]
    # Moon in Pisces: 12th is Aquarius, 1st is Pisces, 2nd is Aries
    assert sade_sati_signs("Pisces") == ["Aquarius", "Pisces", "Aries"]
    # Moon in Leo: 12th is Cancer, 1st is Leo, 2nd is Virgo
    assert sade_sati_signs("Leo") == ["Cancer", "Leo", "Virgo"]


def test_sade_sati_phase_name():
    # Moon in Scorpio
    assert sade_sati_phase_name("Scorpio", "Libra") == RISING_PHASE
    assert sade_sati_phase_name("Scorpio", "Scorpio") == PEAK_PHASE
    assert sade_sati_phase_name("Scorpio", "Sagittarius") == SETTING_PHASE
    assert sade_sati_phase_name("Scorpio", "Capricorn") is None
    assert sade_sati_phase_name("Scorpio", "Aries") is None


def test_is_sade_sati_active():
    assert is_sade_sati_active("Cancer", "Gemini") is True
    assert is_sade_sati_active("Cancer", "Cancer") is True
    assert is_sade_sati_active("Cancer", "Leo") is True
    assert is_sade_sati_active("Cancer", "Virgo") is False


def test_sade_sati_evidence():
    evidence = sade_sati_evidence("Virgo", "Leo")
    assert len(evidence) == 1
    assert evidence[0]["phase"] == RISING_PHASE
    assert evidence[0]["moon_sign"] == "Virgo"
    assert evidence[0]["saturn_sign"] == "Leo"
    assert evidence[0]["house_from_moon"] == 12

    assert sade_sati_evidence("Virgo", "Aquarius") == []


# ============================================================
# CONTEXT HELPERS
# ============================================================

def test_context_helpers():
    context = SimpleNamespace(
        planets={
            "Moon": SimpleNamespace(sign="Libra"),
            "Saturn": SimpleNamespace(sign="Scorpio"),
        }
    )
    moon_sign, saturn_sign = moon_and_saturn_signs_from_context(context)
    assert moon_sign == "Libra"
    assert saturn_sign == "Scorpio"
    assert detect_sade_sati_from_context(context) == SETTING_PHASE


def test_context_helpers_missing():
    context = SimpleNamespace(planets={})
    moon_sign, saturn_sign = moon_and_saturn_signs_from_context(context)
    assert moon_sign is None
    assert saturn_sign is None
    assert detect_sade_sati_from_context(context) is None


# ============================================================
# TIMELINE GENERATION & PERIODS
# ============================================================

def test_generate_sade_sati_periods():
    start = datetime(2020, 1, 1)
    periods = generate_sade_sati_periods("Gemini", start, phase_years=2.5)

    assert len(periods) == 3
    assert periods[0].phase == RISING_PHASE
    assert periods[0].saturn_sign == "Taurus"
    assert periods[0].start == start

    assert periods[1].phase == PEAK_PHASE
    assert periods[1].saturn_sign == "Gemini"
    assert periods[1].start == periods[0].end

    assert periods[2].phase == SETTING_PHASE
    assert periods[2].saturn_sign == "Cancer"
    assert periods[2].start == periods[1].end

    total_days = sum(p.duration_days for p in periods)
    assert pytest.approx(total_days, 0.1) == 7.5 * DAYS_PER_YEAR


def test_period_contains_and_current():
    start = datetime(2025, 1, 1)
    periods = generate_sade_sati_periods("Capricorn", start, phase_years=2.5)

    test_moment = datetime(2026, 6, 1)
    current = current_sade_sati_period(periods, moment=test_moment)
    assert current is not None
    assert current.phase == RISING_PHASE

    outside_moment = datetime(2035, 1, 1)
    assert current_sade_sati_period(periods, moment=outside_moment) is None
