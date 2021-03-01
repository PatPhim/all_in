from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import requests

rand0 = (random.randint(1, 3))

def tel(path,filename,df):
    driver = webdriver.Chrome('data/chromedriver.exe')
    driver.minimize_window()
    tel= []
    for i in range(len(df)):
        f = open("data/csv/selenium/live_res.csv", "a")
        name = (df['name_org'][i])
        list_q = [f"{name} téléphone siège social"]
        driver.get("https://www.bing.com/")
        search = driver.find_element_by_name('q')
        search.clear()
        search.send_keys(random.choice(list_q), Keys.ENTER)
        try:
            res = driver.find_element_by_class_name("b_focusTextMedium")
            res = res.text
            tel.append(str(res))
            f.write("\n#1,"+ name+','+str(res))
            print("#1,"+ name+','+str(res))
        except:
            try:
                res = driver.find_element_by_class_name("b_focusTextLarge")
                res = res.text
                tel.append(str(res))
                f.write("\n#2," + name + ',' + str(res))
                print("#2,"+ name+','+ str(res))
            except:
                try:
                    search = driver.find_element_by_name('q')
                    search.clear()
                    search.send_keys(random.choice(list_q), Keys.ENTER)
                    res = driver.find_element_by_class_name("b_focusTextLarge")
                    res = res.text
                    tel.append(str(res))
                    f.write("\n#3," + name + ',' + str(res))
                    print("#3,"+ name+','+ str(res))
                except:
                    try:
                        search = driver.find_element_by_name('q')
                        search.clear()
                        search.send_keys(random.choice(list_q), Keys.ENTER)
                        res = driver.find_element_by_class_name("b_focusTextMedium")
                        res = res.text
                        tel.append(str(res))
                        f.write("\n#4," + name + ',' + str(res))
                        print("#4,"+ name+','+ str(res))
                    except:
                        tel.append("Pas trouvé")
                        f.write("\n#5,"+ str(name)+',Pas trouvé')
                        print("#5,"+ str(name)+',Pas trouvé')

    df['tel_fixe_bot']=tel
    #df.to_csv(f'{path}tel_{filename}')
    driver.quit()
    return df

def web(path,filename,df):
    driver = webdriver.Chrome('data/chromedriver.exe')
    driver.minimize_window()
    web_l = []
    for i in range(len(df)):
        name = (df['name_org'][i])
        list_q = [f'{name}.fr {name}.com site internet']
        driver.get("https://www.bing.com/")
        search = driver.find_element_by_name('q')
        search.clear()
        search.send_keys(random.choice(list_q), Keys.ENTER)
        try:
            res = driver.find_element_by_css_selector("#b_results > li:nth-child(1) > h2 > a").get_attribute('href')
            web_l.append(res)
            print("#1,"+name+','+str(res))
        except:
            try:
                res = driver.find_element_by_css_selector("#b_results > li:nth-child(1) > div.b_title > h2 > a").get_attribute('href')
                web_l.append(res)
                print("#2,"+name+','+str(res))
            except:
                try:
                    res = driver.find_element_by_css_selector("#b_results > li:nth-child(2) > h2 > a").get_attribute('href')
                    web_l.append(res)
                    print("#3,"+name+','+str(res))
                except:
                    web_l.append("erreur")
                    print(name+',erreur')
    df['web'] = web_l
    df['ban'] = (df['web'].str.contains(pat='mozilla|google|wix|pagesjaunes|wiki|youtube|petitfute|lafabriquedunet|indeed|trustpilot|euronext|twitter|yahoo|linkedin|reverso|facebook|lexpress|linguee|entreprises.lefigaro.fr|blog|verif.com|societe.com|kompass'))
    #df.to_csv(f'{path}web_{filename}')
    driver.quit()
    return df

def linkedin_org(path,filename,df):
    driver = webdriver.Chrome('data/chromedriver.exe')
    driver.minimize_window()
    linke = []
    for i in range(len(df)):
        name = (df['name_org'][i])
        list_q = [f'site:linkedin.com/company/ "{name}"']
        #list_q = [f'page linkedin {name}']
        driver.get("https://www.bing.com/")
        search = driver.find_element_by_name('q')
        search.clear()
        search.send_keys(random.choice(list_q), Keys.ENTER)
        try:
            res = driver.find_element_by_css_selector("#b_results > li:nth-child(1) > h2 > a").get_attribute('href')
            linke.append(res)
            print("#1,"+name+','+str(res))
        except:
            try:
                res = driver.find_element_by_css_selector("#b_results > li:nth-child(1) > div.b_title > h2 > a").get_attribute('href')
                linke.append(res)
                print("#2,"+name+','+str(res))
            except:
                try:
                    res = driver.find_element_by_css_selector("#b_results > li:nth-child(2) > h2 > a").get_attribute('href')
                    linke.append(res)
                    print("#3,"+name+','+str(res))
                except:
                    linke.append("erreur")
                    print(name+',erreur')
    df['linke'] = linke
    #df.to_csv(f'{path}linke_{filename}')
    driver.quit()
    return df

def nbr_employees(path,filename,df):
    driver = webdriver.Chrome('data/chromedriver.exe')
    driver.minimize_window()
    res_l = []
    for i in range(len(df)):
        name = (df['name_org'][i])
        list_q = [f'site:linkedin.com/company {name} voir les employés']
        driver.get("https://www.bing.com/")
        search = driver.find_element_by_name('q')
        search.clear()
        search.send_keys(random.choice(list_q), Keys.ENTER)
        try:
            res = driver.find_element_by_xpath('//*[@id="b_results"]/li[1]/div/div[2]/div/ul[1]/li/div')
            res= res.text
            if "Employés" in res:
                try:
                    res = res.replace('.', ',')
                except:
                    pass
                res = res.replace('Employés : ','')
                res_l.append(res)
                print(name+','+str(res))
            else:
                res_l.append("nc")
                print(str(name) + ",nc")
        except:
            res_l.append("error")
            print(str(name) + ",error")
    df['employees'] = res_l
    df.to_csv(f'{path}linke_{filename}')
    driver.quit()
    return df

### ATTENTION VIRER LES https://
def linkedin(df):
    driver = webdriver.Chrome('data/chromedriver.exe')
    res_l = []
    driver.get(f"https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    login = driver.find_element_by_id("username")
    login.send_keys('dominique@supertripper.com')
    mdp = driver.find_element_by_id("password")
    mdp.send_keys('Super2017', Keys.ENTER)
    time.sleep(rand0)
    for i in range(len(df)):
        url = df['url'][i]
        name = df['name_org'][i]
        try:
            driver.get(f"https://{url}/")
            time.sleep(rand0)
            driver.execute_script("window.scrollTo(0, 600)")
            time.sleep(rand0)
            try:
                res = driver.find_element_by_partial_link_text("Voir les")
                res = res.text
                if "employés" in res:
                    res_l.append(res)
                    print(name+','+str(res))
                else:
                    res_l.append("nc")
                    print(name+','+"nc")
            except:
                res_l.append("null")
                print(name + ',' + "null")
        except:
            res_l.append("error")
            print(name + ',' + "error")
    df['employes'] = res_l
    driver.quit()

