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

nasdaq_list=get_sp500_list()

data = pd.DataFrame({
    "Open": [100, 105, 110, 115],  
    "High": [110, 115, 120, 125],  
    "Low": [95, 100, 113, 94],  
    "Close": [108, 112, 114, 123]  
})

#print((nasdaq_list[475]))
#print(ett80_form(get_ohlc_data(nasdaq_list[59])))

def single_analys(chek_tiker, found):
    ohlc = get_ohlc_data(chek_tiker)
    found[0] = False

    if lo.ett80_form(ohlc):
        print("{}: 180".format(chek_tiker))
        found[0] = True
    if lo.reversal_form(ohlc):
        print("{}: reversal".format(chek_tiker))
        found[0] = True
    if lo.spik_form(ohlc):
        print("{} : spik".format(chek_tiker))
        found[0] = True
    if lo.key_reversal_form(ohlc):
        print("{} : key_reversel".format(chek_tiker))
        found[0] = True
    if lo.interference_form(ohlc):
        print("{} : interference".format(chek_tiker))
        found[0] = True
    if lo.fort_form(chek_tiker):
        print("{} : fortsätnings".format(chek_tiker))
        found[0] = True
    if lo.holy_grail_form(ohlc, chek_tiker):
        print("{} : holy grail!".format(chek_tiker))
        found[0] = True
    if lo.pattern_gap_form(ohlc):
        print("{} : patern gap".format(chek_tiker))
        found[0] = True
    if lo.impuls_form(ohlc, chek_tiker):
        print("{} : impuls".format(chek_tiker))
        found[0] = True
    if lo.Riko_form(ohlc):
        print("{} : rikoshet".format(chek_tiker))
        found[0] = True
    if lo.reversal_gap_formation(ohlc):
        print("{} : reversel gap".format(chek_tiker))
        found[0] = True

    return found[0]

def list_analys(list):
    good_boys=[]
    found=[False]
    for i in range(len(list)-400):
        single_analys(list[i], found)
        if found[0] :
            good_boys.append(list[i])

        if i%60==0 and i!=0:
            print("pausar pga 'Rate limited'.")
            time.sleep(30)
            print("startar igen")
    return good_boys

good_boys=['MMM', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', 'APD', 'ABNB', 'AKAM', 'ALGN', 'ALLE', 'LNT', 'GOOGL', 'GOOG', 'MO', 'AMZN', 'AMCR', 'AEE', 'AXP', 'AIG', 'AMT', 'AMP', 'AME', 'ADI', 'ANSS', 'APA', 'APO', 'AMAT', 'APTV', 'ANET', 'ATO', 'ADSK', 'ADP', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BDX', 'BBY', 'TECH', 'BIIB', 'BLK', 'BX', 'BK', 'BKNG', 'BSX', 'AVGO', 'BR', 'BXP', 'CHRW', 'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'CCL', 'CARR', 'CAT', 'CBRE', 'CNC', 'CNP', 'CF', 'CHTR', 'CVX', 'CMG', 'CB']
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
        ohlc = get_ohlc_data(list[i])
        bb_list.append(lo.Boll_Band(ohlc))
    sorted_BB=lo.quick_sort(bb_list)
    
    for i in range(len(sorted_BB)):
        index = bb_list.index(sorted_BB[i])
        ticker_list.append(temp_list[index])
        temp_list[index]=""
        bb_list[index]=""
    
    return ticker_list
#print (list_analys(nasdaq_list))


b= sort_BB(good_boys)
print(b[0])
print(lo.calc_rsi(get_ohlc_data("ato")))
print(lo.Boll_Band(get_ohlc_data("ato")))
