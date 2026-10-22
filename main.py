from fastapi import FastAPI
from routes import hello, math_ops, time_route

app = FastAPI(
    title="FastAPI Starter Service",
    description="A clean and minimal FastAPI template for learning and quick backend development.",
    version="1.0.0",
)

app.include_router(hello.router)
app.include_router(math_ops.router)
app.include_router(time_route.router)


@app.get("/healthz")
def healthz():
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "FastAPI Starter Service is running!", "docs": "/docs"}


@app.get("/readyz")
def readyz():
    """Expose a lightweight readiness probe for deployment orchestration."""
    return {"status": "ready", "service": app.title, "version": app.version}


@app.get("/version")
def version():
    """Expose service metadata for deployment checks and diagnostics."""
    return {"service": app.title, "version": app.version}
