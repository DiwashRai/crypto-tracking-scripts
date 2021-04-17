# import ccxt
# from datetime import date, timedelta

# yesterday = date.today() - timedelta(days=1)
# startOfYesterday = yesterday.strftime("%Y-%m-%d") + " 00:00:00"

# binance = ccxt.binance ({ 'enableRateLimit': True })
# symbols = [ 'ETH/USDT', 'BTC/USDT', 'ADA/USDT', 'LINK/USDT', 'XRP/USDT', 'DOT/USDT' ]
# for symbol in symbols:
#     ohlcv_data = binance.fetch_ohlcv(symbol, '1d', binance.parse8601(startOfYesterday), 1)
#     print(ohlcv_data)


from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1PJUh6kNjcUjVTpHzBFixIM0f1EZpOGKiDOhd5h7xYeQ'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Transactions!A1:C9").execute()
# values = result.get('values', [])

print(result)