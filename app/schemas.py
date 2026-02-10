from pydantic import BaseModel
from typing import List, Optional


class IngestResult(BaseModel):
    inserted: int
    skipped_duplicates: int


class MetricPoint(BaseModel):
    date: str
    n_reviews: int
    avg_rating: Optional[float]
    avg_sentiment: Optional[float]
    neg_share: Optional[float]


class ProductMetrics(BaseModel):
    product_id: str
    frequency: str
    series: List[MetricPoint]
    summary: dict


class AlertPoint(BaseModel):
    date: str
    metric: str
    value: float
    zscore: float


class ProductAlerts(BaseModel):
    product_id: str
    alerts: List[AlertPoint]
