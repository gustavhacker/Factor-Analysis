import time
import pandas as pd
import requests
import json

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Successfully saved to {filename}")

tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NVDA', 'JPM', 'JNJ','PG', 'NFLX', 'CRM',
        'ADBE', 'PYPL', 'ORCL', 'INTC', 'CSCO', 'TXN', 'AVGO', 'QCOM', 'BAC', 'WFC', 'C', 'GS', 
        'MS', 'AXP', 'BLK', 'PNC', 'USB', 'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'GE', 'CAT', 'HON',
        'MMM', 'BA', 'UNP', 'KO', 'PEP', 'MCD', 'SBUX', 'NKE', 'HD', 'LOW', 'TGT', 'WMT', 'PFE']

test_tickers = ['AAPL']#, 'MSFT', 'AMZN', 'GOOGL', 'META']

for ticker in test_tickers: 
    url_income = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey=ITBVCUIP3HPRI53K'
    url_balance = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey=ITBVCUIP3HPRI53K'
    url_cashflow = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey=ITBVCUIP3HPRI53K'
    
    r_income = requests.get(url_income)
    data_income = r_income.json()
    save_json(data_income, 'income_statement.json')
    time.sleep(12)
    
    r_balance = requests.get(url_balance)
    data_balance = r_balance.json()
    save_json(data_balance, 'balance_sheet.json')
    time.sleep(12)
    
    r_cashflow = requests.get(url_cashflow)
    data_cashflow = r_cashflow.json()
    save_json(data_cashflow, 'cash_flow.json')
    time.sleep(12)
    