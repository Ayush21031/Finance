import yfinance as yf
import pandas as pd

def fun(symbol):
    nifty_symbol = symbol
    start_date = '2023-04-01'
    end_date = '2024-07-01'

    nifty_data = yf.download(tickers=nifty_symbol, start=start_date, end=end_date, interval='1d')
    nifty_data['EMA50'] = nifty_data['Close'].ewm(span=50, adjust=False).mean()

    # Calculated the upper and lower bounds for buy signal (1% range around EMA)
    nifty_data['Upper_Bound'] = nifty_data['EMA50'] * 1.01
    nifty_data['Lower_Bound'] = nifty_data['EMA50'] * 0.99

    buy_signals = nifty_data[(nifty_data['Close'] >= nifty_data['Lower_Bound']) & (nifty_data['Close'] <= nifty_data['Upper_Bound'])]

    # Check if the last day's close price is in the buy signal range
    if not buy_signals.empty and buy_signals.index[-1] == nifty_data.index[-1]:
        return symbol

data = pd.read_csv("ind_nifty500list.csv")
names = data["Symbol"].values

buy_signal_stocks = []
for symbol in names:
    symbol = symbol + ".NS"
    result = fun(symbol)
    if result is not None:
        buy_signal_stocks.append(result)

print("Stocks in the buy signal range as of the current date:")
for stock in buy_signal_stocks:
    print(stock)