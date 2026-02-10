import pandas as pd


def aggregate_reviews(df: pd.DataFrame, freq: str = "D") -> pd.DataFrame:
    """Aggregate review-level data into a time series.

    Expected columns: review_id, created_at, rating, sentiment_score, sentiment_label.
    """
    if df.empty:
        return pd.DataFrame(columns=["date","n_reviews","avg_rating","neg_share","avg_sentiment"])

    d = df.copy()
    d["created_at"] = pd.to_datetime(d["created_at"])
    d = d.sort_values("created_at")
    d["date"] = d["created_at"].dt.to_period(freq).dt.start_time.dt.date.astype(str)

    g = d.groupby("date", as_index=False)
    out = g.agg(
        n_reviews=("review_id", "count"),
        avg_rating=("rating", "mean"),
        avg_sentiment=("sentiment_score", "mean"),
        neg_share=("sentiment_label", lambda s: (s == "neg").mean() if len(s) > 0 else None),
    )
    return out
