import pandas as pd

# 1. Load the data
df = pd.read_csv('data/data.csv')
print("Shape:", df.shape)  

# 2. Check missing values before cleaning
print("\nMissing payment before:", df['payment'].isnull().sum())  # expect 44

# 3. Fill missing payment values with a label (keeps the rows and their real data)
df['payment'] = df['payment'].fillna('Unknown')

# 4. Verify the cleaning worked
print("\nMissing payment after:", df['payment'].isnull().sum())  # expect 0
print("Shape after:", df.shape)                                  # still (6433, 14)
print("\nPayment value counts:")
print(df['payment'].value_counts())  # 'Unknown' should show 44

print(df.isnull().sum())
#checking if both columns have missing values at exact same row
mask_o = df['pickup_zone'].isnull()

mask_t = df['pickup_borough'].isnull()

print((mask_o & mask_t).sum())

#checking if both columns have missing values at exact same row
mask_od = df['dropoff_zone'].isnull()
mask_td = df['dropoff_borough'].isnull()
print(((mask_od) & (mask_td)).sum())

#filtering pickup columns

#df['pickup_zone'] = df.groupby('pickup_zone')[['pickup_zone' , 'dropoff_zone', 'distance' , 'fare' , 'total']]
#print(df['pickup_zone'])

missing_pickup = df[mask_o]
print(missing_pickup.shape)

print(missing_pickup[['pickup', 'dropoff', 'distance', 'fare', 'total']])

mask_distance = df['distance']== 0
print(mask_distance.sum())

print((missing_pickup['distance']==0).sum())
mask_full = df['distance'] == 0

#aggregates = df.groupby(mask_full)['distance'].agg(['sum()' , 'mean()'])
print(mask_full.groupby(mask_o).agg(['sum' , 'mean']))
df['pickup_missing'] = mask_o
print(df.shape)

print(df['pickup_missing'].sum())

#handle dropoff rows

missing_dropoff = df[mask_od]
print(missing_dropoff.shape)

print(missing_dropoff[['distance', 'fare', 'total'] ])
mask_dropoff =df['distance'] == 0 
print(mask_dropoff.sum())
print((missing_dropoff['distance']==0).sum())