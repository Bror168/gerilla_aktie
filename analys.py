import logic as lo
import sok as so
import tkinter as tk
from tkinter import messagebox
import copy
import yfinance as yf

#global lista med aktier som hittas med list analys, sparas i en global variable för att sedan kunna användas för att sortera utifrån rsi och bbu
aktie_list=[]

#roc=roc(analys[0][i])
#output+="roc:\n"
#for idx in range(len(roc)):
#output+=f"{roc[idx]}\n"

dat = yf.Ticker("AAPL")
dat=dat.history(period='1mo')
print(dat)

#analyserar en aktie
def run_single_analysis():
    ticker = entry.get().upper()  # Hämtar ticker-symbolen från ett inmatningsfält och gör den till versaler
    rsi = lo.calc_rsi(lo.get_ohlc_data(ticker))  # Hämtar historisk data och räknar ut RSI-värdet
    boll = lo.Boll_Band(ticker)  # Hämtar Bollinger Band-data
    analysis = so.single_analys(ticker)  # Kör en separat teknisk analys och letar efter formationer

    # Formaterar och visar resultatet i en etikett
    output = f"RSI:\n{rsi}\n\nBollinger Bands:\n{boll}\n\nFormationer:\n{analysis[0]}"
    result_label.config(text=output)


#analyserar flera aktier samtidigt, input ges i en list med aktie tickers
def run_list_analysis():
    global aktie_list
    string = entry2.get().upper()  # Hämtar användarens input och gör den till versaler
    analys_list = []
    split = 0

    # Delar upp strängen med tickers (som är separerade med mellanslag) till en lista
    for i in range(len(string)):
        if string[i] == " ":
            analys_list.append(string[split:i])
            split = i + 1
        if i + 1 == len(string):  # När sista tecknet är nått, lägg till sista ticker
            analys_list.append(string[split:i + 1])

    analys = so.list_analys(analys_list)  # Gör analys för hela listan
    aktie_list = analys[0]  # Sparar listan av hittade aktier

    # Formaterar och visar resultatet i en text-widget
    output = "    ---Found---\n\n"
    for i in range(len(analys[0])):
        output += f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output += f"{analys[1][i][x]}\n"

    result_text2.config(state="normal")  # Möjliggör redigering tillfälligt
    result_text2.delete("1.0", tk.END)  # Tömmer tidigare innehåll
    result_text2.insert("1.0", output)  # Skriver in nytt resultat
    result_text2.config(state="disabled")  # Låser textfältet igen


#tar en lista med n antal aktier tickers och rangårdnar dom efter bäst till sämst
def run_best_analysis():
    string = entry4.get().upper()  # Hämtar användarens input
    analys_list = []
    split = 0

    # Parsar tickers från strängen och sparar i analys_list
    for i in range(len(string)):
        if string[i] == " ":
            analys_list.append(string[split:i])
            split = i + 1
        if i + 1 == len(string):
            analys_list.append(string[split:i + 1])

    analys = so.list_analys(analys_list)
    aktie_list = analys[0]  # Lista över hittade tickers

    # Rangordnar aktier baserat på RSI och Bollinger Band
    rsi_topp = so.sort_RSI(copy.deepcopy(aktie_list))  # Sorterad lista enligt RSI
    bbu_topp = so.sort_BB(copy.deepcopy(aktie_list))   # Sorterad lista enligt BB

    wight_list = []  # Lista som håller viktningen (lägre värde = bättre rankning)

    for i in range(len(aktie_list)):
        # Kombinerar ranking från båda indikatorer
        wight_list.append(bbu_topp.index(aktie_list[i]))
        wight_list[i] += rsi_topp.index(aktie_list[i])

    smal_list = lo.quick_sort(wight_list)  # Sorterar aktierna efter total rank

    output = "    ---topp 5---\n\n"
    for i in range(len(analys[0])):
        if i == 5:  # Visar bara topp 5 aktier
            result_label4.config(text=output)
            return
        
        index = wight_list.index(smal_list[i])  # Hitta index för nästa bäst rankade aktie
        smal_list[i] = ""  # Tömmer värde så vi inte återanvänder samma
        wight_list[index] = ""
        
        # Lägger till analysdata i utmatningen
        output += f"#{i+1} {analys[0][index]} :\n"
        for x in range(len(analys[1][index])):
            output += f"{analys[1][index][x]}\n"
        output += f"rsi:{lo.calc_rsi(so.get_ohlc_data(analys[0][index]))}\n"
        output += f"bbu:{lo.Boll_Band(analys[0][index])}\n"
        output += "\n"

    result_label4.config(text=output)  # Visar resultatet

