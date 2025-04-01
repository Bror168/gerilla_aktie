import yfinance as yf
import pandas as pd
import numpy as np

def get_ohlc_data(ticker_symbol, period="5d", interval="1d"):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data

import numpy as np

def RSI(ticker, period=2):
    series = data["Close"]
    delta = series.diff().dropna()
    u = np.where(delta > 0, delta, 0)
    d = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(u[:period])  
    avg_loss = np.mean(d[:period])  
    u = np.concatenate(([avg_gain], u[period:]))
    d = np.concatenate(([avg_loss], d[period:]))
    rs = pd.Series(u).ewm(com=period-1, adjust=False).mean() / \
         pd.Series(d).ewm(com=period-1, adjust=False).mean()
    return 100 - 100 / (1 + rs)


# Example usage:
rsi_values = RSI("MSFT", 2)
print(rsi_values.iloc[-1])  # Print today's RSI value

    
def get_omxs30_companies():
    url = "https://en.wikipedia.org/wiki/OMX_Stockholm_30"
    df_list = pd.read_html(url)
    omxs30_df = df_list[1]  # Justera indexet om det behövs
    companies = omxs30_df[["Company", "Symbol"]]
    return companies

companies = get_omxs30_companies()
omx_list=[]
for index, row in companies.head(30).iterrows():
    symbol = row["Symbol"]
    ny_symbol=""
    for i in range(len(symbol)):
        if symbol[i]==" ":
            ny_symbol+="-"
        else:
            ny_symbol+=symbol[i]
   # print(f"{ny_symbol}"+".ST")
    omx_list.append(ny_symbol +".ST")
#print(omx_list)

