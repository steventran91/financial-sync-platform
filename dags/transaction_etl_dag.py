import csv
import boto3
import os, io
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pydantic import ValidationError
from backend.app.etl.core import load_valid_rows_to_db
from backend.app.models.create_transaction import CreateTransactionRequest
from backend.app.db.session import SessionLocal
from botocore.exceptions import ClientError
from airflow.models import Variable


def extract(**context):
    bucket = Variable.get("aws_bucket_name")
    region = Variable.get("aws_region")
    access_key = Variable.get("aws_access_key_id")
    secret_key = Variable.get("aws_secret_access_key")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    try:
            response = s3.get_object(Bucket=bucket, Key="transactions.csv")
            content = response["Body"].read().decode("utf-8")
            reader = csv.DictReader(io.StringIO(content))
            rows = list(reader)
            print(f"Extracted {len(rows)} rows: {rows}")
            context["ti"].xcom_push(key="rows", value=rows)
    except ClientError as e:
        raise FileNotFoundError("File not present for sync job")


def transform(**context):
    rows = context["ti"].xcom_pull(key="rows", task_ids="extract")

    valid_rows = []
    bad_rows = []

    for row in rows:

        transaction_date = row['transaction_date']
        if 'T' not in transaction_date:
            transaction_date = transaction_date + 'T00:00:00'

        try:
            transaction = CreateTransactionRequest(
                amount= row['amount'],
                transaction_date=transaction_date,
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
        load_valid_rows_to_db(db=db, valid_rows=rows)
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



