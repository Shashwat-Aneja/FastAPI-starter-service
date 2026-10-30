import re
from uuid import uuid4

from fastapi import FastAPI, Request
from routes import hello, math_ops, time_route

REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")

app = FastAPI(
    title="FastAPI Starter Service",
    description="A clean and minimal FastAPI template for learning and quick backend development.",
    version="1.0.0",
)


@app.middleware("http")
async def attach_request_id(request: Request, call_next):
    """Propagate a valid request ID or generate one for tracing a request."""
    incoming_id = request.headers.get("x-request-id", "")
    request_id = incoming_id if REQUEST_ID_PATTERN.fullmatch(incoming_id) else str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


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
