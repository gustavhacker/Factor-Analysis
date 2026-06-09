import pandas as pd
import json

def load_json(path):
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    df_income = pd.read_csv("./data/us-income-quarterly.csv", sep = ";")
    df_cash = pd.read_csv("./data/us-cashflow-quarterly.csv", sep = ";")
    df_balance = pd.read_csv("./data/us-balance-quarterly.csv", sep = ";")

    
    print("Diff balance - income")
    print(set(df_balance['Ticker'].unique()) - set(df_income['Ticker'].unique()))
    print("Diff income - cash")
    print(set(df_income['Ticker'].unique()) - set(df_cash['Ticker'].unique()))
    print("Diff balance - cash")
    print(set(df_balance['Ticker'].unique()) - set(df_cash['Ticker'].unique()))