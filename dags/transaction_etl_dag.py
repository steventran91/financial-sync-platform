import csv
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pydantic import ValidationError
from backend.app.models.create_transaction import CreateTransactionRequest
from backend.app.services.transaction_service import create_transaction
from backend.app.db.session import SessionLocal


def extract(**context):
    file_path = "/path/to/my/file.csv"

    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        context["ti"].xcom_push(key="rows", value=rows)

def transform(**context):
    rows = context["ti"].xcom_pull(key="rows", task_ids="extract")
    valid_rows = []
    bad_rows = []

    for row in rows:
        try:
            transaction = CreateTransactionRequest(
                amount= row['amount'],
                transaction_date=row['transaction_date'],
                merchant=row['merchant'],
                sync_job_id=row['sync_job_id'],
            )
            valid_rows.append(transaction.model_dump())

        except ValidationError as e:
            bad_rows.append({"row": dict(row), "error": str(e)})

    context["ti"].xcom_push(key='valid_rows', value=valid_rows)
    context["ti"].xcom_push(key='bad_rows', value=bad_rows)


def load(**context):
    rows = context["ti"].xcom_pull(key='valid_rows', task_ids="transform")
    try:
        db = SessionLocal()
        for row in rows:
            payload = CreateTransactionRequest(**row)
            create_transaction(db=db, payload=payload)
    finally:
        db.close()

with DAG(
    dag_id="transaction_etl",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )
    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )
    load_task = PythonOperator(
        task_id="load",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task



