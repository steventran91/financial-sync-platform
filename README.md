# Financial Sync Platform

A FastAPI-based backend that simulates a real-world financial ETL pipeline, similar to systems used in healthcare billing and fintech. Built to demonstrate backend and data engineering skills including REST API design, database modeling, data validation, pipeline orchestration, and cloud storage integration.

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM for database models
- **Pydantic** — request/response validation
- **Apache Airflow** — pipeline orchestration and scheduling
- **AWS S3** — cloud storage for CSV ingestion and error reporting
- **Docker + Docker Compose** — containerized services
- **pytest** — automated test suite

## Architecture

```
HTTP Upload ──→ ETL Service ──→ PostgreSQL
                   ↑
AWS S3 ──→ Airflow DAG (scheduled daily)
                   ↓
           Failed rows ──→ AWS S3 (JSON error report)
```

## Features

### REST API
- Full CRUD for `transactions` and `sync_jobs`
- Filter transactions by `status`, `merchant`, or `sync_job_id`
- Pagination via `limit` and `offset` query parameters
- API key authentication on all endpoints

### Data Validation
- Pydantic validators enforce positive amounts and reject future transaction dates
- Invalid rows are skipped during ETL and reported separately

### ETL Pipeline (two modes)
- **HTTP upload** — `POST /transactions/upload` accepts a CSV file and processes it in real time
- **Airflow DAG** — scheduled daily pipeline that pulls CSV from AWS S3, validates rows, loads valid data into PostgreSQL, and writes failed rows to a separate S3 JSON file for investigation

### Infrastructure
- Fully containerized with Docker Compose (app database, Airflow metadata database, Airflow webserver, Airflow scheduler)
- Separate test database for isolated test runs
- Secrets managed via `.env` file (not committed)

## How to Run

**1. Clone the repo and set up environment variables:**
```bash
cp .env.example .env
# Fill in your database credentials, AWS keys, and API key
```

**2. Start all services:**
```bash
docker compose up -d
```

**3. Create database tables:**
```bash
python -m scripts.create_tables
```

**4. Start the API:**
```bash
uvicorn backend.app.main:app --reload
```

**5. API docs:**
```
http://localhost:8000/docs
```

**6. Airflow UI:**
```
http://localhost:8080
```

**7. Run tests:**
```bash
PYTHONPATH=. pytest tests/test_main.py -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/sync-jobs` | List all sync jobs |
| POST | `/sync-jobs` | Create a sync job |
| GET | `/sync-jobs/{id}` | Get sync job by ID |
| GET | `/transactions` | List transactions (supports filtering + pagination) |
| POST | `/transactions` | Create a transaction |
| GET | `/transactions/{id}` | Get transaction by ID |
| PATCH | `/transactions/{id}` | Update transaction status |
| DELETE | `/transactions/{id}` | Delete a transaction |
| POST | `/transactions/upload` | Upload CSV for ETL processing |

## Authentication

All endpoints require an API key passed in the request header:
```
financial-platform-api-key: your-api-key
```
