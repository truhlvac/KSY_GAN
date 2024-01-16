import pandas as pd
import numpy as np

df = pd.read_csv('list_attr_celeba.txt', delim_whitespace=True, header=None, dtype='str')
df.columns = df.iloc[0]

columns_to_keep = ["nameofimage", "Male", "Young", "Eyeglasses"]
df = df[columns_to_keep]

df.loc[:, 'label'] = 0
mask = (df['Male'].values == '1') & (df['Young'].values == '1') & (df["Eyeglasses"].values == '1')
df.loc[mask, 'label'] = 0
mask = (df['Male'].values == '1') & (df['Young'].values == '1') & (df["Eyeglasses"].values == '-1')
df.loc[mask, 'label'] = 1
mask = (df['Male'].values == '1') & (df['Young'].values == '-1') & (df["Eyeglasses"].values == '1')
df.loc[mask, 'label'] = 2
mask = (df['Male'].values == '1') & (df['Young'].values == '-1') & (df["Eyeglasses"].values == '-1')
df.loc[mask, 'label'] = 3
mask = (df['Male'].values == '-1') & (df['Young'].values == '1') & (df["Eyeglasses"].values == '1')
df.loc[mask, 'label'] = 4
mask = (df['Male'].values == '-1') & (df['Young'].values == '1') & (df["Eyeglasses"].values == '-1')
df.loc[mask, 'label'] = 5
mask = (df['Male'].values == '-1') & (df['Young'].values == '-1') & (df["Eyeglasses"].values == '1')
df.loc[mask, 'label'] = 6
mask = (df['Male'].values == '-1') & (df['Young'].values == '-1') & (df["Eyeglasses"].values == '-1')
df.loc[mask, 'label'] = 7
columns_to_keep = ["nameofimage", "label"]
df = df[columns_to_keep]

df.to_csv('filtered_file.txt', index=False, sep=' ')