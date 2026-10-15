# Taxi Trip Audit Pipeline
# Taxi Trip Audit Pipeline

A pandas project that audits and cleans a real NYC taxi trips dataset (6,433 trips, 14 columns) and flags suspicious records for review.

## Project structure
```
data/    data.csv (raw data) and cleaned_trips.csv (output)
src/     download_data.py, audit_pipeline.py
```

## How to run
Run both commands from the project root:
```
pip install -r requirements.txt
python src/download_data.py
python src/audit_pipeline.py
```

## What the pipeline does
- **Audit:** missing values, duplicate rows, and how the location gaps overlap.
- **Clean:** missing `payment` values are labeled `Unknown` (rows are kept); `pickup` and `dropoff` are converted to datetime.
- **Features:** trip duration in seconds.
- **Flags:**
  - `pickup_missing`: the pickup location is missing.
  - `impossible_fare`: zero distance, both locations missing, and a fare above 10.
  - `trip_below_minute_fare_above_normal`: a trip under 60 seconds with a fare above 15.
  - `review_needed`: any of the three flags above.
  - `distance_outlier`: distance above the IQR upper limit (6.555).
- **Insights:** average fare by pickup borough, average tip by payment type, trips per hour of day.
- **Export:** cleaned data saved to `data/cleaned_trips.csv`; the raw file is never changed.

## Key findings
- No duplicate rows.
- 44 trips have no payment type. All show a tip of 0, and cash tips are never recorded in this data.
- Missing zone and borough values always occur together (26 pickup, 45 dropoff).
- Missing pickup locations are linked to odd trips: 42% of them have zero distance, against 0.6% of the rest.
- 38 trips are flagged for review.
- 734 trips (about 11%) are distance outliers, but fare and duration rise with distance, so they look like real long trips and are kept.

## Tools
Python, pandas