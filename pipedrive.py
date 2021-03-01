import requests
from configparser import ConfigParser
import pandas as pd

config = ConfigParser()
config.read('config.ini')

API_PIPE = (config['DEFAULT']["api_pipedrive"])

def filter_person(id):
    url = f"https://api.pipedrive.com/v1/persons?filter_id={id}&start=0&limit=500&api_token={API_PIPE}"

    headers = {
        "Accept": "application/json"
    }
    r = requests.request("GET", url, headers=headers)
    j = r.json()
    return j['data']

def filter_orgas(id):
    url = f"https://api.pipedrive.com/v1/organizations?filter_id={id}&limit=500&start=0&api_token={API_PIPE}"

    headers = {
        "Accept": "application/json"
    }
    r = requests.request("GET", url, headers=headers)
    j = r.json()
    f_orgas = j['data']
    name,id_org,label,address_street_number,address_route,address_locality,address_admin_area_level_1,address_country,address_postal_code,tel_standard,linkedin,naf,siteweb,name_naf,last_ca = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    for i in range (len(f_orgas)):
        id_org.append(f_orgas[i]['id'])
        label.append(f_orgas[i]['label'])
        address_street_number.append(f_orgas[i]['address_street_number'])
        address_route.append(f_orgas[i]['address_route'])
        address_locality.append(f_orgas[i]['address_locality'])
        address_admin_area_level_1.append(f_orgas[i]['address_admin_area_level_1'])
        address_country.append(f_orgas[i]['address_country'])
        address_postal_code.append(f_orgas[i]['address_postal_code'])
        tel_standard.append(f_orgas[i]['4a6f7bb4a06646ef6744398a0c195417942d50c6'])
        linkedin.append(f_orgas[i]['fb6466618ff2c3a36af3bd24c07bcab64eb730de'])
        name.append(f_orgas[i]['name'])
        naf.append(f_orgas[i]['92b6ec0a1f00769091fb70b37267ce52377ecfa8'])
        siteweb.append(f_orgas[i]['360494af75bc55c665444bbed752ce49d26abd9b'])
        name_naf.append(f_orgas[i]['2f79932ae88bd7bdb90cc2f1b467812661746c15'])
        last_ca.append(f_orgas[i]['4f951d344b09f3db7934d0a74c1fb6b78b3d7ab4'])
    df = pd.DataFrame()
    df["name_org"]=name
    df["id_org"]=id_org
    df["address_street_number"]=address_street_number
    df["address_route"]=address_route
    df["address_locality"]=address_locality
    df["address_admin_area_level_1"]=address_admin_area_level_1
    df["address_country"]=address_country
    df["address_postal_code"]=address_postal_code
    df["tel_standard"]=tel_standard
    df["linkedin"]=linkedin
    df["label"]=label
    df["naf"]=naf
    df["siteweb"]=siteweb
    df["name_naf"]=name_naf
    df["last_ca"]=last_ca
    #timestamp = mydate.dh_light()
    #df.to_csv(f'data/csv/pipedrive/{timestamp}_filtre{id}.csv')
    #print(f_orgas[0]['name'])
    return df

