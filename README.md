# ReviewPulse (internship prototype)

ReviewPulse is a small FastAPI microservice prototype for **English-language marketplace review analytics**.

## What it does
- Ingest reviews from a CSV file
- Store raw and derived fields in a local **SQLite** database
- Compute a transparent baseline sentiment score (lexicon-based)
- Build time-series metrics (daily/weekly): `n_reviews`, `avg_rating`, `avg_sentiment`, `neg_share`
- Detect anomalies using EWMA smoothing and z-scores of residuals

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open the interactive API docs: `http://127.0.0.1:8000/docs`

## Demo data
Generate a small synthetic dataset and a figure:
```bash
python scripts/make_sample_data.py
```

Then ingest the CSV through the API:
- POST `/ingest/file` with `reviews_sample.csv`

