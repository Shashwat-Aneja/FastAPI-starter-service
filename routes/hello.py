from fastapi import APIRouter, HTTPException, Query

router = APIRouter(
    prefix="/hello",
    tags=["Hello"]
)

@router.get("/")
def say_hello():
    return {"message": "Hello from FastAPI!"}

@router.get("/greet")
def greet(name: str = Query(default="Guest", max_length=80)):
    normalized_name = name.strip()
    if not normalized_name:
        raise HTTPException(status_code=422, detail="Name must not be blank.")
    return {"message": f"Hello, {normalized_name}! Welcome to the FastAPI Starter Service."}
