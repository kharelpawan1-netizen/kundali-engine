"""
astronomy/julian.py

Julian Day calculation.

Compatible with Python 3.9
"""

import swisseph as swe


def julian_day(utc_datetime):

    hour = (
        utc_datetime.hour
        + utc_datetime.minute / 60
        + utc_datetime.second / 3600
    )

    return swe.julday(
        utc_datetime.year,
        utc_datetime.month,
        utc_datetime.day,
        hour
    )