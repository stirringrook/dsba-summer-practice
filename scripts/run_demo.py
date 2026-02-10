"""Small end-to-end demo without a running API server.

1) Loads sample data
2) Computes sentiment + daily aggregates
3) Flags anomalies via z-scores on EWMA residuals
"""

import pandas as pd

from app.pipeline.sentiment import sentiment_score_and_label
from app.analytics.aggregations import aggregate_reviews
from app.analytics.anomaly import detect_alerts


df = pd.read_csv("reviews_sample.csv")

df["sentiment_score"], df["sentiment_label"] = zip(*df["text"].astype(str).map(sentiment_score_and_label))

ts = aggregate_reviews(df, freq="D")
alerts = detect_alerts(ts, metric="neg_share", z_threshold=2.0)

print(ts.head(10))
print("\nAlerts:")
for a in alerts:
    print(a)
