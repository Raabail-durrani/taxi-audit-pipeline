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

