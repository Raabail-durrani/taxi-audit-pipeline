import pandas as pd

# 1. Load the data
df = pd.read_csv('data/data.csv')
print("Shape:", df.shape)  

# ---------- 2. Fix missing payment values ----------
print("\nMissing payment before:", df['payment'].isnull().sum()) 

# Label instead of dropping: these rows still have real fare/distance data
df['payment'] = df['payment'].fillna('Unknown')

print("Missing payment after:", df['payment'].isnull().sum()) 
print("Shape after:", df.shape)                               
print(df['payment'].value_counts())                           

# ---------- 3. Missing location columns ----------
print("\nMissing values per column:")
print(df.isnull().sum())

# True/False masks: True where the value is missing
pickup_zone_missing = df['pickup_zone'].isnull()
pickup_borough_missing = df['pickup_borough'].isnull()
dropoff_zone_missing = df['dropoff_zone'].isnull()
dropoff_borough_missing = df['dropoff_borough'].isnull()

# Do zone and borough go missing on exactly the same rows?
print("\nPickup zone & borough both missing:", (pickup_zone_missing & pickup_borough_missing).sum())  
print("Dropoff zone & borough both missing:", (dropoff_zone_missing & dropoff_borough_missing).sum()) 

# ---------- 4. Zero-distance trips ----------
zero_distance = df['distance'] == 0
print("\nZero-distance trips (all):", zero_distance.sum()) 

# Rows with a missing pickup / dropoff location
missing_pickup_rows = df[pickup_zone_missing]
missing_dropoff_rows = df[dropoff_zone_missing]
print("Missing pickup rows:", missing_pickup_rows.shape)    
print("Missing dropoff rows:", missing_dropoff_rows.shape)  

print("Zero-distance among missing pickup:", (missing_pickup_rows['distance'] == 0).sum())    
print("Zero-distance among missing dropoff:", (missing_dropoff_rows['distance'] == 0).sum())  

# Share of zero-distance trips: missing vs present location
print("\nZero-distance by pickup missing:")
print(zero_distance.groupby(pickup_zone_missing).agg(['sum', 'mean']))
print("\nZero-distance by dropoff missing:")
print(zero_distance.groupby(dropoff_zone_missing).agg(['sum', 'mean']))

# ---------- 5. Flags ----------
# Neutral flag: only states what is true (the pickup location is missing)
df['pickup_missing'] = pickup_zone_missing
print("\nShape with flag:", df.shape)                       
print("Flagged pickup_missing:", df['pickup_missing'].sum()) 

# ---------- 6. Broken trips ----------
print("\nMissing pickup AND dropoff:", (pickup_zone_missing & dropoff_zone_missing).sum())  # expect 21

# Strongest warning: zero distance AND both locations missing
broken_trip = zero_distance & pickup_zone_missing & dropoff_zone_missing
print("Zero distance + both locations missing:", broken_trip.sum())  # expect 11

# Fares of these trips
print(df[broken_trip]['fare'])

distance_above_zero = df['distance'] > 0
print(df[distance_above_zero]['fare'].describe())

fare_cutoff = 10
fare_above_cutoff = df['fare'] > fare_cutoff
df['impossible_fare'] = broken_trip & fare_above_cutoff
print('Impossible-fare trips: ', df['impossible_fare'].sum())
print(df.shape)

print(df.duplicated().sum())
print(df.dtypes)

df['pickup'] = pd.to_datetime(df['pickup'])

df['dropoff'] = pd.to_datetime(df['dropoff'])

print(df.dtypes)
df['duration'] = df['dropoff'] - df['pickup']

print(df['duration'].head())

df['duration_seconds']= df['duration'].dt.seconds

print(df['duration_seconds'].head())
print(df['duration_seconds'].describe())

df['trips_below_one_minute'] = df['duration_seconds'] < 60
print(df['trips_below_one_minute'].sum())
short_trips = df[df['trips_below_one_minute']]

print(short_trips.shape)

print(short_trips[['duration_seconds', 'distance', 'fare']].sort_values('fare', ascending=False).head(10))
short_and_impossible = (df['trips_below_one_minute']) & (df['impossible_fare'])
print(short_and_impossible.sum())

short_trip_fare_cutoff = 15
fare_above_short_trip_cutoff = df['fare'] > short_trip_fare_cutoff

df['trip_below_minute_fare_above_normal']=  (df['trips_below_one_minute']) & (fare_above_short_trip_cutoff) 

print('trips that are below 1 minute and have large fares: ' , df['trip_below_minute_fare_above_normal'].sum())

df['review_needed'] = (df['pickup_missing']) | (df['impossible_fare'] ) | (df['trip_below_minute_fare_above_normal'] )

print('to be reviewed: ', df['review_needed'].sum())