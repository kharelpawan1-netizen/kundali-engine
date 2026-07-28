"""
Tests for Paksha Bala.

According to Brihat Parashara Hora Shastra.
"""

from astronomy.paksha_bala import moon_phase_angle, paksha_bala


def test_new_moon():
    """
    Sun and Moon together.
    """

    result = paksha_bala(
        100.0,
        100.0,
    )

    assert result.value == 0.0


def test_first_quarter():
    """
    90° separation.
    """

    result = paksha_bala(
        0.0,
        90.0,
    )

    assert result.value == 30.0


def test_full_moon():
    """
    180° separation.
    """

    result = paksha_bala(
        0.0,
        180.0,
    )

    assert result.value == 60.0


def test_last_quarter():
    """
    270° separation.
    """

    result = paksha_bala(
        0.0,
        270.0,
    )

    assert result.value == 30.0


def test_wraparound_angle():
    """
    Longitude wraparound.
    """

    angle = moon_phase_angle(
        350.0,
        10.0,
    )

    assert angle == 20.0


def test_wraparound_strength():
    """
    Strength across 360° boundary.
    """

    result = paksha_bala(
        350.0,
        10.0,
    )

    assert result.value == (20.0 / 3.0)


def test_zero_and_360_same():
    """
    0° and 360° are identical.
    """

    result = paksha_bala(
        0.0,
        360.0,
    )

    assert result.value == 0.0


def test_value_never_exceeds_sixty():
    """
    Paksha Bala is always between 0 and 60.
    """

    for angle in range(361):
        value = paksha_bala(
            0.0,
            float(angle),
        ).value

        assert 0.0 <= value <= 60.0
