# ----------------------------------------------------
# Gerilla Aktie – © 2025 Bror168
# Skapad av Bror168 (https://github.com/Bror168)
# Denna kod är skyddad enligt MIT-licensen.
# All kopiering utan erkännande är förbjuden.
# Version: 1.0.0
# ----------------------------------------------------

import yfinance as yf
import pandas as pd
import numpy as np
import math

def quick_sort(arr):
    # Rekursiv implementation av quicksort-algoritmen
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # Välj mitt-elementet som pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def get_ohlc_data(ticker_symbol, period="5d", interval="1d"):
    # Hämtar OHLC-data (Open, High, Low, Close) för en given aktie
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data

def calc_rsi(data, period=2):
    #rsi calculatorn funkar ish brukar vara 2-3% för mycket/för lite 
    # gämfört med avanzas rsi calculator. Men är tillräkkligt när aför mitt ändamål.
    #RSI = 100 – (100/1+RS) RS=genomsnitlig vinst/förlust på n dagar
    series = data["Close"]
    delta = series.diff().dropna()

    u = np.where(delta > 0, delta, 0)
    d = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(u[:period])  
    avg_loss = np.mean(d[:period])  
    # Initiera medelvärden innan EMA-beräkning
    u = np.concatenate(([avg_gain], u[period:]))
    d = np.concatenate(([avg_loss], d[period:]))
    rs = pd.Series(u).ewm(com=period-1, adjust=False).mean() / \
         pd.Series(d).ewm(com=period-1, adjust=False).mean()
    
    # Returnerar RSI-värde för andra dagen
    return 100 - 100 / (1 + rs[2]) 

def SMA20(ticker_symbol, dag):  # dag=1 är idag
    # Beräknar 20-dagars glidande medelvärde (Simple Moving Average)
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period="2mo", interval="1d")
    close_list = data["Close"].tolist()
    return sum(close_list[-20-dag : -dag]) / 20

def Boll_Band(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="2mo", interval="1d")
    close_list = data["Close"].tolist()
    
    period_closes = close_list[-20: ]
    # Beräknar medelvärdet (SMA20)
    mean = sum(period_closes) / len(period_closes)

    #räknar ut diviation från sma20
    squared_diffs = [(price - mean) ** 2 for price in period_closes]
    variance = sum(squared_diffs) / (len(period_closes) - 1)
    # Standardavvikelse (sample std)
    std_dev = math.sqrt(variance)
    upper_band = mean + (2 * std_dev)
    lower_band = mean - (2 * std_dev)
    # Returnerar kvoten (mått på avståndet mellan banden)
    return upper_band/lower_band


# Funktion som returnerar en lista med True/False baserat på om priset ökat
# under olika tidsperioder: 5 dagar, 1 månad, 3 månader
def roc(ticker):
    roc_list = []  # Lista som kommer innehålla True/False för varje period
    stock = yf.Ticker(ticker)
    # --- 5 dagar ---
    data = stock.history(period="5d", interval="1d")["Close"].tolist()
    # Jämför senaste stängningskurs med den första
    if data[-1] > data[0]:
        roc_list.append("roc5")
    # --- 1 månad ---
    data = stock.history(period="1mo", interval="1d")["Close"].tolist()
    if data[-1] > data[0]:
        roc_list.append("roc")
    # --- 3 månader ---
    data = stock.history(period="3mo", interval="1d")["Close"].tolist()
    if data[-1] > data[0]:
        roc_list.append("roc66")
    # Returnerar en lista med tre boolska värden som visar om aktien gått upp
    # över 5 dagar, 1 månad och 3 månader (i den ordningen)
    return roc_list

# Beräknar SMA (Simple Moving Average) för en viss dag bakåt
def SMA(ticker_symbol, period, day):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=f"{period}d", interval="1d")
    close_list = data["Close"].tolist()
    # Kontrollera att det finns tillräckligt med data
    if len(close_list) < period + day:
        raise ValueError("För lite data för att räkna ut SMA.")
    # Tar ett snitt på 'period' antal dagar, med 'day' förskjutning bakåt
    return sum(close_list[-period-day:-day]) / period

# Kollar om dagens range (högsta - lägsta) är minst dubbelt så stor som någon av de senaste 10 dagarna (exkl. idag)
def dgr10_2(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period="1mo", interval="1d")
    # Beräknar dagens range
    today_range = data["High"].iloc[-1] - data["Low"].iloc[-1]
    # Jämför med de föregående 10 dagarnas range
    for i in range(2, 12):  # Börjar på 2 för att undvika att jämföra med dagens range
        day_range = data["High"].iloc[-i] - data["Low"].iloc[-i]
        if today_range >= 2 * day_range:
            return True

    return False

# Kollar om dagens volym är minst dubbelt så stor som någon av de senaste 10 dagarna (exkl. idag)
def range_dubble(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period="1mo", interval="1d")
    # Hämtar dagens volym
    today_volume = data["Volume"].iloc[-1]
    # Jämför med de föregående 10 dagarnas volym
    for i in range(2, 12):  # Börjar på 2 för att undvika att jämföra med idag
        day_volume = data["Volume"].iloc[-i]
        if today_volume >= 2 * day_volume:
            return True
    return False


def spik_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #closing är lägre än igår
    if not close_list[-1]<close_list[-2]:
        san=False

    return san
    
