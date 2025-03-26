import streamlit as st
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# JDKDCP93LFYX0C9K
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo'
r = requests.get(url)

def get_stock_data(ticker: str):
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
    else:
        st.error("Error fetching data. Check the ticker symbol or API key.")
        return None

# plot creation
def plot_stock_data(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df["Close"], label="Close price", color="blue")
    plt.plot(df.index, df["Close"].rolling(window=10).mean(), label="10-days average", linestyle="dashed", color="red")
    plt.plot(df.index, df["Close"].rolling(window=50).mean(), label="50-days average", color="green")
    plt.plot(df.index, df["Close"].rolling(window=200).mean(), label="200-days average", color="purple")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(f"Graph {symbol}")
    plt.legend()
    st.pyplot(plt)

st.title("📈 Finance analysis")
st.sidebar.header("Settings")

ticker = st.sidebar.text_input("Type share ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", datetime.date(2000, 1, 1), format='DD/MM/YYYY', min_value=datetime.date(2000, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today(), format='DD/MM/YYYY', min_value=datetime.date(2000, 1, 1))
if st.sidebar.button("Load data"):
    df = get_stock_data(ticker)
    if df is not None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df = df[(df.index >= start_date) & (df.index <= end_date)]
        plot_stock_data(df, ticker)