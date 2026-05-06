import io
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

def test_create_transaction_invalid_amount():
    sync = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending", 
    }

    response = client.post("/sync-jobs", json=sync)
    assert response.status_code == 200

    txn = {
        "amount": -25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
    }

    response = client.post("/transactions", json=txn)
    assert response.status_code == 422

def test_create_transaction_invalid_date():
    sync = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending", 
    }

    response = client.post("/sync-jobs", json=sync)
    assert response.status_code == 200

    txn = {
        "amount": 25,
        "transaction_date": "2027-04-30T00:00:00",
        "merchant": "Kith",
    }

    response = client.post("/transactions", json=txn)
    assert response.status_code == 422


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
    
    txn_id_response = client.get(f"/transactions/{txn_id}")
    assert txn_id_response.status_code == 200
    txn_data = txn_id_response.json()
    assert txn_data["amount"] == "25"
    assert txn_data["transaction_date"] == "2026-04-30T00:00:00"
    assert txn_data["merchant"] == "Kith"
    assert txn_data["sync_job_id"] == sync_data["id"]

def test_get_transaction_by_filter():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }

    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200
    sync_data = response.json()

    txn = {
        "amount": 25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
        "sync_job_id": sync_data["id"],
    }

    response = client.post("/transactions", json=txn)
    assert response.status_code == 200
    txn_data = response.json()
    txn_status = txn_data["status"]
    txn_merchant = txn_data["merchant"]
    txn_job_id = txn_data["sync_job_id"]
    

    response = client.get(f"/transactions?status={txn_status}")
    assert response.status_code == 200
    data = response.json()
    statuses = {status["status"] for status in data}
    assert txn_status in statuses
    merchants = {merchant["merchant"] for merchant in data}
    assert txn_merchant in merchants
    ids = {sync_job["sync_job_id"] for sync_job in data}
    assert txn_job_id in ids

def test_patch_transaction():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }

    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200
    sync_data = response.json()

    txn = {
        "amount": 25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
        "sync_job_id": sync_data["id"],
    }

    response = client.post("/transactions", json=txn)
    assert response.status_code == 200
    txn_data = response.json()
    txn_id = txn_data["id"]
    assert txn_data["status"] == "pending"

    txn_update = {
        "status": "completed",
    }

    response = client.patch(f"/transactions/{txn_id}", json=txn_update)
    assert response.status_code == 200
    txn_update_data = response.json()
    assert txn_update_data["status"] == "completed"
    assert txn_update_data["id"] == txn_id


def test_update_transaction_not_found():
    txn_update = {
        "status": "completed",
    }

    response = client.patch(f"/transactions/{99}", json=txn_update)
    assert response.status_code == 404

def test_delete_transaction():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }

    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200
    sync_data = response.json()

    txn = {
        "amount": 25,
        "transaction_date": "2026-04-30T00:00:00",
        "merchant": "Kith",
        "sync_job_id": sync_data["id"],
    }

    response = client.post("/transactions", json=txn)
    assert response.status_code == 200
    txn_data = response.json()
    txn_id = txn_data["id"]

    response = client.delete(f"/transactions/{txn_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Transaction deleted"}
    


def test_delete_transaction_not_found():
    response = client.delete(f"/transactions/{99}")
    assert response.status_code == 404


def test_transaction_not_found():
    response = client.get(f"/transactions/{99999}")

    assert response.status_code == 404 
    assert response.json() == {"detail": "Transaction not found"}

def test_upload_valid_csv():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }
    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200
    sync_job_id = response.json()["id"]

    csv_content = f"transaction_date,amount,merchant,sync_job_id\n2026-04-01,250.00,Nike,{sync_job_id}\n"
    file = ("test.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    response = client.post("/transactions/upload", files={"file": file})
    assert response.status_code == 200

    rows_processed = response.json()["rows_processed"]
    errors = response.json()["errors"]
    assert rows_processed == 1
    assert errors == []

def test_upload_with_bad_rows():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }
    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200
    sync_job_id = response.json()["id"]

    csv_content = (
        f"transaction_date,amount,merchant,sync_job_id\n"
        f"2027-04-01,250.00,Nike,{sync_job_id}\n"
        f"2026-04-01,-250.00,Nike,{sync_job_id}\n"
        f"2026-04-01,0.00,Nike,{sync_job_id}\n"
    )
    file = ("test.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    response = client.post("/transactions/upload", files={"file": file})
    assert response.status_code == 200
    data = response.json()
    assert len(data["errors"]) == 3
    assert data["errors"][0]["row"]["transaction_date"] == "2027-04-01"
    assert data["errors"][1]["row"]["amount"] == "-250.00"
    assert data["errors"][2]["row"]["amount"] == "0.00"


def test_upload_empty_file():
    sync_job = {
        "provider_id": 100,
        "job_type": "payments",
        "status": "pending",
    }
    response = client.post("/sync-jobs", json=sync_job)
    assert response.status_code == 200


    csv_content = (
        f"transaction_date,amount,merchant,sync_job_id\n"
    )
    file = ("test.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")
    response = client.post("/transactions/upload", files={"file": file})
    assert response.status_code == 200
    data = response.json()
    rows_processed = data["rows_processed"]
    errors = data["errors"]
    assert rows_processed == 0
    assert errors == []

    