def update_orga(id,name,tel):
    url = "https://api.pipedrive.com/v1/organizations/{}?api_token={}".format(id,API_PIPE)

    payload = {
        "name" : name,
        '653035742d219ff22aad06669b78a1d9d31790d2': tel,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.request("PUT", url, headers=headers, data=payload)
    j = r.json()
    print("Import statut : " + str(j['success']))

def remove_dupe_siren():
        df = pd.read_csv('data/csv/removedupe.csv')

        ser_website = pd.Series(df["Organization - Site Web"])
        ser_website = ser_website.str.replace("https://", '').str.replace("http://", '').str.replace(r'"', '')
        ser_website = ser_website.str.split("/").str[0]
        ser_website = ser_website.str.split("|").str[0]
        ser_website = ser_website.str.split(",").str[0]
        df["Organization - Site Web"] = ser_website
        ser_address = pd.Series(df["Organization - Address"])
        ser_address = ser_address.str.replace("Ã©", 'é').str.replace("ÃŽ", 'I').str.replace(r'Ã´', 'o').str.replace(r'â€™', "'").str.replace(r'Ã¯', "ï")
        df["Organization - Address"] = ser_address

        ser_name = pd.Series(df["Organization - Name"])
        ser_name = ser_name.str.upper()
        df["Organization - Name"] = ser_name


        #### Fill cell by "*_Null#"
        fill_siren = []
        cpt = 0
        for i in df["Organization - Numéro Siren"]:
            if type(i) is float:
                cpt += 1
                fill_siren.append("Siren_Null_" + str(cpt))
            else:
                fill_siren.append(i)
        df["Siren_new"] = fill_siren
        df.sort_values(by='Organization - Numéro Siren',ascending=True,inplace=True)

        ser_sirnew = pd.Series(df["Siren_new"])

        siren_all = ser_sirnew.duplicated(keep=False)
        df["dupe_siren"] = siren_all
        siren_one = ser_sirnew.duplicated(keep="first")
        df["first_dupe_siren"] = siren_one
        df = df[(df['dupe_siren']==True)]
        df.reset_index(inplace=True)
        merge =[]
        for i in range(len(df)):
            if df['first_dupe_siren'][i]==True and df['first_dupe_siren'][i-1]==True and df['first_dupe_siren'][i-2]==False:
                merge.append(df['Organization - ID'][i-2])
            elif df['first_dupe_siren'][i]==True and df['first_dupe_siren'][i-1]==True and df['first_dupe_siren'][i-2]==True and df['first_dupe_siren'][i-3]==False:
                merge.append(df['Organization - ID'][i-3])
            elif df['first_dupe_siren'][i]==True and df['first_dupe_siren'][i-1]==True and df['first_dupe_siren'][i-2]==True and df['first_dupe_siren'][i-3]==True and df['first_dupe_siren'][i-4]==False:
                merge.append(df['Organization - ID'][i-4])
            elif df['first_dupe_siren'][i]==True and df['first_dupe_siren'][i-1]==True and df['first_dupe_siren'][i-2]==True and df['first_dupe_siren'][i-3]==True and df['first_dupe_siren'][i-4]==True and df['first_dupe_siren'][i-5]==False:
                merge.append(df['Organization - ID'][i-5])
            elif df['first_dupe_siren'][i]==True:
                merge.append(df['Organization - ID'][i-1])
            else:
                merge.append(df['Organization - ID'][i])
        df['Merge Id']=merge
        df.to_csv('data/csv/pipedrive/removedupe2.csv')
        return df

def remove_dupe_website():
    df = pd.read_csv('data/csv/remove_dup.csv')

    ser_website = pd.Series(df["Organization - Site Web"])
    ser_website = ser_website.str.replace("https://", '').str.replace("http://", '').str.replace(r'"', '')
    ser_website = ser_website.str.split("/").str[0]
    ser_website = ser_website.str.split("|").str[0]
    ser_website = ser_website.str.split(",").str[0]
    df["Organization - Site Web"] = ser_website
    ser_address = pd.Series(df["Organization - Address"])
    ser_address = ser_address.str.replace("Ã©", 'é').str.replace("ÃŽ", 'I').str.replace(r'Ã´', 'o').str.replace(r'â€™',
                                                                                                                "'").str.replace(
        r'Ã¯', "ï")
    df["Organization - Address"] = ser_address

    ser_name = pd.Series(df["Organization - Name"])
    ser_name = ser_name.str.upper()
    df["Organization - Name"] = ser_name

    #### Fill cell by "*_Null#"
    fill_siren = []
    cpt = 0
    for i in df["Organization - Site Web"]:
        if type(i) is float:
            cpt += 1
            fill_siren.append("web_Null_" + str(cpt))
        else:
            fill_siren.append(i)
    df["web_new"] = fill_siren
    df.sort_values(by='Organization - Site Web', ascending=True, inplace=True)

    ser_webnew = pd.Series(df["web_new"])

    web_all = ser_webnew.duplicated(keep=False)
    df["dupe_web"] = web_all
    web_one = ser_webnew.duplicated(keep="first")
    df["first_dupe_web"] = web_one
    df = df[(df['dupe_web'] == True)]
    df.reset_index(inplace=True)
    merge = []
    for i in range(len(df)):
        if df['first_dupe_web'][i] == True and df['first_dupe_web'][i - 1] == True and df['first_dupe_web'][i - 2] == False:
            merge.append(df['Organization - ID'][i - 2])
        elif df['first_dupe_web'][i] == True and df['first_dupe_web'][i - 1] == True and df['first_dupe_web'][
            i - 2] == True and df['first_dupe_web'][i - 3] == False:
            merge.append(df['Organization - ID'][i - 3])
        elif df['first_dupe_web'][i] == True and df['first_dupe_web'][i - 1] == True and df['first_dupe_web'][
            i - 2] == True and df['first_dupe_web'][i - 3] == True and df['first_dupe_web'][i - 4] == False:
            merge.append(df['Organization - ID'][i - 4])
        elif df['first_dupe_web'][i] == True and df['first_dupe_web'][i - 1] == True and df['first_dupe_web'][
            i - 2] == True and df['first_dupe_web'][i - 3] == True and df['first_dupe_web'][i - 4] == True and \
                df['first_dupe_web'][i - 5] == False:
            merge.append(df['Organization - ID'][i - 5])
        elif df['first_dupe_web'][i] == True:
            merge.append(df['Organization - ID'][i - 1])
        else:
            merge.append(df['Organization - ID'][i])
    df['Merge Id'] = merge
    df.to_csv('data/csv/pipedrive/removedupe2.csv')
    return df

def merge_orga(id,mer_id):
    url = f"https://api.pipedrive.com/v1/organizations/{id}/merge?api_token={API_PIPE}"
    payload = {
        "merge_with_id": mer_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.request("POST", url, headers=headers, data=payload)
    j = r.json()
    print(j)

def org_exist(df,path,filename):
    res = []
    for i in range(len(df)):
        siren = df['siren_pappers'][i]
        url1 = f"https://api.pipedrive.com/v1/itemSearch?term={siren}&item_types=organization&fields=custom_fields&start=0&api_token={API_PIPE}"
        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url1, headers=headers)
        j = r.json()
        try:
            id=(j['data']['items'][0]['item']['id'])
            res.append(id)
        except:
            print("Not in Pipe")
            res.append("Not in Pipe")

    df['Siren_in_pipe?'] = res
    df.to_csv(f'{path}exist_{filename}.csv')

def get_all_orgas():
    cpt = 0
    for i in range (0,100):
        while True:
            cpt += 1
            url = f"https://api.pipedrive.com/v1/organizations?filter_id=625&start={i}&api_token=a45355a6de79f4752db9de3053cbc7e663fbf1e5"
            headers = {
                "Accept": "application/json"
            }
            r = requests.request("GET", url, headers=headers)
            j = r.json()
            print(cpt, len(j['data']))

## GET ID PERSON with name & company
def items_pers(df,filename):
    res = []
    for i in range(len(df)):
        name = df['name'][i].replace(" ","%20")
        id_org = df['id_pipe'][i]
        url1 = f"https://api.pipedrive.com/v1/persons/search?term={name}&organization_id={id_org}&start=0&api_token={API_PIPE}"

        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url1, headers=headers)
        j = r.json()
        try:
            id=(j['data']['items'][0]['item']['id'])
            res.append(id)
            print(id)
        except:
            print("Not in Pipe")
            res.append("Not in Pipe")

    df['id_pipe'] = res
    df.to_csv(f'data/csv/pipedrive/id_{filename}')

