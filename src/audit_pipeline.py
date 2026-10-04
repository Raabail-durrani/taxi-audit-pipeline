import numpy as np
import pandas as pd

df = pd.read_csv('data/data.csv')

print(df.shape)

print(df["payment"].isnull())