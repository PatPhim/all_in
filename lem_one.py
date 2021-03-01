import pandas as pd
import requests
import mydate
import os

today = mydate.date_j()
yesterday = mydate.date_j1()

def extract(datodo):
    payload = {}
    headers = {'Authorization': 'Basic OjJhZmM5YTcwMjA4ZmRmNmFjOGM2MWRiOGM4N2RhNTU4'}

    ope = "https://api.lemlist.com/api/activities?user=API&type=emailsOpened"
    r_ope = requests.request("GET", ope, headers=headers, data=payload)
    j_ope = r_ope.json()
    df_ope = pd.DataFrame(j_ope)
    df_ope = df_ope.filter(
        items=['_id', 'type', 'createdAt', 'email', 'firstName', 'lastName', 'companyName', 'campaignName'])

    cli = "https://api.lemlist.com/api/activities?user=2afc9a70208fdf6ac8c61db8c87da558&type=emailsClicked"
    r_cli = requests.request("GET", cli, headers=headers, data=payload)
    j_cli = r_cli.json()
    df_cli = pd.DataFrame(j_cli)
    df_cli = df_cli.filter(
        items=['_id', 'type', 'createdAt', 'email', 'firstName', 'lastName', 'companyName', 'campaignName'])

    bou = "https://api.lemlist.com/api/activities?user=2afc9a70208fdf6ac8c61db8c87da558&type=emailsBounced"
    r_bou = requests.request("GET", bou, headers=headers, data=payload)
    j_bou = r_bou.json()
    df_bou = pd.DataFrame(j_bou)
    df_bou = df_bou.filter(
        items=['_id', 'type', 'createdAt', 'email', 'firstName', 'lastName', 'companyName', 'campaignName'])

    ###### MERGE DES CLICKED, OPENED, BOUNCED + COLONNES DATE ET HEURE

    extract_new = pd.concat([df_ope, df_cli, df_bou])
    extract_new.to_csv('data/csv/lemlist/extract_new.csv')
    try:
        extract_old = pd.read_csv('data/csv/lemlist/extract_old.csv')
        df_ext = pd.concat([extract_new, extract_old])
    except:
        print("old manquant")
        df_ext = pd.read_csv('data/csv/lemlist/extract_new.csv')

    day = []
    for j in df_ext['createdAt']:
        day.append(j[:10])
    df_ext.insert(4, 'day', day)

    hour = []
    for j in df_ext['createdAt']:
        hour.append(j[11:19])
    df_ext.insert(5, 'hour', hour)

    ###### KEEP ALL ENTREES DU JOUR
    df_res_g = df_ext.loc[df_ext['day'] == f'{datodo}']

    df_res = df_res_g.drop_duplicates(subset='_id', keep='last')
    df_res.reset_index(inplace=True)
    df_res = df_res.sort_values(by='createdAt', ascending=False)
    df_res.to_csv(f"data/csv/lemlist/extract_all_{datodo}.csv")

    ###### SCORES DES ENTREES UNIQUES
    df_res_g = df_res_g.drop_duplicates(subset='_id', keep=False)
    df_res_g.reset_index(inplace=True)
    if len(df_res_g) == 0:
        "Rien à traiter pour le moment"
        df_res_g.to_csv(f'data/csv/lemlist/last_to_score.csv')
    else:
        list_score = []
        for i in range(len(df_res_g)):
            if df_res_g['type'][i] == "emailsOpened":
                list_score.append(1)
            elif df_res_g['type'][i] == "emailsClicked":
                list_score.append(2)
            elif df_res_g['type'][i] == "emailsBounced":
                list_score.append(-1000)
        df_res_g.insert(2, 'scoring', list_score)
        df_res_g = df_res_g.groupby(['email', 'day']).sum()
        df_res_g.reset_index(inplace=True)

        df_res_g.to_csv(f'data/csv/lemlist/last_to_score.csv')

        id_pipe,id_url = [],[]
        for g in df_res_g['email']:
            api_email = f'https://api.pipedrive.com/v1/itemSearch?term={g}&start=0&api_token=a45355a6de79f4752db9de3053cbc7e663fbf1e5'
            r = requests.get(api_email)
            r.content
            j = r.json()
            try:
                get_id = j['data']['items'][0]['item']['id']
                id_pipe.append(get_id)
                id_url.append(f'https://supertripper.pipedrive.com/person/{get_id}')
            except:
                id_pipe.append("KO")
                id_url.append(f'https://supertripper.pipedrive.com/person/{get_id}')
        df_res_g['id_pipe'] = id_pipe
        df_res_g['id_url'] = id_url

        owner_id, company_id, company_name, score_pipe, label,url = [], [], [], [], [],[]
        for f in (df_res_g['id_pipe']):
            if f == "KO":
                owner_id.append("")
                score_pipe.append("")
                company_id.append("")
                company_name.append("")
                label.append("")
                pass
            elif f != "KO":
                api_id = f'https://api.pipedrive.com/v1/persons/{f}?api_token=a45355a6de79f4752db9de3053cbc7e663fbf1e5'
                r = requests.get(api_id)
                r.content
                j = r.json()
                owner_id.append(j['data']['owner_id']['id'])
                score_pipe.append(j['data']['430f02d0a955328a81b3cd5134bf0db5b56d942c'])
                company_id.append(j['data']['org_id']['value'])
                company_name.append(j['data']['org_id']['name'])
                label.append(j['data']['label'])

        df_res_g['score_pipe'] = score_pipe
        df_res_g['label'] = label
        df_res_g['owner_id'] = owner_id
        df_res_g['company_name'] = company_name
        df_res_g['company_id'] = company_id
        df_res_g = df_res_g.fillna(0)

        ns_pipe, ns_lem = [], []
        for lem_s in df_res_g['scoring']:
            lem_s = int(lem_s)
            ns_lem.append(lem_s)
        for pip_s in df_res_g['score_pipe']:
            try:
                if pip_s == None:
                    ns_pipe.append(0)
                else:
                    ns_pipe.append(int(pip_s))
            except:
                ns_pipe.append(0)
        df_res_g['score_pipe'] = ns_pipe
        df_res_g['scoring'] = ns_lem
        df_res_g['sum_score'] = df_res_g['score_pipe'] + df_res_g['scoring']

        ###### SI SCORE OK ET LABEL OK = TRAITEMENT MQL

        mql_score = []
        for sco in df_res_g['sum_score']:
            if sco == 4 or sco == 6 or sco == 8 or sco == 10 or sco == 12 or sco == 14 or sco == 16 or sco == 18 or sco == 20 or sco >= 22:
                mql_score.append('True')
            else:
                mql_score.append('False')
        df_res_g['mql_score'] = mql_score

        mql_label = []
        for so2 in df_res_g['label']:
            if so2 == 1 or so2 == 12 or so2 == 24 or so2 == 36 or so2 == 221 or so2 == 317 or so2 == 351:
                mql_label.append('False')
            else:
                mql_label.append('True')
        df_res_g['mql_label'] = mql_label

        ###### CREATION MESSAGE MQL
        log_mql = []
        for i in range(len(df_res_g)):
            if len(df_res_g) > 0 and df_res_g['mql_score'][i] == "True" and df_res_g['mql_label'][i] == "True":
                payload = '{"person_id": ' + str(df_res_g['id_pipe'][i]) + ',"org_id": ' + str(
                    df_res_g['company_id'][i]) + ',"type": "MQL",' + f'"subject": "MQL - Signaux faibles - SCORE = ' + str(
                    df_res_g['sum_score'][i]) + '","user_id": ' + str(df_res_g['owner_id'][i]) + '}'
                print(df_res_g['id_url'][i] + " : " + payload)

                log_mql.append("MQL crée pour " + df_res_g['email'][i] + ' car label = ' + str(
                    df_res_g['label'][i]) + ' & score = ' + str(df_res_g['sum_score'][i]))
            else:
                log_mql.append("")
        df_res_g["log_mql"] = log_mql

        # try:
        #     df_res_g.to_csv('data/csv/lemlist/resume.csv')
        # except:
        #     pass

        print(df_res_g)

    # return df_res_g

print(extract(yesterday))