def items_org(df,filename):
    res = []
    for i in range(len(df)):
        name = df['Company'][i]
        url = f"https://api.pipedrive.com/v1/itemSearch?term={name}&item_types=organization&start=0&api_token={API_PIPE}"

        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url, headers=headers)
        j = r.json()
        try:
            id=(j['data']['items'][0]['item']['id'])
            res.append(id)
            print(id)
        except:
            print("Not in Pipe")
            res.append("Not in Pipe")

    df['id_pipe'] = res
    df.to_csv(f'data/csv/pipedrive/id_{filename}')

# WITH ID ORG > GET TEL, TEL_BOT
def detail_org(df,path,filename):
    l_tel_bot = []
    l_tel= []
    for i in range(len(df)):
        id_org = df['id_org'][i]
        url = f"https://api.pipedrive.com/v1/organizations/{id_org}?api_token={API_PIPE}"

        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url, headers=headers)
        j = r.json()

        try:
            tel_bot =(j['data']['653035742d219ff22aad06669b78a1d9d31790d2'])
            l_tel_bot.append(tel_bot)
            print(tel_bot)
        except:
            print("Not in Pipe")
            l_tel_bot.append("Not in Pipe")

        try:
            tel =(j['data']['4a6f7bb4a06646ef6744398a0c195417942d50c6'])
            l_tel.append(tel)
            print(tel)
        except:
            print("Not in Pipe")
            l_tel.append("Not in Pipe")

    df['tel'] = l_tel
    df['tel_bot'] = l_tel_bot
    df.to_csv(f'{path}id_{filename}')

