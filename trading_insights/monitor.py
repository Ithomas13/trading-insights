import time, json
from pathlib import Path
from typing import Dict

def log_metrics(metrics: Dict, path: str = "metrics/metrics.jsonl") -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    payload = {"ts": int(time.time()), **metrics}
    with open(path, "a") as f:
        f.write(json.dumps(payload) + "\n")

def basic_alerts(metrics: Dict) -> list[str]:
    alerts = []
    if metrics.get("test_r2") is not None and metrics["test_r2"] < 0.0:
        alerts.append("Warning: test R^2 < 0 suggests poor generalization.")
    return alerts
