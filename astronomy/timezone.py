"""
astronomy/timezone.py

Timezone utilities for the Kundali Engine.

Version: 1.2.1
Compatible with Python 3.9
"""

from datetime import timezone

import pytz


def local_to_utc(local_datetime, timezone_name):
    """
    Convert local datetime to UTC.

    Parameters
    ----------
    local_datetime : datetime
        Naive local datetime.

    timezone_name : str
        Example:
            Asia/Kathmandu
            Asia/Kolkata
            Europe/London

    Returns
    -------
    datetime
        Timezone-aware UTC datetime.
    """

    tz = pytz.timezone(timezone_name)

    local_dt = tz.localize(local_datetime)

    utc_dt = local_dt.astimezone(timezone.utc)

    return utc_dt