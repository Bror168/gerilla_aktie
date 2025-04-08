import yfinance as yf #https://yfinance-python.org/reference/api/yfinance.Ticker.html
import pandas as pd
import logic as lo
import time

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
    sp500_list.pop(73)
    return sp500_list

#nasdaq_list=get_sp500_list()

data = pd.DataFrame({
    "Open": [100, 105, 110, 115],  
    "High": [110, 115, 120, 125],  
    "Low": [95, 100, 113, 94],  
    "Close": [108, 112, 114, 123]  
})

#print((nasdaq_list[475]))
#print(ett80_form(get_ohlc_data(nasdaq_list[59])))

def single_analys(chek_tiker):
    ohlc = get_ohlc_data(chek_tiker)
    found = False
    form_list=[]

    if lo.ett80_form(ohlc):
        form_list.append("180")
    if lo.reversal_form(ohlc):
        form_list.append("reversal")
    if lo.spik_form(ohlc):
        form_list.append("spik")
    if lo.key_reversal_form(ohlc):
        form_list.append("key_reversel")
    if lo.interference_form(ohlc):
        form_list.append("interference")
    if lo.fort_form(chek_tiker):
        form_list.append("fortsätnings")
    if lo.holy_grail_form(ohlc, chek_tiker):
        form_list.append("holy grail!")
    if lo.pattern_gap_form(ohlc):
        form_list.append("patern gap")
    if lo.impuls_form(ohlc, chek_tiker):
        form_list.append("impuls")
    if lo.Riko_form(ohlc):
        form_list.append("rikoshet")
    if lo.reversal_gap_formation(ohlc):
        form_list.append("reversel gap")
    
    if len(form_list)>0:
        found=True
    
    return form_list, found

def list_analys(list):
    print(list)
    return_list=[]
    form_list=[]
    for i in range(len(list)):
        good=single_analys(list[i])
        if good[-1]:
            return_list.append(list[i])
            form_list.append(good[0])
        if i%60==0 and i!=0:
            print("pausar pga 'Rate limited'.")
            time.sleep(30)
            print("startar igen")
    return return_list , form_list

good_boys=['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AFL', 'A', 'APD', 'AKAM', 'ARE', 'ALGN', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AEE', 'AEP', 'AMT', 'AMGN', 'ADI', 'ANSS', 'AON', 'AAPL', 'APTV', 'ACGL', 'AJG', 'AIZ', 'T', 'ATO', 'ADP', 'AZO', 'AVB', 'BKR', 'BALL', 'BAX', 'BIIB', 'BK', 'BKNG', 'BSX', 'BR', 'BRO', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'CCL', 'CBOE', 'CDW', 'CNC', 'CNP', 'CHTR', 'CVX', 'CB', 'CHD']
def sort_rsi(list):
    temp_list=list
    rsi_list=[]
    ticker_list=[]
    for i in range(len(list)):
        ohlc = get_ohlc_data(list[i])
        rsi_list.append(lo.calc_rsi(ohlc))
    sorted_rsi=lo.quick_sort(rsi_list)
    for i in range(len(sorted_rsi)):
        index = rsi_list.index(sorted_rsi[i])
        ticker_list.append(temp_list[index])
        temp_list[index]=""
        rsi_list[index]=""
    
    return ticker_list

def sort_BB(list):
    temp_list=list
    bb_list=[]
    ticker_list=[]
    for i in range(len(list)):
        bb_list.append(lo.Boll_Band(list[i]))
    sorted_BB=lo.quick_sort(bb_list)
    
    for i in range(len(sorted_BB)):
        index = bb_list.index(sorted_BB[i])
        ticker_list.append(temp_list[index])
        temp_list[index]=""
        bb_list[index]=""
    
    return ticker_list
#print (list_analys(nasdaq_list))


#b= sort_BB(good_boys)
#print(b[-1])
#print("rsi:")
#print(lo.calc_rsi(get_ohlc_data("VOLV-B.ST")))
#print("vol:")
#print(lo.Boll_Band("VOLV-B.ST"))
#print(single_analys("VOLV-B.ST"))
# Assuming these exist and work




