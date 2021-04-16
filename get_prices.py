import ccxt
from datetime import date, timedelta

yesterday = date.today() - timedelta(days=1)
startOfYesterday = yesterday.strftime("%Y-%m-%d") + " 00:00:00"

binance = ccxt.binance ({ 'enableRateLimit': True })
symbols = [ 'ETH/USDT', 'BTC/USDT', 'ADA/USDT', 'LINK/USDT', 'XRP/USDT', 'DOT/USDT' ]
for symbol in symbols:
    ohlcv_data = binance.fetch_ohlcv(symbol, '1d', binance.parse8601(startOfYesterday), 1)
    print(ohlcv_data)

