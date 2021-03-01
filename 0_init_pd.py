import pandas as pd
import csv

df1 = pd.read_csv('data/csv/to_clean/ECO_ARG__1189135772.csv')
df2 = pd.read_csv('data/csv/to_clean/ECO_GOLD__904781657.csv')
df3 = pd.read_csv('data/csv/to_clean/ECO_OR__904781657.csv')
df4 = pd.read_csv('data/csv/to_clean/ECO_PLA__1198935518.csv')
df5 = pd.read_csv('data/csv/to_clean/ECO_PLATINUM__1107055866.csv')
df6 = pd.read_csv('data/csv/to_clean/ECO_SILVER___1286706239.csv')
df = pd.read_csv('data/csv/to_clean/ECO_BRONZE__1189135772.csv')

#df = pd.concat([df1,df2,df3,df4,df5,df6])
df = df.sort_values(by="url").reset_index().drop(columns='index')

l_url = []
l_do = []
for i in range (len(df)):
    x=(df['url'][i])
    l_u = x.split('|')
    l_url.append(l_u[0])
    y = x.replace('https://','').replace('http://','')
    l_d = y.split('/')
    l_do.append(l_d[0])

df['domain']=l_do
df['url']=l_url

df = df.drop_duplicates(subset='url',keep='last').drop_duplicates(subset='domain',keep='last').reset_index().drop(columns='index')

df['ban']=(df['domain'].str.contains(pat = '.be|.ch|.lu|.de|finance.orange|indeed|euronext|ecovadis|bourse|twitter|yahoo|linkedin|reverso|facebook|lexpress|boursedirect|boursier|boursorama|itespresso|jobteaser|jobtransport|linguee|silicon|youtube|qualite-references|trends.directindustry.fr|zonebourse|parisactionclimat'))

df = df[df['ban'] != True].drop_duplicates(subset='domain',keep='first')
df.to_csv('data/csv/resume_ecovadis.csv')
#print(df.head())
print(len(df))