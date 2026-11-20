from datetime import datetime, timezone

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/time", tags=["Time"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@router.get("/now")
def get_current_time():
    return {"current_time": utc_now().isoformat().replace("+00:00", "Z")}


def _unix_microseconds(instant):
    delta = instant - datetime(1970, 1, 1, tzinfo=timezone.utc)
    return (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds


@router.get("/timestamp")
def get_timestamp():
    return {"timestamp": _unix_microseconds(utc_now()) // 1_000_000}


@router.get("/timestamp-ms")
def get_timestamp_ms():
    """Return the current Unix timestamp in milliseconds for JavaScript clients."""
    instant = utc_now()
    return _unix_microseconds(instant) // 1000


@router.get("/formatted")
def get_formatted_time():
    return {"formatted_time": utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")}


@router.get("/zone")
def get_zoned_time(name: str = Query(default="UTC", min_length=1, max_length=100)):
    """Convert the same UTC instant to a named IANA timezone."""
    try:
        zone = ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        raise HTTPException(status_code=422, detail="Unknown IANA timezone.")
    return {"timezone": name, "current_time": utc_now().astimezone(zone).isoformat()}
