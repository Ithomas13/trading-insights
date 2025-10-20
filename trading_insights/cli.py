import argparse
import pandas as pd
from .config import DataConfig, TrainConfig
from .ingest import fetch_stock, fetch_vix
from .earnings import parse_earnings_text
from .backtest import build_dataset, train_and_backtest
from .monitor import log_metrics, basic_alerts

def main():
    p = argparse.ArgumentParser("Trading Insights CLI")
    p.add_argument("--ticker", default="AAPL")
    p.add_argument("--start", default="2018-01-01")
    p.add_argument("--end")
    p.add_argument("--vix", default="^VIX")
    p.add_argument("--earnings-file", required=True, help="Path to text file with lines: YYYY-MM-DD, EPS")
    p.add_argument("--model-out", default="artifacts/ols.pkl")
    args = p.parse_args()

    dcfg = DataConfig(ticker=args.ticker, start=args.start, end=(args.end or DataConfig().end), vix_symbol=args.vix)

    with open(args.earnings_file, "r") as f:
        earnings_text = f.read()
    earnings_df = parse_earnings_text(earnings_text)

    stock_df = fetch_stock(dcfg.ticker, dcfg.start, dcfg.end)
    vix_df   = fetch_vix(dcfg.vix_symbol, dcfg.start, dcfg.end)

    dataset = build_dataset(stock_df, earnings_df, vix_df)
    model, metrics = train_and_backtest(dataset, TrainConfig())

    model.save(args.model_out)
    log_metrics(metrics)
    for a in basic_alerts(metrics):
        print(a)

    last_row = dataset.iloc[-1:][["eps","vix_level"]]
    pred = model.predict(last_row)[0]
    print(f"Latest inferred post-earnings move prediction: {pred:.2f}%")

if __name__ == "__main__":
    main()
