from datetime import datetime, timezone

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/time", tags=["Time"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@router.get("/now")
def get_current_time():
    return {"current_time": utc_now().isoformat().replace("+00:00", "Z")}


@router.get("/timestamp")
def get_timestamp():
    return {"timestamp": int(utc_now().timestamp())}


@router.get("/timestamp-ms")
def get_timestamp_ms():
    """Return the current Unix timestamp in milliseconds for JavaScript clients."""
    instant = utc_now()
    return int(instant.timestamp()) * 1000 + instant.microsecond // 1000


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
