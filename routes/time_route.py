from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/time", tags=["Time"])


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@router.get("/now")
def get_current_time():
    return {"current_time": utc_now().isoformat().replace("+00:00", "Z")}


@router.get("/timestamp")
def get_timestamp():
    return {"timestamp": int(utc_now().timestamp())}


@router.get("/formatted")
def get_formatted_time():
    return {"formatted_time": utc_now().strftime("%Y-%m-%d %H:%M:%S UTC")}
