from models.ephemeris_position import EphemerisPosition


def test_position_creation():
    position = EphemerisPosition(
        longitude=100.0,
        latitude=2.0,
        distance=1.0,
        longitude_speed=0.9856,
        latitude_speed=0.0,
        distance_speed=0.0,
        retrograde=False,
    )

    assert position.longitude == 100.0
    assert position.latitude == 2.0
    assert position.distance == 1.0
    assert not position.retrograde
