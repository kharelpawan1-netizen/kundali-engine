"""
astronomy/julian.py

Julian Day utilities.

Version:
    2.1.0

Compatible with Python 3.9
"""

from datetime import datetime

import swisseph as swe


def datetime_to_julian(dt: datetime) -> float:
    """
    Convert a UTC datetime to Julian Day.

    Parameters
    ----------
    dt : datetime
        UTC datetime.

    Returns
    -------
    float
        Julian Day.
    """

    hour = (
        dt.hour + dt.minute / 60.0 + dt.second / 3600.0 + dt.microsecond / 3600000000.0
    )

    return swe.julday(dt.year, dt.month, dt.day, hour)


def julian_to_datetime(jd: float) -> datetime:
    """
    Convert Julian Day to UTC datetime.

    Parameters
    ----------
    jd : float
        Julian Day.

    Returns
    -------
    datetime
        UTC datetime.
    """

    year, month, day, hour = swe.revjul(jd)

    hours = int(hour)

    minutes = int((hour - hours) * 60)

    seconds = int(round((((hour - hours) * 60) - minutes) * 60))

    return datetime(year, month, day, hours, minutes, seconds)
