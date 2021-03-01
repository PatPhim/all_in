import pappers as pa
import pandas as pd
import pipedrive as pi

# filename = "0202-assurance-Achats _ Services Gé"
# df = pd.read_csv(f'data\csv\pappers\{filename}.csv')
# pa.unit(df,filename)

filename = "d0202-assurance-Achats _ Services Gé_r248"
df = pd.read_csv(f'data\csv\pappers\{filename}.csv')
pi.org_exist(df,filename)