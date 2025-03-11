import yfinance as yf
import pandas as pd

def get_ohlc_data(ticker_symbol, period="5d", interval="1d"):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data

def reversal_form(data):
    close_list = data["Close"].tolist()
    open_list = data["Open"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    
    if not close_list[-1]>close_list[-2]:
        san=False
    
    if not close_list[-1]>high_list[-2]:
        san=False
    
    return san

def ett80_form(data):
    close_list = data["Close"].tolist()
    open_list = data["Open"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True

    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    if (close_list[-2]-low_list[-2])/(high_list[-2]-low_list[-2])>0.25:
        san=False
    return san

def get_sp500_list():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df_list = pd.read_html(url)
    sp500_df = df_list[0]  # Tabellen med S&P 500-företag finns oftast som första tabellen
    companies = sp500_df[["Security", "Symbol"]]  
    
    sp500_list = [row["Symbol"] for _, row in companies.iterrows()]
    return sp500_list

nasdaq_list=get_sp500_list()
data = pd.DataFrame({
    "Open": [100, 105, 110, 115],  
    "High": [110, 115, 120, 125],  
    "Low": [95, 100, 113, 94],  
    "Close": [108, 112, 114, 123]  
})

print(get_ohlc_data(nasdaq_list[59]))
print(ett80_form(nasdaq_list[59]))

for i in range(len(nasdaq_list)-1):
    print("reversal {} 180 {}".format(ett80_form(get_ohlc_data(nasdaq_list[i])), reversal_form(get_ohlc_data(nasdaq_list[i]))))
    print(i)