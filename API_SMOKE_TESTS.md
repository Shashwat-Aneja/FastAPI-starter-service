API smoke checks

Start the service with `uvicorn main:app --reload`, then check `GET /`, `GET /healthz`, `GET /version`, and `GET /openapi.json`.

Example:

```sh
curl --fail http://127.0.0.1:8000/healthz
curl --fail http://127.0.0.1:8000/version
```

A successful health response proves the app process is responsive; it does not prove external dependencies are healthy. Add dependency-specific readiness checks if databases, queues, or other services are introduced.