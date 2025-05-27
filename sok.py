# ----------------------------------------------------
# Gerilla Aktie – © 2025 Bror168
# Skapad av Bror168 (https://github.com/Bror168)
# Denna kod är skyddad enligt MIT-licensen.
# All kopiering utan erkännande är förbjuden.
# Version: 1.0.0
# ----------------------------------------------------

import yfinance as yf #https://yfinance-python.org/reference/api/yfinance.Ticker.html
import pandas as pd
import logic as lo
import time

def get_sp500_list():
    #hämtar lista på sp500 tickers från wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    df_list = pd.read_html(url)
    sp500_df = df_list[0]  
    companies = sp500_df[["Security", "Symbol"]]  
    
    sp500_list = [row["Symbol"] for _, row in companies.iterrows()] #formatiserar
    #tar bort företag som inta fans med på yfinance
    sp500_list.pop(60)
    sp500_list.pop(74)
    sp500_list.pop(73)
    return sp500_list

def omx30():
    #hämtar lista på omx30 tickers från wikipedia
    url = "https://en.wikipedia.org/wiki/OMX_Stockholm_30"
    df_list = pd.read_html(url)
    omxs30_df = df_list[1]  
    companies = omxs30_df[["Company", "Symbol"]]

    omx_list=[]
    # läger på .st på alla tickers, gör om mellan rum till - samt omformatiserar datan
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
    #hämtar ohlc för aktie (ticker)
    ohlc = lo.get_ohlc_data(chek_tiker)
    found = False
    form_list=[]

    #kollar om aktien uppfyler kraven för någon av formationerna
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
    
    #kollar om aktien uppfylde någon av formationerna
    if len(form_list)>0:
        found=True
    
    return form_list, found

#ta en lista med aktier och analyserar
def list_analys(list):
    return_list=[]
    form_list=[]
    for i in range(len(list)):
        #analyserar aktien
        good=single_analys(list[i])
        if good[-1]:
            #läger till aktien på en lista med potensielt bra aktier samt vilka formationer de uppfyler
            return_list.append(list[i])
            form_list.append(good[0])
        #pga request limits till yfinance behöver programet pausa om den skickar för många requests 
        if i%60==0 and i!=0:
            time.sleep(30)
    return return_list , form_list

#sorterar aktier efter deras rsi värde
def sort_RSI(list):
    temp_list=list
    rsi_list=[]
    ticker_list=[]
    for i in range(len(list)):
        #läger på rsi av aktierna på en lista
        ohlc = lo.get_ohlc_data(list[i])
        rsi_list.append(lo.calc_rsi(ohlc))
     #sortera denna lista med rsi samt 
    sorted_rsi=lo.quick_sort(rsi_list)
    # sorterar aktielistan utifrån rsi listan
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
        #sorterar efter bolinger band
        bb_list.append(lo.Boll_Band(list[i]))
    sorted_BB=lo.quick_sort(bb_list)
    #vänder på listan
    for i in range(len(bb_list)):
        invert_list.append(sorted_BB[-i-1])
    sorted_BB=invert_list
    
    #sorterar aktielistan utifrån bolinger band listan 
    for i in range(len(sorted_BB)):
        index = bb_list.index(sorted_BB[i])
        ticker_list.append(temp_list[index])
        temp_list[index]=""
        bb_list[index]=""
    
    return ticker_list