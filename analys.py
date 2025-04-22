import logic as lo
import sok as so
import tkinter as tk
from tkinter import messagebox

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
    print(aktie_list)
    aktie_list=analys[0]
    print(aktie_list)
    
    output="---Found---\n"
    for i in range(len(analys[0])):
        output+=f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output+=f"{analys[1][i][x]}\n"
        output+="\n"
    result_label2.config(text=output)

def sortera(mode):
    global aktie_list
    print(aktie_list)
    sort_list=[]
    if mode=="rsi":
        sort_list=so.sort_BB(aktie_list)
    if mode=="bb":
        sort_list=so.sort_BB(aktie_list)

    aktie_list=sort_list

    output="---Found---\n"
    for i in range(len(sort_list)):
        output+=f"{sort_list[i]} :\n"
        if mode=="rsi":
            output+=f"{lo.calc_rsi(lo.get_ohlc_data(sort_list[i]))} :\n\n"
        if mode=="bb":
            output+=f"{lo.Boll_Band(sort_list[i])} :\n\n"
    result_label2.config(text=output)

def index_analyze():
    string=entry3.get().upper()
    analys_list=[]
    if string=="OMX30":
        print(2)
        analys_list=so.omx30()
    if string=="SP500":
        analys_list=so.get_sp500_list()
    
    print(analys_list)
    analys = so.list_analys(analys_list)
    print(analys)
    output="---Found---\n"
    for i in range(len(analys[0])):
        output+=f"{analys[0][i]} :\n"
        for x in range(len(analys[1][i])):
            output+=f"{analys[1][i][x]}\n"
        output+="\n"
    
    result_text3.config(state="normal")  
    result_text3.delete("1.0", tk.END)
    result_text3.insert("1.0", output)
    result_text3.config(state="disabled")  


def show_single_analyze():
    index_frame.pack_forget()
    list_frame.pack_forget()
    single_frame.pack(padx=10, pady=10)

def show_list_analyze():
    index_frame.pack_forget()
    single_frame.pack_forget()
    list_frame.pack(padx=10, pady=10)

def show_index_analyze():
    list_frame.pack_forget()
    single_frame.pack_forget()
    index_frame.pack(padx=10, pady=10)
    

    


# GUI setup
root = tk.Tk()
root.title("Stock Analyzer")

#knappar
top_button_frame = tk.Frame(root)
top_button_frame.pack(pady=10)

tk.Button(top_button_frame, text="Single Analyze", command=show_single_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="List Analyze", command=show_list_analyze).pack(side="left", padx=5)
tk.Button(top_button_frame, text="Index Analyze", command=show_index_analyze).pack(side="left", padx=5)


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

result_label2 = tk.Label(list_frame, text="", justify="left", wraplength=400)
result_label2.pack(padx=10, pady=10)


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





root.mainloop()

