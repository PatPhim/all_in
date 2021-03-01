import pandas as pd
import re

filename = "regex.csv"
path = 'data/csv/to_clean/'
df = pd.read_csv(f'{path}{filename}')

l_url_s = []
l_name_s = []
for i in range (len(df)):
    name = df['name_org'][i]
    url = df['url'][i]
    if '/company/' in df['url'][i]:
        name_s = name.replace('.','').replace('-','').replace("[",'').replace("]",'').replace("'",'').lower()[0:3]
        url_s = url.split('company/')[1].replace('.','').replace('-','').replace('%20','').replace('%C3%A9','é').replace('%27','').lower()
        l_name_s.append(name_s)
        l_url_s.append(url_s)
    else:
        l_name_s.append("error")
        l_url_s.append("error")
df['name_s'] = l_name_s
df['url_s'] = l_url_s

print(df)



    #     x = re.search(r"name_s", r"url_s")
    #     if x:
    #         print(name+', Match')
    #         ddd.append('Match')
    #     else:
    #         print(name+', KO')
    #         ddd.append('KO')
    # else:
    #     print(name + ', ERROR')
    #     ddd.append('ERROR')





