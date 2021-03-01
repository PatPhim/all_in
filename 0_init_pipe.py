import pipedrive as pi
import pandas as pd

filename = "pipe.csv"
path = "data/csv/pipedrive/"
df = pd.read_csv(f'{path}{filename}')
pi.detail_pers(df,path,filename)