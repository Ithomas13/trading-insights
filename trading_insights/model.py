import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from .config import TrainConfig

class OLSModel:
    def __init__(self):
        self.model = None
        self.columns = None

    def fit(self, df: pd.DataFrame, cfg: TrainConfig) -> dict:
        X = df[list(cfg.feature_cols)]
        X = sm.add_constant(X)
        y = df[cfg.target_col]
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=cfg.test_size, random_state=cfg.random_state)
        m = sm.OLS(y_tr, X_tr).fit()
        self.model = m
        self.columns = list(X.columns)
        y_pred = m.predict(X_te)
        ss_res = ((y_te - y_pred)**2).sum()
        ss_tot = ((y_te - y_te.mean())**2).sum()
        test_r2 = float(1 - ss_res/ss_tot) if ss_tot != 0 else None
        return {
            "train_r2": float(m.rsquared),
            "test_r2": test_r2,
            "n_train": int(len(X_tr)),
            "n_test": int(len(X_te)),
            "coef": {c: float(p) for c, p in zip(self.columns, m.params)}
        }

    def predict(self, features: pd.DataFrame) -> pd.Series:
        if self.model is None or self.columns is None:
            raise RuntimeError("Model not fit")
        X = sm.add_constant(features)
        X = X.reindex(columns=self.columns, fill_value=1.0)
        return self.model.predict(X)

    def save(self, path: str) -> None:
        import pathlib
        pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"model": self.model, "columns": self.columns}, f)

    def load(self, path: str) -> None:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        self.model = obj["model"]
        self.columns = obj["columns"]
