import subprocess
from prefect import flow, task
from datetime import datetime

@task(log_prints=True)
def ingest_prices():
    print(f"[{datetime.now()}] Starting ingestion...")
    result = subprocess.run(
        ["python", "ingestion/fetch_prices.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"Ingestion failed: {result.stderr}")
    print("Ingestion complete.")

@task(log_prints=True)
def load_to_warehouse():
    print(f"[{datetime.now()}] Loading to DuckDB...")
    result = subprocess.run(
        ["python", "ingestion/load_duckdb.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"Load failed: {result.stderr}")
    print("Load complete.")

@task(log_prints=True)
def run_transforms():
    print(f"[{datetime.now()}] Running dbt models...")
    result = subprocess.run(
        ["dbt", "run", "--project-dir", "transforms"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise RuntimeError(f"dbt failed: {result.stderr}")
    print("Transforms complete.")

@flow(name="market-pulse-pipeline")
def market_pulse_pipeline():
    ingest_prices()
    load_to_warehouse()
    run_transforms()

if __name__ == "__main__":
    market_pulse_pipeline()
