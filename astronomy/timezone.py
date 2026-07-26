"""
astronomy/timezone.py

Timezone utilities for Kundali Engine.

Features
--------
- Validate IANA timezone names.
- Convert local datetime to UTC.
- Convert UTC datetime to local timezone.
- Normalize timezone names.
- Return UTC offset.
- Python 3.9 compatible.

Author:
    Kundali Engine

License:
    MIT
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_TIMEZONE = "UTC"


class TimezoneError(Exception):
    """
    Raised when an invalid timezone is encountered.
    """


def is_valid_timezone(timezone_name: str) -> bool:
    """
    Check whether an IANA timezone exists.

    Parameters
    ----------
    timezone_name : str

    Returns
    -------
    bool
    """

    try:
        ZoneInfo(timezone_name)
        return True
    except ZoneInfoNotFoundError:
        return False


def normalize_timezone(timezone_name: Optional[str]) -> str:
    """
    Normalize timezone string.

    If None or empty, UTC is returned.

    Parameters
    ----------
    timezone_name : str | None

    Returns
    -------
    str
    """

    if timezone_name is None:
        return DEFAULT_TIMEZONE

    timezone_name = timezone_name.strip()

    if timezone_name == "":
        return DEFAULT_TIMEZONE

    if not is_valid_timezone(timezone_name):
        raise TimezoneError(f"Unknown timezone: '{timezone_name}'")

    return timezone_name


def get_timezone(timezone_name: str) -> ZoneInfo:
    """
    Return ZoneInfo object.

    Parameters
    ----------
    timezone_name : str

    Returns
    -------
    ZoneInfo
    """

    timezone_name = normalize_timezone(timezone_name)

    return ZoneInfo(timezone_name)


def local_to_utc(
    local_datetime: datetime,
    timezone_name: str,
) -> datetime:
    """
    Convert local datetime into UTC.

    Parameters
    ----------
    local_datetime : datetime

    timezone_name : str

    Returns
    -------
    datetime
    """

    tz = get_timezone(timezone_name)

    if local_datetime.tzinfo is None:

        local_datetime = local_datetime.replace(tzinfo=tz)

    else:

        local_datetime = local_datetime.astimezone(tz)

    return local_datetime.astimezone(ZoneInfo("UTC"))


def utc_to_local(
    utc_datetime: datetime,
    timezone_name: str,
) -> datetime:
    """
    Convert UTC datetime to local timezone.

    Parameters
    ----------
    utc_datetime : datetime

    timezone_name : str

    Returns
    -------
    datetime
    """

    tz = get_timezone(timezone_name)

    if utc_datetime.tzinfo is None:

        utc_datetime = utc_datetime.replace(tzinfo=ZoneInfo("UTC"))

    else:

        utc_datetime = utc_datetime.astimezone(ZoneInfo("UTC"))

    return utc_datetime.astimezone(tz)


def get_utc_offset(
    timezone_name: str,
    when: Optional[datetime] = None,
) -> timedelta:
    """
    Return the UTC offset for a timezone.

    Parameters
    ----------
    timezone_name : str
        IANA timezone name.

    when : datetime, optional
        Datetime used to determine the offset.
        If omitted, the current datetime is used.

    Returns
    -------
    timedelta
    """

    tz = get_timezone(timezone_name)

    if when is None:
        when = datetime.now(tz)

    elif when.tzinfo is None:
        when = when.replace(tzinfo=tz)

    else:
        when = when.astimezone(tz)

    offset = when.utcoffset()

    if offset is None:
        return timedelta(0)

    return offset


def timezone_name(
    timezone_name: str,
) -> str:
    """
    Return the canonical timezone name.

    Parameters
    ----------
    timezone_name : str

    Returns
    -------
    str
    """

    tz = get_timezone(timezone_name)

    return str(tz)


def current_local_time(
    timezone_name: str,
) -> datetime:
    """
    Return the current local datetime
    in the specified timezone.

    Parameters
    ----------
    timezone_name : str

    Returns
    -------
    datetime
    """

    tz = get_timezone(timezone_name)

    return datetime.now(tz)


def current_utc_time() -> datetime:
    """
    Return the current UTC datetime.

    Returns
    -------
    datetime
    """

    return datetime.now(ZoneInfo("UTC"))


__all__ = [
    "TimezoneError",
    "DEFAULT_TIMEZONE",
    "is_valid_timezone",
    "normalize_timezone",
    "get_timezone",
    "local_to_utc",
    "utc_to_local",
    "get_utc_offset",
    "timezone_name",
    "current_local_time",
    "current_utc_time",
]
