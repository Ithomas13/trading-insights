import pandas as pd
import yfinance as yf

def fetch_stock(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        raise ValueError(f"No stock data for {ticker}")
    return df.rename_axis("Date").reset_index()[["Date","Open","High","Low","Close","Adj Close","Volume"]]

def fetch_vix(vix_symbol: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(vix_symbol, start=start, end=end, progress=False)
    if df.empty:
        raise ValueError("No VIX data")
    return df.rename_axis("Date").reset_index()[["Date", "Close"]].rename(columns={"Close":"VIX_Close"})
