from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/math",
    tags=["Math Operations"]
)

@router.get("/add")
def add(x: float, y: float):
    return {"operation": "add", "x": x, "y": y, "result": x + y}

@router.get("/subtract")
def subtract(x: float, y: float):
    return {"operation": "subtract", "x": x, "y": y, "result": x - y}

@router.get("/multiply")
def multiply(x: float, y: float):
    return {"operation": "multiply", "x": x, "y": y, "result": x * y}

@router.get("/divide")
def divide(x: float, y: float):
    if y == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero.")
    return {"operation": "divide", "x": x, "y": y, "result": x / y}
