import pandas as pd
import glob

filenames = glob.glob('*.csv')
df_list = []
for filename in filenames:
    df = pd.read_csv(filename)
    df_list.append(df)

df = pd.concat(df_list)
df.to_csv('combined_bill.csv', index=False)