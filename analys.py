import logic as lo
import sok as so
import tkinter as tk
from tkinter import messagebox

def run_single_analysis(): 
    ticker = entry.get().upper()
    rsi = lo.calc_rsi(so.get_ohlc_data(ticker))
    boll = lo.Boll_Band(ticker)
    analysis = so.single_analys(ticker)

    output = f"RSI:\n{rsi}\n\nBollinger Bands:\n{boll}\n\nFormationer:\n{analysis[0]}"
    result_label.config(text=output)

def run_list_analysis():
    string=entry.get().upper()
    analys_list=[]
    split=0
    for i in range(len(string)):
        if string[i]==" ":
            analys_list.append(string[split:i])
            split=i+1
        if i+1==len(string):
            analys_list.append(string[split:i+1])

    print(analys_list)
    analys = so.list_analys(analys_list)
    print(analys)

def show_single_analyze():
    list_frame.pack_forget()
    single_frame.pack(padx=10, pady=10)

def show_list_analyze():
    single_frame.pack_forget()
    list_frame.pack(padx=10, pady=10)

# GUI setup
root = tk.Tk()
root.title("Stock Analyzer")

#knappar
tk.Button(root, text="single Analyze", command=show_single_analyze).pack(pady=10)
tk.Button(root, text="list Analyze", command=show_list_analyze).pack(pady=10)

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
entry = tk.Entry(list_frame, width=30)
entry.pack(pady=5)
tk.Button(list_frame, text="Analyze", command=run_list_analysis).pack(pady=10)


root.mainloop()
