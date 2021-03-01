import requests
from configparser import ConfigParser
import pandas as pd
from math import *

config = ConfigParser()
config.read('config.ini')

API_PAPPERS = (config['DEFAULT']["api_pappers"])

def conv(conv):
    url = f"https://api.pappers.fr/v1/recherche?api_token={API_PAPPERS}&entreprise_cessee=false&convention_collective={conv}&resultat_min=1000000&resultat_max=100000000000&tranche_effectif_min=22&tranche_effectif_max=41&par_page=1000&page=1"
    headers = {
        "Accept": "application/json"
    }
    r = requests.request("GET", url, headers=headers)
    j = r.json()
    ent = j['entreprises']

    total = (j['total_entreprises'])
    res = (len(ent))
    n_page = floor(total/res)

    siren=[]
    nom=[]
    code_postal=[]
    ville=[]
    code_naf=[]
    libelle_code_naf=[]
    domaine_act=[]
    nom_conv=[]
    code_conv=[]
    autres_conv=[]
    ca=[]
    resultat=[]
    effectif=[]
    for i in range (len(ent)):
        siren.append(ent[i]['siren'])
        nom.append(ent[i]['nom_entreprise'])
        code_postal.append(ent[i]['siege']['code_postal'])
        ville.append(int(ent[i]['siege']['ville']))
        effectif.append(ent[i]['effectif'])
        code_naf.append(ent[i]['code_naf'])
        libelle_code_naf.append(ent[i]['libelle_code_naf'])
        domaine_act.append(ent[i]['domaine_activite'])
        nom_conv.append(ent[i]['conventions_collectives'][0]['nom'])
        code_conv.append(ent[i]['conventions_collectives'][0]['idcc'])
        autres_conv.append(len(ent[i]['conventions_collectives']))
        ca.append(int(ent[i]['chiffre_affaires']))
        resultat.append(int(ent[i]['resultat']))

    df = pd.DataFrame(list(zip(siren,nom,code_postal,ville,effectif,code_naf,libelle_code_naf,nom_conv,code_conv,autres_conv,domaine_act,ca,resultat)),columns =['siren', 'nom','code_postal','ville','effectif','code_naf','libelle_code_naf','nom_conv','code_conv','autres_conv','domaine_act','ca','resultat'])
    df.to_csv(f'data/csv/pappers/c{conv}_r{total}.csv')
    return df
def dept(dp_search):
    url = f"https://api.pappers.fr/v1/recherche?api_token={API_PAPPERS}&entreprise_cessee=false&departement={dp_search}&resultat_min=1000&tranche_effectif_min=22&tranche_effectif_max=41&par_page=5000&page=1"

    headers = {
        "Accept": "application/json"
    }
    r = requests.request("GET", url, headers=headers)
    j = r.json()
    ent = j['entreprises']

    total = (j['total_entreprises'])

    siren=[]
    nom=[]
    code_postal=[]
    ville=[]
    code_naf=[]
    libelle_code_naf=[]
    ca=[]
    resultat=[]
    effectif=[]
    annee_finances=[]
    dept=[]
    for i in range (len(ent)):
        siren.append(ent[i]['siren'])
        nom.append(ent[i]['nom_entreprise'])
        code_postal.append(int(ent[i]['siege']['code_postal']))
        ville.append(ent[i]['siege']['ville'])
        effectif.append(ent[i]['effectif'])
        code_naf.append(ent[i]['code_naf'])
        libelle_code_naf.append(ent[i]['libelle_code_naf'])
        ca.append(int(ent[i]['chiffre_affaires']))
        resultat.append((ent[i]['resultat']))
        annee_finances.append(int(ent[i]['annee_finances']))
        dept.append(dp_search)

    df = pd.DataFrame(list(zip(siren,nom,code_postal,ville,effectif,code_naf,libelle_code_naf,ca,resultat,annee_finances,dept)),columns =['siren', 'nom','code_postal','ville','effectif','code_naf','libelle_code_naf','ca','resultat','annee_finances','dept'])
    df.to_csv(f'data/csv/pappers/d{dp_search}_r{total}.csv')
    return df

def unit(df,path,filename):
    siren_l = []
    name_l = []
    for i in range(len(df)):
        name = df['name_org'][i]
        try:
            url = f"https://api.pappers.fr/v1/recherche?api_token={API_PAPPERS}&nom_entreprise={name}"

            headers = {
                "Accept": "application/json"
            }
            r = requests.request("GET", url, headers=headers)
            j = r.json()
            ent = j['entreprises']
            try:
                siren_l.append(ent[0]['siren'])
                name_l.append(name)
                print(ent[0]['nom_entreprise']+','+ent[0]['siren'])
            except:
                siren_l.append('error')
                name_l.append(name)
                print(name+','+'error')
        except:
            print(name +", PAS TROUVE")
            siren_l.append('error')
            name_l.append(name)

    #df = pd.DataFrame(list(zip(name_l,siren_l)),columns =['name','siren'])
    df["siren_pappers"] = siren_l
    df["name_pappers"] = name_l
    #df.to_csv(f'{path}res_{filename}')
    return df