from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from .db import engine, Base, get_db
from .crud import init_db, upsert_reviews, fetch_reviews_df
from .schemas import IngestResult, ProductMetrics, ProductAlerts, AlertPoint, MetricPoint
from .analytics.aggregations import aggregate_reviews
from .analytics.anomaly import detect_alerts

app = FastAPI(title="ReviewPulse", version="0.1.0")


@app.on_event("startup")
def on_startup():
    init_db(engine, Base)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest/file", response_model=IngestResult)
async def ingest_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Upload a .csv file")

    content = await file.read()
    df = pd.read_csv(BytesIO(content))

    required = {"review_id", "product_id", "created_at"}
    if not required.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"CSV must contain columns: {sorted(required)}")

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df = df.dropna(subset=["created_at", "review_id", "product_id"])

    reviews = df.to_dict(orient="records")
    inserted, skipped = upsert_reviews(db, reviews)

    return IngestResult(inserted=inserted, skipped_duplicates=skipped)


@app.get("/product/{product_id}/metrics", response_model=ProductMetrics)
def product_metrics(product_id: str, freq: str = "D", db: Session = Depends(get_db)):
    df = fetch_reviews_df(db, product_id)
    ts = aggregate_reviews(df, freq=freq)

    series = [MetricPoint(**row) for row in ts.to_dict(orient="records")]

    summary = {
        "n_reviews_total": int(df.shape[0]),
        "avg_rating_total": float(df["rating"].mean()) if df.shape[0] and df["rating"].notna().any() else None,
        "neg_share_total": float((df["sentiment_label"] == "neg").mean()) if df.shape[0] else None,
    }
    return ProductMetrics(product_id=product_id, frequency=freq, series=series, summary=summary)


@app.get("/product/{product_id}/alerts", response_model=ProductAlerts)
def product_alerts(product_id: str, freq: str = "D", z_threshold: float = 2.0, db: Session = Depends(get_db)):
    df = fetch_reviews_df(db, product_id)
    ts = aggregate_reviews(df, freq=freq)

    alerts = []
    for metric in ["neg_share", "avg_rating", "avg_sentiment"]:
        alerts.extend(detect_alerts(ts, metric=metric, z_threshold=z_threshold))

    alerts_sorted = sorted(alerts, key=lambda x: (x["date"], x["metric"]))
    return ProductAlerts(product_id=product_id, alerts=[AlertPoint(**a) for a in alerts_sorted])
