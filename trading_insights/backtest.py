import pandas as pd
from .model import OLSModel
from .config import TrainConfig
from .features import compute_price_changes, attach_vix

def build_dataset(stock_df, earnings_df, vix_df) -> pd.DataFrame:
    chg = compute_price_changes(stock_df, earnings_df)
    data = attach_vix(chg, vix_df)
    return data.sort_values("Earnings Date").reset_index(drop=True)

def train_and_backtest(dataset: pd.DataFrame, cfg: TrainConfig) -> tuple[OLSModel, dict]:
    model = OLSModel()
    metrics = model.fit(dataset, cfg)
    return model, metrics
