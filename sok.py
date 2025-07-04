import yfinance as yf #https://yfinance-python.org/reference/api/yfinance.Ticker.html
import pandas as pd
import logic as lo
import time
from collections import Counter


def get_tickers_on_index(wiki_index, End):
    #hämtar lista på tickers i en viss index från wikipedia
    url = f"https://en.wikipedia.org/wiki/{wiki_index}"
    df_list = pd.read_html(url)
    companies = pd.DataFrame()
    for i in range(len(df_list)):
        try:
            index_list_df = df_list[i]  
            
            if "Symbol" in index_list_df:
                companies = pd.DataFrame(index_list_df[["Symbol"]])
        except Exception as e:
            print(":(")

    index_list=[]
    # läger på .st på alla tickers, gör om mellan rum till - samt omformatiserar datan
    
    for index, row in companies.head(len(companies)).iterrows():
        symbol = row["Symbol"]
        ny_symbol=""
        for i in range(len(symbol)):
            if symbol[i]==" ":
                ny_symbol+="-"
            else:
                ny_symbol+=symbol[i]
        if End.upper()!= "NONE":
            index_list.append(ny_symbol +f".{End}")
        else:
            index_list.append(ny_symbol)
    return index_list

def index_edge(index_ticker):
    edge_true=single_analys(index_ticker)[1]
    return edge_true

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
        print(i, len(return_list))

    count_list=[]
    for i in form_list:
        count_list.append(i[0])
    räknare = Counter(count_list)

    # Konvertera till DataFrame
    df = pd.DataFrame(räknare.items(), columns=["form", "antal"])

    return return_list , form_list, df

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
