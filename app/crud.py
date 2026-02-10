from typing import Dict, List, Tuple

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Review
from .pipeline.sentiment import sentiment_score_and_label


def init_db(engine, Base):
    Base.metadata.create_all(bind=engine)


def upsert_reviews(db: Session, review_dicts: List[Dict]) -> Tuple[int, int]:
    """Insert new reviews; skip duplicates by review_id."""
    inserted = 0
    skipped = 0

    for r in review_dicts:
        review_id = str(r.get("review_id"))
        product_id = str(r.get("product_id"))
        created_at = r.get("created_at")

        if not review_id or not product_id or created_at is None:
            continue

        exists = db.execute(select(Review.id).where(Review.review_id == review_id)).first()
        if exists:
            skipped += 1
            continue

        text = r.get("text")
        score, label = sentiment_score_and_label(text)

        obj = Review(
            review_id=review_id,
            product_id=product_id,
            seller_id=r.get("seller_id"),
            created_at=created_at,
            rating=float(r["rating"]) if r.get("rating") is not None else None,
            text=str(text) if text is not None else None,
            sentiment_score=score,
            sentiment_label=label,
        )
        db.add(obj)
        inserted += 1

    db.commit()
    return inserted, skipped


def fetch_reviews_df(db: Session, product_id: str) -> pd.DataFrame:
    rows = db.execute(select(Review).where(Review.product_id == product_id)).scalars().all()
    if not rows:
        return pd.DataFrame(columns=[
            "review_id","product_id","seller_id","created_at","rating","text","sentiment_score","sentiment_label"
        ])
    data = [
        {
            "review_id": r.review_id,
            "product_id": r.product_id,
            "seller_id": r.seller_id,
            "created_at": r.created_at,
            "rating": r.rating,
            "text": r.text,
            "sentiment_score": r.sentiment_score,
            "sentiment_label": r.sentiment_label,
        }
        for r in rows
    ]
    return pd.DataFrame(data)