def reversal_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #closing är högre än igår
    if not close_list[-1]>close_list[-2]:
        san=False
    #closing är lägre än gårdagens high
    if not close_list[-1]<high_list[-2]:
        san=False
    
    return san

def key_reversal_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #closing är högre än igår
    if not close_list[-1]>close_list[-2]:
        san=False

    return san

def pattern_gap_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    # lägsta kurs ligger mellan gårdagens stägning och högsta notering 
    if not low_list[-1]>close_list[-2] and low_list[-1]<high_list[-2]:
        san=False
    # stägning ligger över gårdagens högsta och stägning för 2 dgr sen
    if not close_list[-1]>high_list[-2] and close_list[-1]>close_list[-3]:
        san=False

    return san

def reversal_gap_formation(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #dagens low är över gårdagens high
    if not low_list[-1]>high_list[-2]:
        san=False
    #Om stängningen idag inte är högre än både gårdagens och för-gårdagens stängning
    if not close_list[-1]>close_list[-2] and close_list[-1]>close_list[-3]:
        san= False
    return san


def ett80_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #kollar 5dgr låg
    for i in range(len(low_list)-2):
        if low_list[-1]>low_list[i]:
            san=False
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #gårdagen stänger i undre 1/4
    if (close_list[-2]-low_list[-2])/(high_list[-2]-low_list[-2])>0.25:
        san=False

    return san

def interference_form(data):
    close_list = data["Close"].tolist()
    open_list = data["Open"].tolist()
    san=True
    # stägning för 4 ddg sen är negativ
    if (close_list[-5]-open_list[-5])>0:
        san=False
    #stägning för 3 dagar sen är posetiv
    if (close_list[-4]-open_list[-4])<0:
        san=False
    #stägningen för förgår, igår o idag är negativ
    if (close_list[-3]-open_list[-3])>0 and (close_list[-2]-open_list[-2])>0 and (close_list[-1]-open_list[-1])>0:
        san=False

    return san

def holy_grail_form(data, ticker):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    sma=SMA20(ticker, 1)
    san=True
    #lägsta notering är under sma20
    if not low_list[-1]<sma:
        san=False
    #stägning över sma20 
    if not close_list[-1]>sma:
        san=False
    #stägning i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    #sma20 är stigande
    if not SMA20(ticker, 1)>SMA20(ticker, 5):
        san=False
    #gårdagens lägsta ör störe än sma20
    if not low_list[-2]>SMA20(ticker, 2):
        san=False
    return san

def Riko_form(data):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    # stänger i undre 1/10 av dagens spann
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])>0.1:
        san=False
    return san

def impuls_form(data, ticker):
    close_list = data["Close"].tolist()
    high_list = data["High"].tolist()
    low_list = data["Low"].tolist()
    san=True
    #stänger i övre 1/4
    if (close_list[-1]-low_list[-1])/(high_list[-1]-low_list[-1])<0.75:
        san=False
    # dagens kursrörelse är minst dubbelt så stor som någon av de senaste 10 dagarna
    if not dgr10_2(ticker):
        san=False
    # dagens volym är minst dubbelt så stor som någon av de senaste 10 dagarna
    if not range_dubble(ticker):
        san=False
    return san

#kod skriven av chat gpt, då de va för många kriter för formationen och jag orkade inte göra det :)
def fort_form(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="60d", interval="1d")
    #om gårdagens högsta är större än högsta för dagarna 6 eller 11 dagar tillbaka, returnera False
    if data["High"].iloc[-2] >= data["High"].iloc[-11] or data["High"].iloc[-2] >= data["High"].iloc[-6]:
        return False
    #om gårdagens lägsta är lägre än lägsta för dagarna 6 eller 11 dagar tillbaka, returnera False
    if data["Low"].iloc[-2] <= data["Low"].iloc[-11] or data["Low"].iloc[-1] <= data["Low"].iloc[-6]:
        return False
    # Hämtar SMA20 och SMA50
    sma20 = SMA20(ticker, 1)
    sma50 = SMA(ticker, 50, 1)
    #SMA20 måste vara större än SMA50 för att vara en positiv trend
    if not sma20 > sma50:
        return False
    #SMA50 ska vara stigande (nuvarande SMA50 ska vara större än SMA50 för 5 dagar sen)
    if not SMA(ticker, 50, 1) > SMA(ticker, 50, 5):
        return False
    #dagens stängning ska vara över den högsta nivån de senaste 5 dagarna
    highest_last_5 = max(data["High"].iloc[-6:-1])
    if data["Close"].iloc[-1] <= highest_last_5:
        return False
    #dagens range ska vara åtminstone 1.5 gånger genomsnittet av de senaste 10 dagarnas range
    today_range = data["High"].iloc[-1] - data["Low"].iloc[-1]
    avg_range_10 = sum(data["High"].iloc[-11:-1] - data["Low"].iloc[-11:-1]) / 10
    if today_range <= 1.5 * avg_range_10:
        return False
    #dagens volym ska vara åtminstone 1.5 gånger genomsnittlig volym för de senaste 10 dagarna
    today_volume = data["Volume"].iloc[-1]
    avg_volume_10 = sum(data["Volume"].iloc[-11:-1]) / 10
    if today_volume <= 1.5 * avg_volume_10:
        return False
    # Om alla kriterier uppfylls, returnera True
    return True