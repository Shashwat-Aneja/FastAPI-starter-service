import logging
import re
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes import hello, math_ops, time_route

REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")

logger = logging.getLogger(__name__)


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
    started_at = time.perf_counter()
    request.state.started_at = started_at
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started_at) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{elapsed_ms:.3f}"
    return response


@app.exception_handler(Exception)
async def handle_unhandled_exception(request: Request, exc: Exception):
    """Keep diagnostic headers on server errors without exposing exception details."""
    request_id = getattr(request.state, "request_id", None) or str(uuid4())
    started_at = getattr(request.state, "started_at", None)
    elapsed_ms = (
        (time.perf_counter() - started_at) * 1000
        if isinstance(started_at, (int, float))
        else 0.0
    )
    logger.error(
        "Unhandled request error",
        exc_info=exc,
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers={
            "X-Request-ID": request_id,
            "X-Process-Time-Ms": f"{elapsed_ms:.3f}",
        },
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
