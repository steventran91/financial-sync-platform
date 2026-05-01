from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200 
    assert response.json() == {"status": "ok"}

def test_get_sync_jobs():
    create_payload = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }
    create_resp = client.post("/sync-jobs", json=create_payload)
    assert create_resp.status_code == 200
    new_id = create_resp.json()["id"]

    response = client.get("/sync-jobs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    ids = {job["id"] for job in data}
    assert new_id in ids

def test_get_sync_job_by_id():
    create_payload = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "completed",
    }
    create_resp = client.post("/sync-jobs", json=create_payload)
    assert create_resp.status_code == 200
    job_id = create_resp.json()["id"]

    response = client.get(f"/sync-jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
    assert data["job_type"] == "payments"
    assert data["status"] == "completed"

def test_sync_job_id_not_found():
    response = client.get(f"/sync-jobs/{99999}")

    assert response.status_code == 404 
    assert response.json() == {"detail": "Sync job not found"}

def test_get_sync_job_with_filter():
    payload = {
        "provider_id": 100,
        "job_type": "refunds",
        "status": "pending",
    }
    create_resp = client.post("/sync-jobs", json=payload)
    assert create_resp.status_code == 200
    status = create_resp.json()["status"]
    job_id = create_resp.json()["id"]

    response = client.get(f"/sync-jobs?status={status}")
    assert response.status_code == 200
    data = response.json()
    ids = {job["id"] for job in data}
    assert job_id in ids
    statuses = {status["status"] for status in data}
    assert status in statuses

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


def test_create_transaction():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }

    sync_job_response = client.post("/sync-jobs", json=sync_job)
    assert sync_job_response.status_code == 200
    sync_job_data = sync_job_response.json()

    transaction_payload = {
        "amount": 25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
        "sync_job_id": sync_job_data["id"],
    }

    transaction_response = client.post("/transactions", json=transaction_payload)
    assert transaction_response.status_code == 200
    transaction_data = transaction_response.json()

    assert transaction_data["amount"] == "25"
    assert transaction_data["transaction_date"] == "2026-04-30T00:00:00"
    assert transaction_data["merchant"] == "Kith"
    assert transaction_data["sync_job_id"] == sync_job_data["id"]

def test_get_transaction_by_id():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }

    sync_response = client.post("/sync-jobs", json=sync_job)
    assert sync_response.status_code == 200
    sync_data = sync_response.json()

    txn = {
        "amount": 25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
        "sync_job_id": sync_data["id"],
    }

    txn_response = client.post("/transactions", json=txn)
    assert txn_response.status_code == 200
    txn_id = txn_response.json()["id"]
    
    txn_id_response = client.get(f"transactions/{txn_id}")
    assert txn_id_response.status_code == 200
    txn_data = txn_id_response.json()
    assert txn_data["amount"] == "25"
    assert txn_data["transaction_date"] == "2026-04-30T00:00:00"
    assert txn_data["merchant"] == "Kith"
    assert txn_data["sync_job_id"] == sync_data["id"]




