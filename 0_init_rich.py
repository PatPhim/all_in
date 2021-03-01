import pandas as pd
from configparser import ConfigParser
import requests
import csv

config = ConfigParser()
config.read('config.ini')

API_PAPPERS = (config['DEFAULT']["api_pappers"])
API_PIPE = (config['DEFAULT']["api_pipedrive"])

filename = "new.csv"
path = "data/csv/pipedrive/"
df = pd.read_csv(f'{path}{filename}')

def org_exist(df,path,filename):
    id_pipe_l,name_pipe_l = [],[]
    for i in range(len(df)):
        name = df['name_org'][i].replace(' ', '%20')
        #url1 = f"https://api.pipedrive.com/v1/itemSearch?term={name}&item_types=organization&start=0&api_token={API_PIPE}"
        url1 = f"https://api.pipedrive.com/v1/organizations/search?term={name}&fields=name&start=0&api_token={API_PIPE}"
        headers = {
            "Accept": "application/json"
        }
        r1 = requests.request("GET", url1, headers=headers)
        j1 = r1.json()
        try:
            id=(j1['data']['items'][0]['item']['id'])
            name=(j1['data']['items'][0]['item']['name'])
            print(id,name)
            name_pipe_l.append(name)
            id_pipe_l.append(id)
        except:
            id = "nc_pipe"
            name = df['name_org'][i]
            print(id,name)
            name_pipe_l.append("nc_pipe")
            id_pipe_l.append("nc_pipe")

    df['id_pipe'] = id_pipe_l
    df['name_pipe'] = name_pipe_l
    return df


def siren(df,path,filename):
    siren_pipe_l = []
    visibility = []
    web_l = []
    tel_l = []
    tel_bot_l = []
    for i in range(len(df)):
        id_org = df['id_pipe'][i]
        url = f"https://api.pipedrive.com/v1/organizations/{id_org}?api_token={API_PIPE}"

        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url, headers=headers)
        j = r.json()
        try:
            siren =(j['data']['3b521f404b4f7591c92d632ad4add17966918b86'])
            print(siren)
            url1  = f"https://api.pipedrive.com/v1/itemSearch?term={siren}&item_types=organization&start=0&api_token={API_PIPE}"
            r = requests.request("GET", url1, headers=headers)
            j = r.json()
            res = len(j['data']['items'])
            if siren is not None:
                siren_pipe_l.append(siren)
                visibility.append(res)
            elif siren is None:
                siren_pipe_l.append("nc_pipe")
                visibility.append(res)
        except:
            siren_pipe_l.append("nc_pipe")
            visibility.append("0")
        try:
            web = (j['data']['360494af75bc55c665444bbed752ce49d26abd9b'])
            web_l.append(web)
        except:
            web_l.append("-")
        try:
            tel = (j['data']['4a6f7bb4a06646ef6744398a0c195417942d50c6'])
            tel_l.append(tel)
        except:
            tel_l.append("-")
        try:
            tel_bot = (j['data']['653035742d219ff22aad06669b78a1d9d31790d2'])
            tel_bot_l.append(tel_bot)
        except:
            tel_bot_l.append("-")


    df['siren_pipe'] = siren_pipe_l
    df['siren_pipe_use'] = visibility
    df['web'] = web_l
    df['tel'] = tel_l
    df['tel_bot'] = tel_bot_l

    return df


def unit(df,path,filename):
    siren_l = []
    name_l = []
    cessation_l = []
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
                name_l.append(ent[0]['nom_entreprise'])
                cessation_l.append(ent[0]['entreprise_cessee'])
                print(ent[0]['nom_entreprise']+','+ent[0]['siren'])
            except:
                siren_l.append('nc_paps')
                name_l.append('nc_paps')
                cessation_l.append('nc_paps')
                print(name+','+'nc_paps')
        except:
            print(name +", error")
            siren_l.append('error')
            name_l.append('error')
            cessation_l.append.append('error')
    cess=[]
    for i in cessation_l:
        i = str(i).replace(str(0),"Active").replace(str(1),"Cessée")
        cess.append(i)
    df["name_pappers"] = name_l
    df["siren_pappers"] = siren_l
    df["cessation_pappers"] = cess
    return df

def warning(df,path,filename):
    mess_pipe = []
    mess_use = []
    for i in range(len(df)):
        siren_pipe = df['siren_pipe'][i]
        siren_pap = df['siren_pappers'][i]
        id_pipe = df['id_pipe'][i]
        if siren_pipe == siren_pap:
            mess_pipe.append('Versus_Ok')
        elif siren_pipe == "nc_pipe" and siren_pap == "nc_paps":
            mess_pipe.append('No_result !')
        elif siren_pipe == "nc_pipe" and siren_pap != "nc_paps" and id_pipe == "nc_pipe":
            mess_pipe.append('Ok_for_import')
        elif siren_pipe == "nc_pipe" and siren_pap != "nc_paps" and id_pipe != "nc_pipe":
            mess_pipe.append('Drop_Ko')
        else:
            mess_pipe.append('No_match !')
        siren_pipe_use = df['siren_pipe_use'][i]
        if int(siren_pipe_use) > 1:
            mess_use.append(f'{siren_pipe_use}x !')
        elif int(siren_pipe_use) == 1:
            mess_use.append(f'{siren_pipe_use}x')
        elif int(siren_pipe_use) == 0:
            mess_use.append(f'0')

    df['pipe_vs_paps_siren'] = mess_pipe
    df['num_views_siren_pipe'] = mess_use
    return df

df = org_exist(df,path,filename)
df = siren(df,path,filename)
df = unit(df,path,filename)
df = warning(df,path,filename)

df = df.drop(columns="siren_pipe_use")
df.to_csv(f'{path}res_{filename}')

print(df)