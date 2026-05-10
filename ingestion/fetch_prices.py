import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "JPM", "BAC", "TD", "RY", "SHOP"]
RAW_DATA_DIR = "data/raw"

def fetch_prices(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    print(f"[{datetime.now()}] Fetching data for: {tickers}")
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    prices = raw["Close"].reset_index()
    prices = prices.melt(id_vars="Date", var_name="ticker", value_name="close_price")
    prices["ingested_at"] = datetime.utcnow()
    return prices

def save_locally(df: pd.DataFrame):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"{RAW_DATA_DIR}/prices_{date_str}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")

if __name__ == "__main__":
    df = fetch_prices(TICKERS)
    save_locally(df)
