# Market Pulse 📈

An end-to-end financial data pipeline that ingests real stock market data, transforms it, and surfaces insights through a live dashboard.

## Architecture

yfinance API → CSV (raw) → DuckDB → dbt models → Prefect Orchestration → Streamlit Dashboard

## What It Does

- **Ingests** daily closing prices for 10 tickers (AAPL, MSFT, GOOGL, AMZN, NVDA, JPM, BAC, TD, RY, SHOP) from Yahoo Finance
- **Stores** raw data in DuckDB, a local analytical warehouse
- **Transforms** raw prices into meaningful metrics using dbt:
  - 7-day and 30-day moving averages
  - Daily percentage change
- **Orchestrates** the full pipeline (ingest → load → transform) as a single Prefect flow
- **Visualizes** results in an interactive Streamlit dashboard

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | yfinance, Python |
| Storage | DuckDB |
| Transformation | dbt-core |
| Orchestration | Prefect |
| Dashboard | Streamlit |
| CI | GitHub Actions (coming soon) |
| Containerization | Docker (coming soon) |

## Project Structure

```
market-pulse/
├── ingestion/
│   ├── fetch_prices.py         # Pull data from Yahoo Finance
│   └── load_duckdb.py          # Load CSV into DuckDB warehouse
├── transforms/
│   └── models/
│       ├── stg_prices.sql      # Staging: clean raw prices
│       └── fct_daily_metrics.sql  # Facts: moving averages, % change
├── pipeline/
│   └── flow.py                 # Prefect flow (full pipeline)
├── dashboard/
│   └── app.py                  # Streamlit dashboard
├── data/
│   └── raw/                    # Raw CSV files (gitignored)
└── requirements.txt
```

## How To Run

```bash
# 1. Clone and set up environment
git clone https://github.com/27av03/market-pulse.git
cd market-pulse
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Run the full pipeline
python pipeline/flow.py

# 3. Launch the dashboard
streamlit run dashboard/app.py
```

## Why This Project

I'm a CS + BBA student at Wilfrid Laurier University who sits at the intersection of technology and finance, and I built Market Pulse to reflect exactly that.

Most student projects demonstrate one thing: that you can code. Market Pulse demonstrates something different. It shows that I understand how data moves through a real system, why each layer exists, and how technical decisions connect to business outcomes. That's the mindset I bring from combining a computer science degree with a business degree.

The domain wasn't chosen randomly. Financial data is live, messy, and consequential. The companies I want to work for in fintech, banking, and data-driven technology run on pipelines like this one. Building Market Pulse was my way of speaking their language before walking through the door.
