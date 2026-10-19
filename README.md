# 🐍 FastAPI Snake

A small learning project where I studied **HTTP** and **FastAPI**. It is a mini app for tracking snakes in an imaginary science center: add, view, update and delete snakes.

## Features

- CRUD API for snakes
- Request validation with Pydantic
- Error handling with proper HTTP status codes (`400`, `404`, `422`)
- Layered structure: API → services → repositories
- Auto-generated docs (Swagger UI)

## Tech stack

Python 3.10+, FastAPI, Pydantic, Uvicorn

## Project structure

```
├── main.py                  # App entry point
└── app/
    ├── api/v1/snakes.py     # Endpoints (HTTP layer)
    ├── services/snakes.py   # Business logic
    ├── repositories/snakes.py  # Data access (in-memory storage)
    └── schemas/schemas.py   # Pydantic models
```

## Run locally

```bash
git clone https://github.com/Azorfly/FastAPI_Snake.git
cd FastAPI_Snake
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API in your browser.

## Endpoints

| Method   | Path                | Description           |
|----------|---------------------|-----------------------|
| `GET`    | `/snake`            | Get all snakes        |
| `GET`    | `/snake/{snake_id}` | Get a snake by id     |
| `POST`   | `/snake`            | Add a new snake       |
| `PATCH`  | `/snake/{snake_id}` | Partially update one  |
| `DELETE` | `/snake/{snake_id}` | Delete a snake        |

## Example

```bash
curl -X POST http://127.0.0.1:8000/snake \
  -H "Content-Type: application/json" \
  -d '{"snake_id": 1, "snake_name": "Kaa", "snake_age": 5}'
```

```json
{ "message": "Змея добавлена!" }
```

## Note

Data is stored in memory, so it is lost when the server restarts.