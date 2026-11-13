API smoke checks

Start the service with `uvicorn main:app --reload`, then check `GET /`, `GET /healthz`, `GET /version`, and `GET /openapi.json`.

Example:

```sh
curl --fail http://127.0.0.1:8000/healthz
curl --fail http://127.0.0.1:8000/version
```

A successful health response proves the app process is responsive; it does not prove external dependencies are healthy. Add dependency-specific readiness checks if databases, queues, or other services are introduced.

Greeting input checks:

```sh
curl --fail --get --data-urlencode 'name=  Ada  ' http://127.0.0.1:8000/hello/greet
curl -i --get --data-urlencode 'name=   ' http://127.0.0.1:8000/hello/greet
```

The first request returns a greeting for `Ada` with whitespace trimmed. The second
returns HTTP 422 for a blank name. Names longer than 80 characters also return
HTTP 422, while omitting `name` continues to greet `Guest`.
