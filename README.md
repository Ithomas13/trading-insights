# Trading Insights

Modular earnings-event backtesting pipeline (EPS + VIX → OLS) with a Streamlit UI, CLI, basic metrics logging, and CI.
Includes **example data** so anyone can run it immediately without providing inputs or internet access.

## Quickstart (Streamlit UI)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
The app defaults to **sample data** shipped in `assets/`.
Uncheck the “Use sample data” box to fetch live data via Yahoo Finance.

## CLI

```bash
pip install -e .
python -m trading_insights.cli --earnings-file assets/sample_earnings.txt --ticker AAPL
```

## What’s here
- Modular stages: `ingest` → `features` → `model` → `backtest`
- Streamlit app for demo and exploration
- CLI (`ti`) for reproducibility
- Basic monitoring: JSONL metrics + simple alerts
- CI (GitHub Actions) sanity check build
- Example data in `assets/` (earnings + AAPL/VIX snapshots)
