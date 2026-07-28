"""
Tests for the unified Varga engine.
"""

from astronomy.varga_engine import build_varga_chart
from models.varga_chart import VargaChart


def test_returns_varga_chart():
    """
    Engine returns a VargaChart.
    """

    chart = build_varga_chart(15.5)

    assert isinstance(chart, VargaChart)


def test_hora_exists():
    chart = build_varga_chart(15.5)

    assert chart.hora is not None


def test_drekkana_exists():
    chart = build_varga_chart(15.5)

    assert chart.drekkana is not None


def test_saptamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.saptamsa is not None


def test_navamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.navamsa is not None


def test_dasamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.dasamsa is not None


def test_dvadasamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.dvadasamsa is not None


def test_shodasamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.shodasamsa is not None


def test_vimsamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.vimsamsa is not None


def test_siddhamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.siddhamsa is not None


def test_bhamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.bhamsa is not None


def test_trimshamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.trimshamsa is not None


def test_khavedamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.khavedamsa is not None


def test_akshavedamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.akshavedamsa is not None


def test_shastiamsa_exists():
    chart = build_varga_chart(15.5)

    assert chart.shastiamsa is not None


def test_repeatability():
    """
    Same longitude should produce identical results.
    """

    a = build_varga_chart(123.456)
    b = build_varga_chart(123.456)

    assert a == b


def test_wraparound():
    """
    Longitudes beyond 360° should wrap.
    """

    a = build_varga_chart(361.25)
    b = build_varga_chart(1.25)

    assert a == b


def test_negative_longitude():
    """
    Negative longitude should normalize.
    """

    chart = build_varga_chart(-1.0)

    assert chart.shastiamsa.division == 59
