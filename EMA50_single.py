import yfinance as yf
import plotly.graph_objects as go


nifty_symbol = '^NSEI'
start_date = '2023-04-01'
end_date = '2024-04-28'


nifty_data = yf.download(tickers=nifty_symbol, start=start_date, end=end_date, interval='1d')

nifty_data['EMA50'] = nifty_data['Close'].ewm(span=50, adjust=False).mean()

# Calculated the upper and lower bounds for buy signal (2% range around EMA)
nifty_data['Upper_Bound'] = nifty_data['EMA50'] * 1.01
nifty_data['Lower_Bound'] = nifty_data['EMA50'] * 0.99


buy_signals = nifty_data[(nifty_data['Close'] >= nifty_data['Lower_Bound']) & (nifty_data['Close'] <= nifty_data['Upper_Bound'])]


fig = go.Figure(data=[
    go.Candlestick(x=nifty_data.index,
                   open=nifty_data['Open'],
                   high=nifty_data['High'],
                   low=nifty_data['Low'],
                   close=nifty_data['Close'],
                   name='Candlesticks'),
    go.Scatter(x=nifty_data.index,
               y=nifty_data['EMA50'],
               mode='lines',
               line=dict(color='orange', width=2),
               name='EMA50'),
    go.Scatter(x=buy_signals.index,
               y=buy_signals['Close'],
               mode='markers',
               marker=dict(color='green', size=8, symbol='circle'),
               name='Buy Signal')
])


fig.update_layout(title='Nifty 50 Candlestick Chart with EMA50 and Buy Signals',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  template='plotly_dark')


fig.show()
