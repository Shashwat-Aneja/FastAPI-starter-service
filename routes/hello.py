from fastapi import APIRouter

router = APIRouter(
    prefix="/hello",
    tags=["Hello"]
)

@router.get("/")
def say_hello():
    return {"message": "Hello from FastAPI!"}

@router.get("/greet")
def greet(name: str = "Guest"):
    return {"message": f"Hello, {name}! Welcome to the FastAPI Starter Service."}
