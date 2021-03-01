import cleaner as cl
import pandas as pd
import mydate

filename = "dux-soup-visit-data2021-01-26_14h42"
path = 'data/csv/scrap/'
df = pd.read_csv(f'{path}{filename}.csv',dtype='unicode')

cl.clean_dux(path,filename,df)