# sorterar en lista med aktietickers utifrån bolingerband(bbu) eller relativ strength index(rsi)
def sortera(mode):
    global aktie_list
    sort_list = []

    # Väljer sorteringsmetod beroende på användarens val
    if mode == "rsi":
        sort_list = so.sort_RSI(aktie_list)  # Sortera baserat på RSI-värde (lågt RSI => översåld)
    if mode == "bb":
        sort_list = so.sort_BB(aktie_list)   # Sortera baserat på Bollinger Band (ev. avvikelse från medel)

    aktie_list = sort_list  # Uppdaterar den globala listan med sorterad lista

    # Formaterar och skriver ut sorterat resultat i ett textfält
    output = "    ---Found---\n\n"
    for i in range(len(sort_list)):
        output += f"{sort_list[i]} :\n"
        if mode == "rsi":
            output += f"{lo.calc_rsi(lo.get_ohlc_data(sort_list[i]))} :\n\n"  # Visar RSI-värde
        if mode == "bb":
            output += f"{lo.Boll_Band(sort_list[i])} :\n\n"  # Visar BB-värden

    result_text2.config(state="normal")  
    result_text2.delete("1.0", tk.END)  # Töm tidigare innehåll
    result_text2.insert("1.0", output)  # Skriv nytt innehåll
    result_text2.config(state="disabled")  # Gör fältet skrivskyddat igen


# analyserar alla aktier på en index, tar ett input med namn på indexen t.ex omx30
def index_analyze():
    string = entry3.get().upper()  # Hämtar och konverterar användarens input till versaler
    analys_list = []

    # Hämtar lista med tickers beroende på valt index
    if string == "OMX30":
        analys_list = so.omx30()
    if string == "SP500":
        analys_list = so.get_sp500_list()
    
    analys = so.list_analys(analys_list)  # Kör teknisk analys på varje aktie i listan

    output = "    ---Found---\n"
    for i in range(len(analys[0])):
        output += f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output += f"{analys[1][i][x]}\n"
        output += "\n"

    # Skriver även ut tickers på en rad längst ner
    for i in range(len(analys[0])):
        output += f"{analys[0][i]} "

    result_text3.config(state="normal")  
    result_text3.delete("1.0", tk.END)
    result_text3.insert("1.0", output)
    result_text3.config(state="disabled")  


#knapp som bytter till singel analys
def show_single_analyze():
    # Döljer andra vyer och visar single_frame
    index_frame.pack_forget()
    list_frame.pack_forget()
    best_frame.pack_forget()
    single_frame.pack(padx=10, pady=10)


#knapp som bytter till list analys
def show_list_analyze():
    # Döljer andra vyer och visar list_frame
    index_frame.pack_forget()
    single_frame.pack_forget()
    best_frame.pack_forget()
    list_frame.pack(padx=10, pady=10)


#knapp som bytter till index analys
def show_index_analyze():
    # Döljer andra vyer och visar index_frame
    list_frame.pack_forget()
    single_frame.pack_forget()
    best_frame.pack_forget()
    index_frame.pack(padx=10, pady=10)


#knapp som bytter till aktie analys läge
def show_best_analyze():
    # Döljer andra vyer och visar best_frame
    list_frame.pack_forget()
    single_frame.pack_forget()
    index_frame.pack_forget()
    best_frame.pack(padx=10, pady=10)

    

