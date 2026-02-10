import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

PRODUCTS = ["P-1001", "P-1002"]
SELLERS = ["S-01", "S-02"]

POS_TEXTS = [
    "Great quality, works perfectly, fast delivery.",
    "Excellent product, very satisfied, recommend!",
    "Nice item, good packaging, happy with purchase.",
]
NEG_TEXTS = [
    "Bad quality, arrived damaged, disappointed.",
    "Terrible experience, not working, refund requested.",
    "Awful, looks fake, waste of money.",
]
NEU_TEXTS = [
    "Received the item. Packaging ok.",
    "Delivery on time. Product as described.",
    "Normal quality for the price.",
]


def gen(n_days: int = 15, n_per_day: int = 20) -> pd.DataFrame:
    start = datetime(2026, 1, 26)
    rows = []
    rid = 0

    for d in range(n_days):
        day = start + timedelta(days=d)
        for _ in range(n_per_day):
            rid += 1
            product_id = random.choice(PRODUCTS)
            seller_id = random.choice(SELLERS)

            # Controlled anomaly: burst of negative reviews around days 10-12 for P-1001
            if 10 <= d <= 12 and product_id == "P-1001":
                p_neg = 0.85
            else:
                p_neg = 0.18

            u = random.random()
            if u < p_neg:
                text = random.choice(NEG_TEXTS)
                rating = random.choice([1, 2])
            elif u < p_neg + 0.55:
                text = random.choice(POS_TEXTS)
                rating = random.choice([4, 5])
            else:
                text = random.choice(NEU_TEXTS)
                rating = random.choice([3, 4])

            ts = day + timedelta(minutes=random.randint(0, 60 * 23))
            rows.append(
                {
                    "review_id": f"R-{rid:06d}",
                    "product_id": product_id,
                    "seller_id": seller_id,
                    "rating": float(rating),
                    "text": text,
                    "created_at": ts.isoformat(),
                }
            )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = gen()
    df.to_csv("reviews_sample.csv", index=False)
    print("Saved reviews_sample.csv with", len(df), "rows")
