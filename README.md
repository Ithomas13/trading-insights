# Trading Insights
**Modular ML Backtesting Application for Earnings Predictions**

[![Streamlit](https://img.shields.io/badge/Launch%20App-Streamlit-brightgreen?logo=streamlit)](https://trading-insights.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview
**Trading Insights** is an end-to-end event-driven backtesting platform that analyzes historical **EPS (Earnings per Share)** and **VIX volatility** data to estimate stock price reactions following earnings releases.

The project features:
- A clean **Streamlit dashboard** for interactive prediction and visualization  
- A modular **OLS regression pipeline** for backtesting event-based strategies  
- **Offline sample data** for instant demonstrations without API keys  
- **Logging, CLI support, and Dockerized setup** for scalable deployment  

---

## Quickstart

Clone the repository:
```bash
git clone https://github.com/ithomas13/trading-insights.git
cd trading-insights
```

Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the Streamlit app:
```bash
python -m streamlit run streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Example Output

This project includes recent **AAPL** earnings data to allow for offline use.  
Example output:

| Prediction | Recommendation | Model |  
|-------------|----------------|--------|  
| **+2.14 %** | *Consider Buying Before Earnings* | OLS (EPS + VIX → Price Change) |

![Demo Screenshot](assets/demo.png)

---

## Architecture
```
trading-insights/
├── trading_insights/
│   ├── ingest.py          # Fetches stock and VIX data
│   ├── earnings.py        # Parses EPS input
│   ├── backtest.py        # OLS regression and metrics
│   ├── monitor.py         # Metrics logging
│   └── cli.py             # Command-line interface
├── assets/
│   ├── sample_earnings.txt
│   ├── sample_stock_AAPL.csv
│   ├── sample_vix.csv
│   └── demo.png
├── streamlit_app.py       # Streamlit user interface
├── requirements.txt
└── Dockerfile
```

---

## CLI Usage

Run the backtest directly from the terminal:
```bash
python -m trading_insights.cli --earnings-file assets/sample_earnings.txt --ticker AAPL
```

---

## Technology Stack
- **Python 3.11+**
- **Streamlit** – interactive visualization
- **pandas / NumPy** – data analysis
- **scikit-learn / statsmodels** – regression modeling
- **Altair** – charting
- **Docker** – deployment containerization

---

## License
This project is released under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

---

## Author
**Isaiah Thomas (ithomas13)**  
GitHub: [ithomas13](https://github.com/ithomas13)  
Email: isaiahththomas@gmail.com
