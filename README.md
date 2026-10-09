# FastAPI Starter Service
A clean, minimal, and production-ready FastAPI template designed for learning, prototyping, and building scalable Python backend services.

This project showcases:
- REST API fundamentals
- Structured routing
- Modular backend design
- Clean and readable Python code
- Practical experience with FastAPI and Uvicorn

## Features
- Lightweight REST API
- Modular routes (`/hello`, `/math`, `/time`)
- Automatic interactive API docs at `/docs`
- Health endpoint at `/healthz`
- Finite-number validation for arithmetic inputs and results
- Automated route tests

## Project Structure
```text
fastapi-starter-service/
├── main.py
├── requirements.txt
├── routes/
│   ├── hello.py
│   ├── math_ops.py
│   └── time_route.py
└── tests/
    └── test_math_routes.py
```

## Installation
Create and activate a virtual environment.

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the project and test dependencies:
```bash
python -m pip install -r requirements.txt
```

## Run the API
```bash
uvicorn main:app --reload
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.

## Run Tests
```bash
python -m pytest -q
```

The math route tests cover normal arithmetic, division by zero, non-finite inputs, and arithmetic overflow.

## Example Requests
```bash
curl "http://127.0.0.1:8000/math/add?x=4&y=7"
curl "http://127.0.0.1:8000/time/now"
curl "http://127.0.0.1:8000/healthz"
```