#FROM DETAILS PERSON GET DETAILS ORG
def detail_pers(df,path,filename):
    id_org_l = []
    tel_org_l = []
    name_org_l = []
    name_pers_l = []
    for i in range(len(df)):
        id_pers = df['id_pers'][i]
        url = f"https://api.pipedrive.com/v1/persons/{id_pers}?api_token={API_PIPE}"
        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url, headers=headers)
        j = r.json()

        try:
            org_id =(j['data']['org_id']["value"])
            name_pers =(j['data']['name'])
            id_org_l.append(org_id)
            name_pers_l.append(name_pers)
            print(org_id)
        except:
            print("Not in Pipe")
            id_org_l.append("Not in Pipe")
            name_pers_l.append("Not in Pipe")


        url1 = f"https://api.pipedrive.com/v1/organizations/{org_id}?api_token={API_PIPE}"

        headers = {
            "Accept": "application/json"
        }
        r = requests.request("GET", url1, headers=headers)
        j = r.json()
        # try:
        tel = (j['data']['653035742d219ff22aad06669b78a1d9d31790d2'])
        name = (j['data']['name'])
        tel_org_l.append(tel)
        name_org_l.append(name)
        #     print(id)
        # except:
        #     print("Not in Pipe")
        #     tel_org_l.append("Not in Pipe")
        #     name_org_l.append("Not in Pipe")

    df['id_org'] = id_org_l
    df['name_pers'] = name_pers_l
    df['name_org'] = name_org_l
    df['tel_org'] = tel_org_l
    df.to_csv(f'{path}tel_bot{filename}')
    return df

def update_person(id,name,campagne):
    url = "https://api.pipedrive.com/v1/persons/{}?api_token={}".format(id,API_PIPE)

    payload = {
        "id":id,
        "name": name,
        'a0731819b7dfaee89669d6eaaaeee5b64dece1db': campagne,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.request("PUT", url, headers=headers, data=payload)
    j = r.json()
    print("Import statut : " + str(j['success']))

def note(id,date):
    url = 'https://api.pipedrive.com/v1/notes?org_id={}&start=0&start_date={}&api_token={}'.format(id,date,API_PIPE)

    r = requests.request("GET", url)
    j = r.json()
    todo = []

    try:
        len_data = (len(j['data']))
        if len_data == 1:
            print(str(id)+",OK")
            todo.append(str(id)+",OK")
        elif len_data > 1 and (j['data'][0]['content']) == (j['data'][1]['content']):
            id_note1 = (j['data'][0]['id'])
            id_note2 = (j['data'][1]['id'])
            res = (str(id)+",Note en doublon"+","+str(id_note1)+","+str(id_note2))
            todo.append(res)
            print(res)
        # else:
        #     print(str(id)+",+2 notes différentes")
        #     todo.append(str(id)+",+2 notes différentes")
    except:
        print(str(id) + ",ERROR")
        todo.append(str(id) + ",ERROR")
    return todo

def del_note(id):
    url = 'https://api.pipedrive.com/v1/notes/{}?api_token={}'.format(id, API_PIPE)
    r = requests.request('DELETE',url)
    j = r.json()
    print(id, j)

def del_activity(id):
    url = 'https://api.pipedrive.com/v1/activities/{}?api_token={}'.format(id, API_PIPE)
    r = requests.request('DELETE',url)
    j = r.json()
    print(id, j)