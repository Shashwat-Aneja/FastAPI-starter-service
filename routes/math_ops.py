import math

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/math",
    tags=["Math Operations"],
)


def _validate_operands(x: float, y: float) -> None:
    if not math.isfinite(x) or not math.isfinite(y):
        raise HTTPException(status_code=422, detail="Operands must be finite numbers.")


def _finite_result(result: float) -> float:
    if not math.isfinite(result):
        raise HTTPException(status_code=422, detail="Result is outside the supported numeric range.")
    return result


@router.get("/add")
def add(x: float, y: float):
    _validate_operands(x, y)
    result = _finite_result(x + y)
    return {"operation": "add", "x": x, "y": y, "result": result}


@router.get("/subtract")
def subtract(x: float, y: float):
    _validate_operands(x, y)
    result = _finite_result(x - y)
    return {"operation": "subtract", "x": x, "y": y, "result": result}


@router.get("/multiply")
def multiply(x: float, y: float):
    _validate_operands(x, y)
    result = _finite_result(x * y)
    return {"operation": "multiply", "x": x, "y": y, "result": result}


@router.get("/divide")
def divide(x: float, y: float):
    _validate_operands(x, y)
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero.")
    result = _finite_result(x / y)
    return {"operation": "divide", "x": x, "y": y, "result": result}
