import myselenium as ms
import pandas as pd
import unicodedata
path = 'data/csv/pipedrive/'
filename = "news.csv"
df = pd.read_csv(f"{path}{filename}")

#ms.nbr_employees(path,filename,df)
#ms.linkedin(df)
ms.linkedin_org(path,filename,df)

#ms.tel(path,filename,df)