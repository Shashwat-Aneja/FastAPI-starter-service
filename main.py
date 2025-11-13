from fastapi import FastAPI
from routes import hello, math_ops, time_route

app = FastAPI(
    title="FastAPI Starter Service",
    description="A clean and minimal FastAPI template for learning and quick backend development.",
    version="1.0.0"
)

# Register routes
app.include_router(hello.router)
app.include_router(math_ops.router)
app.include_router(time_route.router)


@app.get("/")
def root():
    return {
        "message": "FastAPI Starter Service is running!",
        "docs": "/docs"
    }
