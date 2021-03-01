import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

def push_drive(key_file,df):
    print("> Connect to Gdrive...")
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name('data/creds.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet_key = key_file
    wks_name = 'Feuille 2'
    d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    print('push Ok')

def sheet_drive(key_file):
    gc = gspread.service_account(filename='data/creds.json')
    sh = gc.open_by_key(key_file)
    worksheet = sh.worksheet('Feuille 1')
    all = worksheet.get_all_values()
    return worksheet