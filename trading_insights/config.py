from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class DataConfig:
    ticker: str = "AAPL"
    start: str = "2018-01-01"
    end: str = date.today().isoformat()
    vix_symbol: str = "^VIX"

@dataclass(frozen=True)
class TrainConfig:
    target_col: str = "price_change_pct"
    feature_cols: tuple = ("eps", "vix_level")
    test_size: float = 0.25
    random_state: int = 42
