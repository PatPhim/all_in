import connect_gpread as cg
import pandas as pd

df = cg.sheet_drive("1FV4nhLDzK32b6a4rcQtgV4_iLFsoXJ_2SSIlLCSpgto")
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
df.reset_index(inplace=True)
df = df.filter(items=['Profile','SalesProfile'])
print(df)
# for i in range(len(df)):
#     print(df['Prix kilo'][i])

