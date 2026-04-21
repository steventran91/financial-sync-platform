from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200 
    assert response.json() == {"status": "ok"}

def test_get_sync_jobs():
    response = client.get("/sync-jobs")

    assert response.status_code == 200 
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_sync_job_by_id():
    response = client.get("/sync-jobs/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["job_type"] == "payments"

def test_get_sync_job_not_found():
    response = client.get("/sync-jobs/9")

    assert response.status_code == 404 
    assert response.json() == {"detail": "Sync job not found"}

def test_create_sync_job():
    payload = {
        "provider_id": 2001,
        "job_type": "payments",
        "status": "pending",
    }

    response = client.post("/sync-jobs", json=payload)

    assert response.status_code == 200 
    data = response.json()
    assert data["provider_id"] == 2001
    assert data["job_type"] == "payments"
    assert data["status"] == "pending"
    assert "id" in data 

