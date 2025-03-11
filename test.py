import pandas as pd

def get_omxs30_companies():
    url = "https://en.wikipedia.org/wiki/OMX_Stockholm_30"
    df_list = pd.read_html(url)
    omxs30_df = df_list[1]  # Justera indexet om det behövs
    companies = omxs30_df[["Company", "Symbol"]]
    return companies

companies = get_omxs30_companies()
omx_list=[]
for index, row in companies.head(30).iterrows():
    symbol = row["Symbol"]
    ny_symbol=""
    for i in range(len(symbol)):
        if symbol[i]==" ":
            ny_symbol+="-"
        else:
            ny_symbol+=symbol[i]
    print(f"{ny_symbol}"+".ST")
    omx_list.append(ny_symbol +".ST")
print(omx_list)

