import pandas as pd
from datetime import timedelta

def _nearest_before(df: pd.DataFrame, dt: pd.Timestamp) -> pd.Timestamp | None:
    s = df[df["Date"] < dt]["Date"]
    return s.iloc[-1] if not s.empty else None

def _nearest_after(df: pd.DataFrame, dt: pd.Timestamp) -> pd.Timestamp | None:
    s = df[df["Date"] > dt]["Date"]
    return s.iloc[0] if not s.empty else None

def compute_price_changes(stock: pd.DataFrame, earnings: pd.DataFrame) -> pd.DataFrame:
    out = []
    for _, row in earnings.iterrows():
        edate = pd.to_datetime(row["Earnings Date"])
        before = _nearest_before(stock, edate - timedelta(days=0))
        after = _nearest_after(stock, edate + timedelta(days=0))
        if before is None or after is None:
            continue
        before_px = stock.loc[stock["Date"] == before, "Close"].iloc[0]
        after_px  = stock.loc[stock["Date"] == after, "Close"].iloc[0]
        chg = (after_px - before_px) / before_px * 100.0
        out.append({"Earnings Date": edate, "price_change_pct": chg, "eps": row["EPS"]})
    return pd.DataFrame(out)

def attach_vix(df_changes: pd.DataFrame, vix: pd.DataFrame) -> pd.DataFrame:
    vix_sorted = vix.sort_values("Date")
    levels = []
    for dt in df_changes["Earnings Date"]:
        sub = vix_sorted[vix_sorted["Date"] <= dt]
        levels.append(sub["VIX_Close"].iloc[-1] if not sub.empty else None)
    out = df_changes.copy()
    out["vix_level"] = levels
    return out.dropna(subset=["vix_level"])
