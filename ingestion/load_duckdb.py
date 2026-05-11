import duckdb
import pandas as pd
import os
from datetime import datetime

DB_PATH = "data/market_pulse.db"
RAW_DATA_DIR = "data/raw"

def get_latest_csv() -> str:
    files = sorted([
        f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")
    ])
    if not files:
        raise FileNotFoundError("No CSV files found in data/raw/")
    return os.path.join(RAW_DATA_DIR, files[-1])

def load_to_duckdb(csv_path: str):
    df = pd.read_csv(csv_path, header=0, names=["date", "ticker", "close_price", "ingested_at"])
    df["close_price"] = df["close_price"].round(4)

    con = duckdb.connect(DB_PATH)

    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_prices (
            date DATE,
            ticker VARCHAR,
            close_price DOUBLE,
            ingested_at TIMESTAMP
        )
    """)

    con.execute("""
        DELETE FROM raw_prices
        WHERE ingested_at::DATE = CURRENT_DATE
    """)

    con.execute("INSERT INTO raw_prices SELECT * FROM df")

    row_count = con.execute("SELECT COUNT(*) FROM raw_prices").fetchone()[0]
    print(f"[{datetime.now()}] Loaded {len(df)} rows. Total in DB: {row_count}")
    con.close()

if __name__ == "__main__":
    csv_path = get_latest_csv()
    print(f"Loading: {csv_path}")
    load_to_duckdb(csv_path)
