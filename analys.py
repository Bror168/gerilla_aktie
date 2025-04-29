import logic as lo
import sok as so
import tkinter as tk
from tkinter import messagebox
import copy

aktie_list=[]

def run_single_analysis(): 
    ticker = entry.get().upper()
    rsi = lo.calc_rsi(so.get_ohlc_data(ticker))
    boll = lo.Boll_Band(ticker)
    analysis = so.single_analys(ticker)

    output = f"RSI:\n{rsi}\n\nBollinger Bands:\n{boll}\n\nFormationer:\n{analysis[0]}"
    result_label.config(text=output)



def run_list_analysis():
    global aktie_list
    string=entry2.get().upper()
    analys_list=[]
    split=0
    for i in range(len(string)):
        if string[i]==" ":
            analys_list.append(string[split:i])
            split=i+1
        if i+1==len(string):
            analys_list.append(string[split:i+1])

    
    analys = so.list_analys(analys_list)
    aktie_list=analys[0]
    
    output="    ---Found---\n\n"
    for i in range(len(analys[0])):
        output+=f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output+=f"{analys[1][i][x]}\n"
        output+="\n"
    
    result_text2.config(state="normal")  
    result_text2.delete("1.0", tk.END)
    result_text2.insert("1.0", output)
    result_text2.config(state="disabled")

def run_best_analysis():
    string=entry4.get().upper()
    analys_list=[]
    split=0
    for i in range(len(string)):
        if string[i]==" ":
            analys_list.append(string[split:i])
            split=i+1
        if i+1==len(string):
            analys_list.append(string[split:i+1])

    analys = so.list_analys(analys_list)
    aktie_list=analys[0]
    rsi_topp=so.sort_RSI(copy.deepcopy(aktie_list))
    bbu_topp=so.sort_BB(copy.deepcopy(aktie_list))
    wight_list=[]

    for i in range(len(aktie_list)):
        wight_list.append(bbu_topp.index(aktie_list[i]))
        wight_list[i]+=rsi_topp.index(aktie_list[i])
    smal_list=lo.quick_sort(wight_list)
    
    
    output="    ---topp 5---\n\n"
    for i in range(len(analys[0])):
        if i==5:
            result_label4.config(text=output)
            return
        index=wight_list.index(smal_list[i])
        smal_list[i]=""
        wight_list[index]=""
        output+=f"#{i+1} {analys[0][index]} :\n"
        for x in range(len(analys[1][index])):
            output+=f"{analys[1][index][x]}\n"
        output+=f"rsi:{lo.calc_rsi(so.get_ohlc_data(analys[0][index]))}\n"
        output+=f"bbu:{lo.Boll_Band(analys[0][index])}\n"
        output+="\n"
    
    result_label4.config(text=output)


def sortera(mode):
    global aktie_list
    sort_list=[]
    if mode=="rsi":
        sort_list=so.sort_RSI(aktie_list)
    if mode=="bb":
        sort_list=so.sort_BB(aktie_list)

    aktie_list=sort_list

    output="    ---Found---\n\n"
    for i in range(len(sort_list)):
        output+=f"{sort_list[i]} :\n"
        if mode=="rsi":
            output+=f"{lo.calc_rsi(lo.get_ohlc_data(sort_list[i]))} :\n\n"
        if mode=="bb":
            output+=f"{lo.Boll_Band(sort_list[i])} :\n\n"
    result_text2.config(state="normal")  
    result_text2.delete("1.0", tk.END)
    result_text2.insert("1.0", output)
    result_text2.config(state="disabled")

def index_analyze():
    string=entry3.get().upper()
    analys_list=[]
    if string=="OMX30":
        analys_list=so.omx30()
    if string=="SP500":
        analys_list=so.get_sp500_list()
    
    analys = so.list_analys(analys_list)
    output="    ---Found---\n"
    for i in range(len(analys[0])):
        output+=f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output+=f"{analys[1][i][x]}\n"
        output+="\n"
    for i in range(len(analys[0])):
        output+=f"{analys[0][i]} "
    
    result_text3.config(state="normal")  
    result_text3.delete("1.0", tk.END)
    result_text3.insert("1.0", output)
    result_text3.config(state="disabled")  


