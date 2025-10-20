import pandas as pd

def parse_earnings_text(text: str) -> pd.DataFrame:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d, eps = line.split(",")
            rows.append({"Earnings Date": pd.to_datetime(d.strip()), "EPS": float(eps.strip())})
        except Exception as e:
            raise ValueError(f"Bad earnings line: {line}") from e
    if not rows:
        raise ValueError("No earnings parsed")
    return pd.DataFrame(rows).sort_values("Earnings Date").reset_index(drop=True)
