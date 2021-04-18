
import ccxt
import datetime
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

back24h = datetime.datetime.now() - datetime.timedelta(hours=24)
back24hFormatted = back24h.strftime("%Y-%m-%d %H:%M:00")

back7d = datetime.datetime.now() - datetime.timedelta(days=7)
back7dFormatted = back7d.strftime("%Y-%m-%d %H:%M:00")

update_list = []
binance = ccxt.binance ({ 'enableRateLimit': True })
for token in tokens:
    print("Getting price data for ", token)
    symbol = token + "/USDT"
    ticker = binance.fetch_ticker(symbol)
    tokenPriceUSDT = (float(ticker['ask']) + float(ticker['bid'])) / 2

    ohlcv_data_24h = binance.fetch_ohlcv(symbol, '1m', binance.parse8601(back24hFormatted), 1)
    change24h = (tokenPriceUSDT / ohlcv_data_24h[0][1]) - 1

    ohlcv_data_7d = binance.fetch_ohlcv(symbol, '1m', binance.parse8601(back7dFormatted), 1)
    change7d = (tokenPriceUSDT / ohlcv_data_7d[0][1]) - 1

    print(token, ' current price: ', tokenPriceUSDT, ' 24h: ' , change24h, ' 7d: ', change7d)
    update_list.append([tokenPriceUSDT, change24h, change7d])

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range='\'Token Prices\'!C4',
                                valueInputOption="USER_ENTERED", body={"values":update_list}).execute()
