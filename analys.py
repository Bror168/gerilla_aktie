# ----------------------------------------------------
# Gerilla Aktie – © 2025 Bror168
# Skapad av Bror168 (https://github.com/Bror168)
# Denna kod är skyddad enligt MIT-licensen.
# All kopiering utan erkännande är förbjuden.
# Version: 1.0.0
# ----------------------------------------------------

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

    

# ======= GUI ========

# färgtema
bg_color = "#343541"
btn_color = "#444654"
text_color = "#ffffff"

root = tk.Tk()
root.title("Stock Analyzer")  # Fönstertitel
root.configure(bg=bg_color)

def show_ascii_frame(): #skriver ut github tagen till skärmen
    ascii_frame = tk.Frame(root, bg=bg_color, bd=2, relief="sunken")
    ascii_frame.pack(fill="x", pady=5)
    ascii_art = "                                                               ,---.-,    \n                                                             '   ,'  '.  \n    ,---,.                                  ,---,             /   /      \\ \n  ,'  .'  \\                              ,`--.' |    ,---.   .   ;  ,/.  : \n,---.' .' |  __  ,-.   ,---.    __  ,-. /    /  :   /     \\  '   |  | :  ; \n|   |  |: |,' ,'/ /|  '   ,'\\ ,' ,'/ /|:    |.' '  /    / '  '   |  ./   : \n:   :  :  /'  | |' | /   /   |'  | |' |`----':  | .    ' /   |   :       , \n:   |    ; |  |   ,'.   ; ,. :|  |   ,'   '   ' ;'    / ;     \\   \\     /  \n|   :     \\'  :  /  '   | |: :'  :  /     |   | ||   :  \\      ;   ,   '\\  \n|   |   . ||  | '   '   | .; :|  | '      '   : ;;   |   ``.  /   /      \\ \n'   :  '; |;  : |   |   :    |;  : |      |   | ''   ;      \\.   ;  ,/.  : \n|   |  | ; |  , ;    \\   \\  / |  , ;      '   : |'   |  .\\  |'   |  | :  ; \n|   :   /   ---'      `----'   ---'       ;   |.'|   :  ';  :'   |  ./   : \n|   | ,'                                  '---'   \\   \\    / |   :      /  \n`----'                                             `---`--`   \\   \\   .'   \n                                                               `---`-'      \n"
    label = tk.Label(ascii_frame, text=ascii_art, font=("Courier", 7), bg=bg_color, fg=text_color, justify="left")
    label.pack(padx=10, pady=5)
    # Ta bort ramen efter 3 sekunder
    root.after(1000, ascii_frame.destroy)


# hjälpmetoder för att implementera färger
def colored_button(master, text, command):
    return tk.Button(master, text=text, command=command, bg=btn_color, fg=text_color, activebackground="#555555", activeforeground=text_color)

def colored_label(master, text):
    return tk.Label(master, text=text, bg=bg_color, fg=text_color)

def colored_entry(master, width=30):
    return tk.Entry(master, width=width, bg=btn_color, fg=text_color, insertbackground=text_color)

def colored_text(master, height=15, width=30, yscrollcommand=None):
    return tk.Text(master, height=height, width=width, wrap="word", bg=btn_color, fg=text_color, insertbackground=text_color, yscrollcommand=yscrollcommand)


#knappar
top_button_frame = tk.Frame(root, bg=bg_color)  # Översta raden med knappar för att byta analysläge
top_button_frame.pack(pady=10)

# Knappar för att växla mellan analyslägen (byter vy)
colored_button(top_button_frame, "Single Analyze", show_single_analyze).pack(side="left", padx=5)
colored_button(top_button_frame, "List Analyze", show_list_analyze).pack(side="left", padx=5)
colored_button(top_button_frame, "Index Analyze", show_index_analyze).pack(side="left", padx=5)
colored_button(top_button_frame, "best stock", show_best_analyze).pack(side="left", padx=5)

show_ascii_frame()


#single analys
single_frame = tk.Frame(root, bg=bg_color)  # Ram för single analyse-vyn

colored_label(single_frame, "Enter Ticker Symbol:").pack(pady=5)  # Instruktionstext
entry = colored_entry(single_frame)  # Inmatningsfält för ticker
entry.pack(pady=5)

colored_button(single_frame, "Analyze", run_single_analysis).pack(pady=10)  # Kör analys

# Här visas resultatet från analysen
result_label = tk.Label(single_frame, text="", justify="left", wraplength=400, bg=bg_color, fg=text_color)
result_label.pack(padx=10, pady=10)


#list analys
list_frame = tk.Frame(root, bg=bg_color)  # Ram för list analyse-vyn
colored_label(list_frame, "Enter list e.g: AAPL NVDA MSFT").pack()  # Instruktionstext
entry2 = colored_entry(list_frame)  # Inmatningsfält för tickers
entry2.pack(pady=5)

# Knapp för att analysera alla tickers i listan
colored_button(list_frame, "Analyze", run_list_analysis).pack(pady=10)
# Knappar för att sortera analysresultat
colored_button(list_frame, "sort rsi", lambda: sortera("rsi")).pack(pady=10)
colored_button(list_frame, "sort bbu", lambda: sortera("bb")).pack(pady=10)

# Resultatfält med scrollbar
result_frame2 = tk.Frame(list_frame, bg=bg_color)
result_frame2.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar2 = tk.Scrollbar(result_frame2)
scrollbar2.pack(side="right", fill="y")
result_text2 = colored_text(result_frame2, yscrollcommand=scrollbar2.set)
result_text2.pack(side="left", fill="both", expand=True)
scrollbar2.config(command=result_text2.yview)


#index analys
index_frame = tk.Frame(root, bg=bg_color)  # Ram för index analyse-vyn
colored_label(index_frame, "välj indexlista |OMX30, SP500|").pack()  # Instruktionstext
entry3 = colored_entry(index_frame)  # Inmatningsfält för indexnamn
entry3.pack(pady=5)

colored_button(index_frame, "Analyze", index_analyze).pack(pady=10)  # Kör analys

# Resultatfält med scrollbar
result_frame3 = tk.Frame(index_frame, bg=bg_color)
result_frame3.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar3 = tk.Scrollbar(result_frame3)
scrollbar3.pack(side="right", fill="y")
result_text3 = colored_text(result_frame3, yscrollcommand=scrollbar3.set)
result_text3.pack(side="left", fill="both", expand=True)
scrollbar3.config(command=result_text3.yview)


#bästa aktien 
best_frame = tk.Frame(root, bg=bg_color)  # Ram för best stock-vyn
colored_label(best_frame, "whil finde the best stock\n input exemple |AAPL NVDA MSFT|").pack()  # Instruktionstext
entry4 = colored_entry(best_frame)  # Inmatningsfält för tickers
entry4.pack(pady=5)

colored_button(best_frame, "Analyze", run_best_analysis).pack(pady=10)  # Kör analys

# Här visas topplistan med bästa aktier
result_label4 = tk.Label(best_frame, text="", justify="left", wraplength=400, bg=bg_color, fg=text_color)
result_label4.pack(padx=10, pady=10)

# Startar huvudloopen för gränssnittet
root.mainloop()
