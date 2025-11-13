from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/time",
    tags=["Time"]
)

@router.get("/now")
def get_current_time():
    return {
        "current_time": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/timestamp")
def get_timestamp():
    return {
        "timestamp": int(datetime.utcnow().timestamp())
    }

@router.get("/formatted")
def get_formatted_time():
    return {
        "formatted_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
