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

def omx30():
    url = "https://en.wikipedia.org/wiki/OMX_Stockholm_30"
    df_list = pd.read_html(url)
    omxs30_df = df_list[1]  # Justera indexet om det behövs
    companies = omxs30_df[["Company", "Symbol"]]

    omx_list=[]
    for index, row in companies.head(30).iterrows():
        symbol = row["Symbol"]
        ny_symbol=""
        for i in range(len(symbol)):
            if symbol[i]==" ":
                ny_symbol+="-"
            else:
                ny_symbol+=symbol[i]
        omx_list.append(ny_symbol +".ST")
    return omx_list

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
    return_list=[]
    form_list=[]
    for i in range(len(list)):
        good=single_analys(list[i])
        if good[-1]:
            return_list.append(list[i])
            form_list.append(good[0])
        if i%60==0 and i!=0:
            time.sleep(30)
    return return_list , form_list

def sort_RSI(list):
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
    invert_list=[]
    bb_list=[]
    ticker_list=[]
    for i in range(len(list)):
        
        bb_list.append(lo.Boll_Band(list[i]))
    sorted_BB=lo.quick_sort(bb_list)
    for i in range(len(bb_list)):
        invert_list.append(sorted_BB[-i-1])
    sorted_BB=invert_list
    
    for i in range(len(sorted_BB)):
        index = bb_list.index(sorted_BB[i])
        ticker_list.append(temp_list[index])
        temp_list[index]=""
        bb_list[index]=""
    
    return ticker_list