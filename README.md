# Financial Sync Platform

A FastAPI-based backend that simulates a real-world financial ETL pipeline.
Built to practice backend and data engineering concepts including REST APIs,
database modeling, data validation, and pipeline orchestration.

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM for database models
- **Pydantic** — data validation
- **Apache Airflow** — pipeline orchestration and scheduling
- **Docker** — containerized services

## Features

- Full CRUD API for transactions and sync jobs
- Filter transactions by status, merchant, or sync job
- Pagination support
- CSV file upload with ETL processing
- Pydantic validation (positive amounts, no future dates)
- Airflow DAG for scheduled ETL pipeline (extract → transform → load)
- Separate test database with full test suite

## How to Run

**Start the database and Airflow:**
```bash
docker compose up -d
