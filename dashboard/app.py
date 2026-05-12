import streamlit as st
import duckdb
import pandas as pd

DB_PATH = "data/market_pulse.db"

st.set_page_config(page_title="Market Pulse", layout="wide")
st.title("📈 Market Pulse")
st.caption("Real-time stock pipeline | yfinance → DuckDB → dbt → Streamlit")

@st.cache_data
def load_data():
    con = duckdb.connect(DB_PATH)
    df = con.execute("""
        SELECT date, ticker, close_price, ma_7d, ma_30d, pct_change_daily
        FROM fct_daily_metrics
        ORDER BY ticker, date
    """).df()
    con.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Filters")
tickers = sorted(df["ticker"].unique())
selected = st.sidebar.multiselect("Select Tickers", tickers, default=["AAPL", "SHOP", "NVDA"])

if not selected:
    st.warning("Select at least one ticker.")
    st.stop()

filtered = df[df["ticker"].isin(selected)]

# Price chart
st.subheader("Close Price + Moving Averages")
for ticker in selected:
    t = filtered[filtered["ticker"] == ticker].set_index("date")
    st.write(f"**{ticker}**")
    st.line_chart(t[["close_price", "ma_7d", "ma_30d"]])

# Daily % change
st.subheader("Daily % Change")
pct = filtered.groupby(["date", "ticker"])["pct_change_daily"].mean().unstack("ticker")
st.line_chart(pct)

# Summary table
st.subheader("Summary Statistics")
summary = filtered.groupby("ticker").agg(
    latest_price=("close_price", "last"),
    avg_price=("close_price", "mean"),
    avg_daily_return=("pct_change_daily", "mean"),
    max_price=("close_price", "max"),
    min_price=("close_price", "min")
).round(2)
st.dataframe(summary)