def show_single_analyze():
    index_frame.pack_forget()
    list_frame.pack_forget()
    best_frame.pack_forget()
    single_frame.pack(padx=10, pady=10)

def show_list_analyze():
    index_frame.pack_forget()
    single_frame.pack_forget()
    best_frame.pack_forget()
    list_frame.pack(padx=10, pady=10)

def show_index_analyze():
    list_frame.pack_forget()
    single_frame.pack_forget()
    best_frame.pack_forget()
    index_frame.pack(padx=10, pady=10)

def show_best_analyze():
    list_frame.pack_forget()
    single_frame.pack_forget()
    index_frame.pack_forget()
    best_frame.pack(padx=10, pady=10)
    

    


# GUI setup
root = tk.Tk()
root.title("Stock Analyzer")

#knappar
top_button_frame = tk.Frame(root)
top_button_frame.pack(pady=10)

tk.Button(top_button_frame, text="Single Analyze", command=show_single_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="List Analyze", command=show_list_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="Index Analyze", command=show_index_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="best stock", command=show_best_analyze).pack(side="left", padx=5)



#single analys
single_frame = tk.Frame(root)

tk.Label(single_frame, text="Enter Ticker Symbol:").pack(pady=5)
entry = tk.Entry(single_frame, width=30)
entry.pack(pady=5)

tk.Button(single_frame, text="Analyze", command=run_single_analysis).pack(pady=10)

result_label = tk.Label(single_frame, text="", justify="left", wraplength=400)
result_label.pack(padx=10, pady=10)

#list analys
list_frame = tk.Frame(root)
tk.Label(list_frame, text="Enter list e.g: AAPL NVDA MSFT").pack()
entry2 = tk.Entry(list_frame, width=30)
entry2.pack(pady=5)

tk.Button(list_frame, text="Analyze", command=run_list_analysis).pack(pady=10)
tk.Button(list_frame, text="sort rsi", command=lambda: sortera("rsi")).pack(pady=10)
tk.Button(list_frame, text="sort bbu", command=lambda: sortera("bb")).pack(pady=10)

result_frame2 = tk.Frame(list_frame)
result_frame2.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar2 = tk.Scrollbar(result_frame2)
scrollbar2.pack(side="right", fill="y")
result_text2 = tk.Text(result_frame2, wrap="word", yscrollcommand=scrollbar2.set, height=15, width=30)
result_text2.pack(side="left", fill="both", expand=True)
scrollbar2.config(command=result_text2.yview)


#index analys
index_frame = tk.Frame(root)
tk.Label(index_frame, text="välj indexlista |OMX30, SP500|").pack()
entry3 = tk.Entry(index_frame, width=30)
entry3.pack(pady=5)

tk.Button(index_frame, text="Analyze", command=index_analyze).pack(pady=10)

result_frame3 = tk.Frame(index_frame)
result_frame3.pack(padx=10, pady=10, fill="both", expand=True)
scrollbar3 = tk.Scrollbar(result_frame3)
scrollbar3.pack(side="right", fill="y")
result_text3 = tk.Text(result_frame3, wrap="word", yscrollcommand=scrollbar3.set, height=15, width=30)
result_text3.pack(side="left", fill="both", expand=True)
scrollbar3.config(command=result_text3.yview)


#bästa aktien 
best_frame = tk.Frame(root)
tk.Label(best_frame, text="whil finde the best stock\n input exemple |AAPL NVDA MSFT|").pack()
entry4 = tk.Entry(best_frame, width=30)
entry4.pack(pady=5)

tk.Button(best_frame, text="Analyze", command=run_best_analysis).pack(pady=10)

result_label4 = tk.Label(best_frame, text="", justify="left", wraplength=400)
result_label4.pack(padx=10, pady=10)


root.mainloop()