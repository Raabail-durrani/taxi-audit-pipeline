import pandas as pd

# ---------- 1. Load the data ----------
df = pd.read_csv('data/data.csv')
print("Shape:", df.shape)  # expect (6433, 14)

# ---------- 2. Fix missing payment values ----------
print("\nMissing payment before:", df['payment'].isnull().sum())  # expect 44

# Label instead of dropping: these rows still have real fare/distance data
df['payment'] = df['payment'].fillna('Unknown')

print("Missing payment after:", df['payment'].isnull().sum())  # expect 0
print("Shape after:", df.shape)                                # still (6433, 14)
print(df['payment'].value_counts())                            # 'Unknown' should show 44

# ---------- 3. Missing location columns ----------
print("\nMissing values per column:")
print(df.isnull().sum())

# True/False masks: True where the value is missing
pickup_zone_missing = df['pickup_zone'].isnull()
pickup_borough_missing = df['pickup_borough'].isnull()
dropoff_zone_missing = df['dropoff_zone'].isnull()
dropoff_borough_missing = df['dropoff_borough'].isnull()

# Do zone and borough go missing on exactly the same rows?
print("\nPickup zone & borough both missing:", (pickup_zone_missing & pickup_borough_missing).sum())      # expect 26
print("Dropoff zone & borough both missing:", (dropoff_zone_missing & dropoff_borough_missing).sum())    # expect 45

# ---------- 4. Zero-distance trips ----------
zero_distance = df['distance'] == 0
print("\nZero-distance trips (all):", zero_distance.sum())  # expect 51

# Rows with a missing pickup / dropoff location
missing_pickup_rows = df[pickup_zone_missing]
missing_dropoff_rows = df[dropoff_zone_missing]
print("Missing pickup rows:", missing_pickup_rows.shape)    # expect (26, 14)
print("Missing dropoff rows:", missing_dropoff_rows.shape)  # expect (45, 14)

print("Zero-distance among missing pickup:", (missing_pickup_rows['distance'] == 0).sum())    # expect 11
print("Zero-distance among missing dropoff:", (missing_dropoff_rows['distance'] == 0).sum())  # expect 15

# Share of zero-distance trips: missing vs present location
print("\nZero-distance by pickup missing:")
print(zero_distance.groupby(pickup_zone_missing).agg(['sum', 'mean']))
print("\nZero-distance by dropoff missing:")
print(zero_distance.groupby(dropoff_zone_missing).agg(['sum', 'mean']))

# ---------- 5. Flags ----------
# Neutral flag: only states what is true (the pickup location is missing)
df['pickup_missing'] = pickup_zone_missing
print("\nShape with flag:", df.shape)                       # expect (6433, 15)
print("Flagged pickup_missing:", df['pickup_missing'].sum())  # expect 26

# ---------- 6. Broken trips ----------
print("\nMissing pickup AND dropoff:", (pickup_zone_missing & dropoff_zone_missing).sum())  # expect 21

# Strongest warning: zero distance AND both locations missing
broken_trip = zero_distance & pickup_zone_missing & dropoff_zone_missing
print("Zero distance + both locations missing:", broken_trip.sum())  # expect 11

# Fares of these trips: next step is to decide which ones are impossible
print(df[broken_trip]['fare'])

distance_above_zero = df['distance'] > 0
print(df[distance_above_zero]['fare'].describe())