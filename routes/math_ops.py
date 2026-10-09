import math

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/math",
    tags=["Math Operations"],
)


def _validate_operands(x: float, y: float) -> None:
    if not math.isfinite(x) or not math.isfinite(y):
        raise HTTPException(
            status_code=422,
            detail="Operands must be finite numbers.",
        )


@router.get("/add")
def add(x: float, y: float):
    _validate_operands(x, y)
    return {"operation": "add", "x": x, "y": y, "result": x + y}


@router.get("/subtract")
def subtract(x: float, y: float):
    _validate_operands(x, y)
    return {"operation": "subtract", "x": x, "y": y, "result": x - y}


@router.get("/multiply")
def multiply(x: float, y: float):
    _validate_operands(x, y)
    return {"operation": "multiply", "x": x, "y": y, "result": x * y}


@router.get("/divide")
def divide(x: float, y: float):
    _validate_operands(x, y)
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero.")
    return {"operation": "divide", "x": x, "y": y, "result": x / y}
