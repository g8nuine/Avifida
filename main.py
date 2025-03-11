import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# JDKDCP93LFYX0C9K
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo'
r = requests.get(url)

def get_stock_data(ticker):
    params = {
        "function": "TIME_SERIES_WEEKLY",
        "symbol": ticker,
        "apikey": "JDKDCP93LFYX0C9K",
        "outputsize": "compact"
    }
    response = requests.get("https://www.alphavantage.co/query", params=params)
    data = response.json()
    if "Weekly Time Series" in data:
        df = pd.DataFrame.from_dict(data["Weekly Time Series"], orient="index")
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        return df

# plot creation
def plot_stock_data(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Close"], label="Close price", color="blue")
    plt.plot(df.index, df["Close"].rolling(window=10).mean(), label="10-days average", linestyle="dashed", color="red")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(f"Graph {symbol}")
    plt.legend()
    st.pyplot(plt)

st.title("📈 Finance analysis")
st.sidebar.header("Settings")

ticker = st.sidebar.text_input("Type share ticker", "AAPL")
if st.sidebar.button("Load data"):
    df = get_stock_data(ticker)
    if df is not None:
        plot_stock_data(df, ticker)