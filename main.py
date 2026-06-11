import pandas as pd
import yfinance as yf
import time
import os
from pathlib import Path

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
    df_merged["Publish Date"] = pd.to_datetime(df_merged["Publish Date"])

    TICKERS = list(df_merged["Ticker"].unique())
    
    df_prices = pd.read_csv("./data/prices.csv", index_col=0, parse_dates=True)
    df_prices_clean = df_prices.dropna(axis=1, how="any")
    
    prices_long = (
        df_prices_clean.reset_index()
          .melt(id_vars='Date',
                var_name='Ticker',
                value_name='Price')
    )

    #TODO:  Använd Publish Date för matchning med pris/inputs 
    prices_long = prices_long.sort_values(by=["Date", "Ticker"])
    df_merged = df_merged.sort_values(by=["Publish Date", "Ticker"])

    df = pd.merge_asof(df_merged, prices_long, left_on="Publish Date", right_on="Date", by="Ticker", direction="backward")
    print(df[df["Ticker"] == "AAPL"]["Publish Date"])

    #TODO: Implementera ratios och LTM-kolumner för rådata som aggregeras (kassaflöde, vinst, omsättning exv.)
    # Bygg sedan 
    
    tickers_complete = list(df_prices_clean.columns)
    df_merged_filtered = df_merged[df_merged["Ticker"].isin(tickers_complete)]
    
