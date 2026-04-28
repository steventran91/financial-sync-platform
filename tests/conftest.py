import os
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/financial_sync_test",
)

import pytest
from sqlalchemy import delete
from backend.app.db.session import SessionLocal
from backend.app.db.models.sync_job import SyncJobDB


@pytest.fixture(autouse=True)
def clear_sync_jobs():
    db = SessionLocal()
    try:
        db.execute(delete(SyncJobDB))
        db.commit()
    finally:
        db.close()