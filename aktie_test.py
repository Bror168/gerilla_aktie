import yfinance as yf

def get_ohlc_data(ticker_symbol, period="5d", interval="1d"):
    """
    Hämtar OHLC-data för den angivna aktien.

    :param ticker_symbol: Aktiens ticker-symbol (t.ex. "AAPL")
    :param period: Tidsperiod att hämta data för (t.ex. "10d" = 10 dagar)
    :param interval: Tidsintervall per datapunkt (t.ex. "1d" = daglig data)
    :return: DataFrame med OHLC-data
    """
    stock = yf.Ticker(ticker_symbol)
    data = stock.history(period=period, interval=interval)
    return data

if __name__ == "__main__":
    ticker = "ATCO-B.ST"  # Ändra till önskad ticker om du vill ha data för en annan aktie
    ohlc_data = get_ohlc_data(ticker)
    
    if not ohlc_data.empty:
        print(f"OHLC-data för {ticker}:")
        print(ohlc_data)
    else:
        print("Ingen data kunde hämtas.")
