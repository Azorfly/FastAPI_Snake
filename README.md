# 🐍 FastAPI Snake

A learning project where I study **HTTP**, **FastAPI**, **SQLAlchemy** and **testing**. It is a small REST API for tracking snakes in an imaginary science center: add, view, update and delete snakes. Data is stored in **PostgreSQL**.

## Features

- CRUD API for snakes
- PostgreSQL storage via SQLAlchemy 2.x (psycopg 3 driver)
- Layered architecture: API → service → repository → ORM model
- Dependency injection with FastAPI `Depends` (one DB session per request)
- Request validation with Pydantic (`422` on invalid input)
- Global error handler: a missing snake returns `404` with a Russian message
- Unit tests with mocks and integration tests against a real Postgres in Docker ([testcontainers](https://testcontainers-python.readthedocs.io/))
- Auto-generated docs (Swagger UI)

## Tech stack

- Python 3.12+
- FastAPI, Pydantic, Uvicorn
- PostgreSQL, SQLAlchemy 2.x, psycopg 3
- pytest, testcontainers, httpx (`TestClient`)
- Docker (for the database and the integration tests)

## Project structure

```
├── main.py                      # App entry point, router + 404 handler for SnakeNotFound
├── pytest.ini                   # pytest config (pythonpath = .)
├── requirements.txt
├── app/
│   ├── api/v1/snakes.py         # Endpoints (HTTP layer), prefix /snake
│   ├── services/snakes.py       # Business logic, maps DB objects to Pydantic schemas
│   ├── repositories/snakes.py   # Data access: SQL queries through the SQLAlchemy session
│   ├── models/snake.py          # SQLAlchemy ORM model (table "snake")
│   ├── schemas/schemas.py       # Pydantic schemas for requests and responses
│   ├── db_session.py            # Engine + get_session dependency
│   └── exceptions.py            # SnakeNotFound
└── test/
    ├── unit/                    # Service tests, repository is mocked (no DB needed)
    └── integration/             # Real Postgres in Docker: repository and full HTTP cycle
```

### How a request flows

```
HTTP request → router (app/api) → SnakeService (app/services) → repository (app/repositories) → PostgreSQL
```

- The DB session comes from `get_session` through `Depends` and is closed after the request.
- The ORM model uses `id / name / age / added`, the API uses `snake_id / snake_name / snake_age / added`. The service converts between them (`db_to_pydantic`).
- If a snake is not found, the repository raises `SnakeNotFound`, and the handler in `main.py` turns it into a `404`.

## Run locally

### 1. Install

```bash
git clone https://github.com/Azorfly/FastAPI_Snake.git
cd FastAPI_Snake
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start PostgreSQL

The app connects to `postgresql+psycopg://postgres:<password>@localhost:5432/postgres`. The URL is set in `app/db_session.py`, so use the same password there and in Docker:

```bash
docker run -d --name snake-db -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres:16
```

### 3. Create the table

The app does not create tables on startup, so create the table once:

```sql
CREATE TABLE snake (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    age   INTEGER      NOT NULL,
    added DATE         NOT NULL DEFAULT CURRENT_DATE
);
```

For example: `docker exec -it snake-db psql -U postgres`, then paste the SQL.

### 4. Run the server

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try the API in your browser.

## Endpoints

| Method   | Path                | Description                    | Success | Errors     |
|----------|---------------------|--------------------------------|---------|------------|
| `GET`    | `/snake`            | Get all snakes (sorted by id)  | `200`   | —          |
| `GET`    | `/snake/{snake_id}` | Get a snake by id              | `200`   | `404`, `422` |
| `POST`   | `/snake`            | Add a new snake                | `201`   | `422`      |
| `PATCH`  | `/snake/{snake_id}` | Update name and/or age         | `200`   | `404`, `422` |
| `DELETE` | `/snake/{snake_id}` | Delete a snake                 | `200`   | `404`, `422` |

- `404`: no snake with this id.
- `422`: invalid input (the id is not a number, a required field is missing, wrong type).
- `id` and `added` (date) are set by the database.
- `PATCH` changes only the fields you send. An empty body `{}` returns the snake unchanged.

## Examples

**Add a snake**

```bash
curl -X POST http://127.0.0.1:8000/snake \
  -H "Content-Type: application/json" \
  -d '{"snake_name": "Kaa", "snake_age": 5}'
```

```json
{
  "message": "Змея добавлена!",
  "id": 1,
  "name": "Kaa",
  "age": 5,
  "date added": "2026-11-14"
}
```

**Get a snake**

```bash
curl http://127.0.0.1:8000/snake/1
```

```json
{ "snake_id": 1, "snake_name": "Kaa", "snake_age": 5, "added": "2026-11-14" }
```

**Update a snake**

```bash
curl -X PATCH http://127.0.0.1:8000/snake/1 \
  -H "Content-Type: application/json" \
  -d '{"snake_age": 6}'
```

```json
{
  "message": "Змея с id 1 обновлена!",
  "updated_snake": { "snake_id": 1, "snake_name": "Kaa", "snake_age": 6, "added": "2026-11-14" }
}
```

**Delete a snake**

```bash
curl -X DELETE http://127.0.0.1:8000/snake/1
```

```json
{ "message": "Змея с ID 1 удалена." }
```

**Snake not found**

```json
{ "detail": "Змеи с ID 1 не существует." }
```

## Tests

```bash
pytest                    # all tests
pytest test/unit          # unit tests only (no Docker needed)
pytest test/integration   # integration tests (Docker must be running)
```

- **Unit tests** (`test/unit/`): test `SnakeService` with the repository replaced by mocks.
- **Integration tests** (`test/integration/`):
  - `testcontainers` starts a fresh `postgres:16` container once per test run, and the tables are created from the ORM model.
  - Each test runs inside a transaction that is rolled back afterwards, so tests don't see each other's data.
  - Test data is seeded with a fixture, not through the code under test.
  - `TestClient` sends real HTTP requests to the app, and `app.dependency_overrides` points `get_session` at the test database.
  - Every endpoint is covered: success cases, `404` and `422`.

## Known limitations

- The database URL is hard-coded in `app/db_session.py`.
- No migrations yet: the table is created by hand.
- Validation checks types only: an empty name or a negative age is accepted.
