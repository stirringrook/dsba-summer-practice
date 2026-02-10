from sqlalchemy import Column, Integer, String, Float, DateTime, Index

from .db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, index=True, nullable=False)
    product_id = Column(String, index=True, nullable=False)
    seller_id = Column(String, index=True, nullable=True)

    created_at = Column(DateTime, index=True, nullable=False)
    rating = Column(Float, nullable=True)
    text = Column(String, nullable=True)

    # Derived fields
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)  # pos/neu/neg


Index("ix_reviews_product_time", Review.product_id, Review.created_at)
