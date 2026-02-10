from typing import List, Dict

import numpy as np
import pandas as pd


def ewma(series: pd.Series, alpha: float = 0.25) -> pd.Series:
    return series.ewm(alpha=alpha, adjust=False).mean()


def zscore_residuals(series: pd.Series, smooth_alpha: float = 0.25, eps: float = 1e-9) -> pd.DataFrame:
    s = series.astype(float)
    m = ewma(s, alpha=smooth_alpha)
    r = s - m

    sigma = r.std(ddof=1) if r.notna().sum() > 2 else (r.abs().mean() + eps)
    z = r / (sigma + eps)

    return pd.DataFrame({"value": s, "smooth": m, "resid": r, "zscore": z})


def detect_alerts(ts_df: pd.DataFrame, metric: str, z_threshold: float = 2.0) -> List[Dict]:
    """Flag points with |z| >= z_threshold on EWMA residuals."""
    if ts_df.empty or metric not in ts_df.columns:
        return []

    x = ts_df[metric].copy()
    if x.isna().all():
        return []

    zdf = zscore_residuals(x.ffill().bfill())

    alerts: List[Dict] = []
    for i, row in zdf.iterrows():
        if abs(row["zscore"]) >= z_threshold:
            alerts.append(
                {
                    "date": ts_df.loc[i, "date"],
                    "metric": metric,
                    "value": float(row["value"]),
                    "zscore": float(row["zscore"]),
                }
            )
    return alerts
