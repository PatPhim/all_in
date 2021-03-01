import pipedrive as pi
import mydate
import pandas as pd
import connect_gpread as cg

def daily(id_per,id_or):
    f = pi.filter_person(id_per)
    qualif,mql,prospect,echec = [],[],[],[]
    for i in range(0,len(f)):
        if f[i]['label'] == 317:
            qualif.append(f[i]['name'])
        elif f[i]['label'] == 220:
            mql.append(f[i]['name'])
        elif f[i]['label'] == 36:
            prospect.append(f[i]['name'])
        elif f[i]['label'] == 334:
            echec.append(f[i]['name'])

    r_q = (len(qualif))
    r_m = (len(mql))
    r_p = (len(prospect))
    r_e = (len(echec))
    date = (mydate.date_j())

    f = pi.filter_orgas(id_or)
    org_pro = []
    client = []
    for i in range(0, len(f)):
        if f['label'][i] == 145:
            org_pro.append(f['name_org'][i])
        elif f['label'][i] == 146:
            client.append(f['name_org'][i])
    r_op = (len(org_pro))
    r_cl = (len(client))

    r = {'date':date,'mql':r_m,'qualif_sdr':r_q,'people_prospect':r_p,'echec':r_e,'client':r_cl,'org_prospect':r_op,}
    print(r)

    worksheet = cg.sheet_drive("1K-woke8IZNlw6lp2IMGqnBhRS5z75zlMlV-ueFPe-As")

    df = pd.DataFrame(worksheet.get_all_records())
    df = df.append(r,ignore_index=True)

    try :
        df = df.drop_duplicates(subset="date",keep='last')
    except:
        pass
    df = df.sort_values(by='date',ascending=False).reset_index().filter(items=['date','mql','qualif_sdr','people_prospect','echec','client','org_prospect'])
    print(df)

    cg.push_drive("1K-woke8IZNlw6lp2IMGqnBhRS5z75zlMlV-ueFPe-As",df)
    return r

daily(549,552)

#https://www.integromat.com/scenario/1878842/edit