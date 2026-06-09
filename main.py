import pandas as pd
import yfinance as yf

if __name__ == "__main__":
    df_income = pd.read_csv("./data/us-income-quarterly.csv", sep = ";")
    df_cash = pd.read_csv("./data/us-cashflow-quarterly.csv", sep = ";")
    df_balance = pd.read_csv("./data/us-balance-quarterly.csv", sep = ";")

    
    """print("Diff balance - income")
    print(set(df_balance['Ticker'].unique()) - set(df_income['Ticker'].unique()))
    print("Diff income - cash")
    print(set(df_income['Ticker'].unique()) - set(df_cash['Ticker'].unique()))
    print("Diff balance - cash")
    print(set(df_balance['Ticker'].unique()) - set(df_cash['Ticker'].unique()))"""

    df_merged = (
        df_income
        .merge(df_cash, on=["Ticker", "Fiscal Year", "Fiscal Period"], how="inner")
        .merge(df_balance, on=["Ticker", "Fiscal Year", "Fiscal Period"], how="inner")
    )

    tickers = list(df_merged["Ticker"].unique())
    prices = yf.download(tickers, start="2019-12-01", end="2026-02-30", interval="1m")["Adj Close"]
    print(prices["AAPL"])

    #TODO: Loopa över X antal tickers och spara ned till CSV-fil saå det bara behöver göras en gång