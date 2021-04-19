
import ccxt
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'service.json'
SPREADSHEET_ID = '1PJUh6kNjcUjVTpHzBFixIM0f1EZpOGKiDOhd5h7xYeQ'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

tokens = [ 'BTC', 'ETH', 'ADA', 'LINK', 'XRP' , 'DOT']


def getThirtyDayCloses(sheet, token):
    print("executing getThirtyDayCloses for : ", token)
    startDay = datetime.date.today() - datetime.timedelta(days=31)
    startDayString = startDay.strftime("%Y-%m-%d") + " 00:00:00"
    binance = ccxt.binance ({ 'enableRateLimit': True })
    symbol = token + "/USDT"
    ohlcv_data = binance.fetch_ohlcv(symbol, '1d', binance.parse8601(startDayString), 30)

    update_list = []
    for x in range(30, 0, -1):
        date = datetime.date.today() - datetime.timedelta(days=x)
        formattedDate = date.strftime('%d/%m/%Y')
        entry = [formattedDate, ohlcv_data[30 - x][4]]
        update_list.append(entry)
    
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=token+"!A3",
                                    valueInputOption="USER_ENTERED", body={"values":update_list}).execute()


def updateDailyCloses(sheet, token, count):
    print("executing updateDailyCloses for : ", token)
    lastDateCell = token + "!A" + str(count + 2)
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=lastDateCell).execute()
    lastUpdateString = result.get('values', [])[0][0]
    nextUpdateDate = datetime.datetime.strptime(lastUpdateString, '%d-%m-%Y').date() + datetime.timedelta(days=1)
    daysToUpdate = (datetime.date.today() - nextUpdateDate).days
    print("Days to update for ", token, ": ", daysToUpdate)

    binance = ccxt.binance ({ 'enableRateLimit': True })
    startDayString = nextUpdateDate.strftime("%Y-%m-%d") + " 00:00:00"
    symbol = token + "/USDT"
    ohlcv_data = binance.fetch_ohlcv(symbol, '1d', binance.parse8601(startDayString), daysToUpdate)

    update_list = []
    for x in range(daysToUpdate):
        formattedDate = nextUpdateDate.strftime('%d/%m/%Y')
        nextUpdateDate = nextUpdateDate + datetime.timedelta(days=1)
        entry = [formattedDate, ohlcv_data[x][4]]
        update_list.append(entry)

    nextDateCell = token + "!A" + str(count + 3)
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=nextDateCell,
                                    valueInputOption="USER_ENTERED", body={"values":update_list}).execute()

    print(ohlcv_data)


def updateTokenSheet(sheet, token):
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range=token+"!A1").execute()
    count = int(result.get('values', [])[0][0])
    print(token, ' count: ', count)
    if count < 30:
        getThirtyDayCloses(sheet, token)
    else:
        updateDailyCloses(sheet, token, count)


def main():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    for token in tokens:
        updateTokenSheet(sheet, token)

if __name__ == '__main__':
    main()