# GUI setup
root = tk.Tk()
root.title("Stock Analyzer")  # Fönstertitel

#knappar
top_button_frame = tk.Frame(root)  # Översta raden med knappar för att byta analysläge
top_button_frame.pack(pady=10)

# Knappar för att växla mellan analyslägen (byter vy)
tk.Button(top_button_frame, text="Single Analyze", command=show_single_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="List Analyze", command=show_list_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="Index Analyze", command=show_index_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="best stock", command=show_best_analyze).pack(side="left", padx=5)


#single analys
single_frame = tk.Frame(root)  # Ram för single analyse-vyn

tk.Label(single_frame, text="Enter Ticker Symbol:").pack(pady=5)  # Instruktionstext
entry = tk.Entry(single_frame, width=30)  # Inmatningsfält för ticker
entry.pack(pady=5)

tk.Button(single_frame, text="Analyze", command=run_single_analysis).pack(pady=10)  # Kör analys

# Här visas resultatet från analysen
result_label = tk.Label(single_frame, text="", justify="left", wraplength=400)
result_label.pack(padx=10, pady=10)


#list analys
list_frame = tk.Frame(root)  # Ram för list analyse-vyn
tk.Label(list_frame, text="Enter list e.g: AAPL NVDA MSFT").pack()  # Instruktionstext
entry2 = tk.Entry(list_frame, width=30)  # Inmatningsfält för tickers
entry2.pack(pady=5)

# Knapp för att analysera alla tickers i listan
tk.Button(list_frame, text="Analyze", command=run_list_analysis).pack(pady=10)
# Knappar för att sortera analysresultat
tk.Button(list_frame, text="sort rsi", command=lambda: sortera("rsi")).pack(pady=10)
tk.Button(list_frame, text="sort bbu", command=lambda: sortera("bb")).pack(pady=10)

# Resultatfält med scrollbar
result_frame2 = tk.Frame(list_frame)
result_frame2.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar2 = tk.Scrollbar(result_frame2)
scrollbar2.pack(side="right", fill="y")
result_text2 = tk.Text(result_frame2, wrap="word", yscrollcommand=scrollbar2.set, height=15, width=30)
result_text2.pack(side="left", fill="both", expand=True)
scrollbar2.config(command=result_text2.yview)


#index analys
index_frame = tk.Frame(root)  # Ram för index analyse-vyn
tk.Label(index_frame, text="välj indexlista |OMX30, SP500|").pack()  # Instruktionstext
entry3 = tk.Entry(index_frame, width=30)  # Inmatningsfält för indexnamn
entry3.pack(pady=5)

tk.Button(index_frame, text="Analyze", command=index_analyze).pack(pady=10)  # Kör analys

# Resultatfält med scrollbar
result_frame3 = tk.Frame(index_frame)
result_frame3.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar3 = tk.Scrollbar(result_frame3)
scrollbar3.pack(side="right", fill="y")
result_text3 = tk.Text(result_frame3, wrap="word", yscrollcommand=scrollbar3.set, height=15, width=30)
result_text3.pack(side="left", fill="both", expand=True)
scrollbar3.config(command=result_text3.yview)


#bästa aktien 
best_frame = tk.Frame(root)  # Ram för best stock-vyn
tk.Label(best_frame, text="whil finde the best stock\n input exemple |AAPL NVDA MSFT|").pack()  # Instruktionstext
entry4 = tk.Entry(best_frame, width=30)  # Inmatningsfält för tickers
entry4.pack(pady=5)

tk.Button(best_frame, text="Analyze", command=run_best_analysis).pack(pady=10)  # Kör analys

# Här visas topplistan med bästa aktier
result_label4 = tk.Label(best_frame, text="", justify="left", wraplength=400)
result_label4.pack(padx=10, pady=10)

# Startar huvudloopen för gränssnittet
root.mainloop()
