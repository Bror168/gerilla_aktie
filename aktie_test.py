import yfinance as yf #https://yfinance-python.org/reference/api/yfinance.Ticker.html
import pandas as pd
import logic as lo

def get_ohlc_data(ticker_symbol, period="5d", interval="1d"):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data


def get_sp500_list():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df_list = pd.read_html(url)
    sp500_df = df_list[0]  # Tabellen med S&P 500-företag finns oftast som första tabellen
    companies = sp500_df[["Security", "Symbol"]]  
    
    sp500_list = [row["Symbol"] for _, row in companies.iterrows()]
    sp500_list.pop(60)
    sp500_list.pop(74)
    return sp500_list

nasdaq_list=get_sp500_list()

data = pd.DataFrame({
    "Open": [100, 105, 110, 115],  
    "High": [110, 115, 120, 125],  
    "Low": [95, 100, 113, 94],  
    "Close": [108, 112, 114, 123]  
})

#print((nasdaq_list[475]))
#print(ett80_form(get_ohlc_data(nasdaq_list[59])))

for i in range(len(nasdaq_list)-1):
    
    chek_tiker=nasdaq_list[i]
    if lo.ett80_form(get_ohlc_data(chek_tiker)) or lo.reversal_form(get_ohlc_data(chek_tiker)):
        print("{} ticker={}: reversal {} 180 {}".format(i, nasdaq_list[i],lo. ett80_form(get_ohlc_data(chek_tiker)), lo.reversal_form(get_ohlc_data(chek_tiker))))
    else:
        print(i)
