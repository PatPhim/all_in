import requests
import pandas as pd
import mydate
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

API_SOC = (config['DEFAULT']["api_societeinfo"])
#API_SOC = "DEMO"

def solde():
    url = "https://societeinfo.com/app/rest/api/v2/apikeyinfo.json?key={}".format(API_SOC)
    r = requests.request("GET", url)
    j = r.json()

    # consumedCredits = str(j['result']["consumedCredits"])+" consumedCredits"
    # maxCredits = str(j['result']["maxCredits"])+" maxCredits"
    # extraCredits = str(j['result']["extraCredits"])+" extraCredits"
    # consumedExtraCredits = str(j['result']["consumedExtraCredits"])+" consumedExtraCredits"
    totalAvailableCredits = str(j['result']["totalAvailableCredits"])+" totalAvailableCredits"

    return totalAvailableCredits

def siren(siren):
    url = "https://societeinfo.com/app/rest/api/v2/company.json/{}?key={}".format(siren,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j

def search(name):
    url = "https://societeinfo.com/app/rest/api/v2/company.json?name={}&key={}".format(name,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j

def search2(name,postal_code):
    url = "https://societeinfo.com/app/rest/api/v2/company.json?name={}&postal_code={}&key={}".format(name,postal_code,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j

def contact(siren):
    url = "https://societeinfo.com/app/rest/api/v2/contacts.json/{}?key={}".format(siren,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j

def enrich(first,last,orga,status_email):
    url = "https://societeinfo.com/app/rest/api/v2/contacts.json?name={}&first_name={}&last_name={}&email_test_result={}&stat&key={}".format(first,last,orga,status_email,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j

def role(societe,role):
    url = "https://societeinfo.com/app/rest/api/v2/contacts.json?name={}&contact_role_query={}&key={}".format(societe,role,API_SOC)
    r = requests.request("GET", url)
    j = r.json()
    return j
