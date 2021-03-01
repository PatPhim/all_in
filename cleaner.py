import pandas as pd
import mydate

def clean_dux(path,filename,df):
    df["Last Name"] = (df["Middle Name"] + ' ' + df["Last Name"]).str.lstrip().str.title()
    df["Company"] = df["Company"].str.upper().astype(str)
    df["First Name"] = df["First Name"].str.lstrip().str.title()
    t_l = []
    j_l = []
    nbcar_first = []
    nbcar_last = []
    nbcar_title = []
    for i in range(len(df)):
        titre = df['Title'][i].capitalize()
        jour = mydate.date_j().replace('-','/')
        nbcar_first.append(len(df['First Name'][i]))
        nbcar_last.append(len(df['Last Name'][i]))
        if " chez " in titre:
            titre = titre.split(" chez ")
            nbcar_title.append(len(titre[0]))
            t_l.append(titre[0])
            j_l.append(jour)
        elif " at " in titre:
            titre = titre.split(" at ")
            nbcar_title.append(len(titre[0]))
            t_l.append(titre[0])
            j_l.append(jour)
        else:
            t_l.append(titre)
            nbcar_title.append(len(titre))
            j_l.append(jour)
    df["Title"] = t_l
    df['date_scrap'] = j_l
    df['nbcar_first'] = nbcar_first
    df['nbcar_last'] = nbcar_last
    df['nbcar_title'] = nbcar_title
    Company=[]
    for c in df["Company"]:
        co = c.replace(' S.A.S.', '').replace(' S.A.', '').replace(' GROUP ', '').replace(' INTERNATIONAL GROUP ', '').replace('É', 'E').replace('È', 'E').replace('À', 'A').replace('Ô', "O").replace('®', "").replace('|', '').replace(':', '')
        Company.append(co)

    df = df.filter(items=["Profile", "Degree", "First Name",'nbcar_first',"Last Name",'nbcar_last',"Title",'nbcar_title',"Company","CompanyProfile","CompanyWebsite","Industry","date_scrap"]).fillna(0)
    df.insert(len(df.columns.values), "Campagne", '')

    Warning = []
    for i in range (len(df)):
        if len(df['First Name'][i]) <= 2 or len(df['Last Name'][i]) <= 2:
            Warning.append('Nom court')
        elif df["Title"][i].__contains__('alternance') or df["Title"][i].__contains__('alternant'):
            Warning.append('En alternance')
        else:
            Warning.append('OK')
        if df["CompanyWebsite"][i].startswith('https'):
            pr = df["CompanyWebsite"][i].replace('https://www.', "")

    df['Warning'] = Warning
    df.sort_values(by='Warning',ascending=True,inplace=True)
    #df= df[df['Warning'] != 'DEL']
    df.reset_index(inplace=True)
    df.drop(columns='index',inplace=True)
    df.to_csv(f"{path}CLEAN_{filename}.csv")

    print('Job done !')

def clean_phantom(file):
    df = pd.read_csv(f'data/csv/to_clean/{file}', dtype='unicode')

    df["Last Name"] = (df["Middle Name"] + ' ' + df["Last Name"]).str.lstrip()
    df["Company"] = df["Company"].str.upper().astype(str)
    df["First Name"] = df["First Name"].str.lstrip()

    Company=[]
    for c in df["Company"]:
        co = c.replace(' S.A.S.', '').replace(' S.A.', '').replace(' GROUP ', '').replace(' INTERNATIONAL GROUP ', '').replace('É', 'E').replace('È', 'E').replace('À', 'A').replace('Ô', "O").replace('®', "").replace('|', '').replace(':', '')
        Company.append(co)

    df = df.filter(items=["Profile", "Degree", "First Name",'nbcar_first',"Last Name",'nbcar_last',"Title",'nbcar_title',"Company","CompanyProfile","CompanyWebsite","Industry"]).fillna(0)
    df.insert(len(df.columns.values), "Campagne", '')

    Warning = []
    for i in range (len(df)):
        if len(df['First Name'][i]) <= 2 or len(df['Last Name'][i]) <= 2:
            Warning.append('DEL')
        elif df["Title"][i].__contains__('alterna') or df["Title"][i].__contains__('Alterna'):
            Warning.append('DEL')
        else:
            Warning.append('OK')
        if df["CompanyWebsite"][i].startswith('https'):
            pr = df["CompanyWebsite"][i].replace('https://www.', "")

    df['Warning'] = Warning
    df.sort_values(by='Warning',ascending=False,inplace=True)
    df= df[df['Warning'] != 'DEL']
    df.to_csv(f"data/csv/to_clean/output/r2.csv")

    print('Job done !')

