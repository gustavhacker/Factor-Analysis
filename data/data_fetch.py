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

#-------------------------------
#Ladda ned priser från finance med delay för at undvika bir rate limits
#Behöver imports för att det ska funka, kolla path också

START        = "2019-12-01"
END          = "2026-02-28"
INTERVAL     = "1mo"
BATCH_SIZE   = 100            # yfinance handles ~100 tickers well per call
SLEEP_BETWEEN_BATCHES = 3     # seconds; increase to 5–8 if you still get 429s
OUTPUT_DIR   = Path("data")
OUTPUT_FILE  = OUTPUT_DIR / "prices.csv"
# ────────────────────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(exist_ok=True)

def download_batch(batch: list[str], attempt: int = 1) -> pd.DataFrame | None:
    """Download one batch, with exponential back-off on failure."""
    try:
        df = yf.download(
            batch,
            start=START,
            end=END,
            interval=INTERVAL,
            auto_adjust=False,
            progress=False,
        )["Adj Close"]
        # yfinance returns a Series (not DataFrame) when only 1 ticker succeeds
        if isinstance(df, pd.Series):
            df = df.to_frame(name=batch[0])
        return df
    except Exception as e:
        if attempt <= 4:
            wait = 2 ** attempt * 10      # 20s, 40s, 80s, 160s
            print(f"  ⚠ Attempt {attempt} failed ({e}). Retrying in {wait}s…")
            time.sleep(wait)
            return download_batch(batch, attempt + 1)
        print(f"  ✗ Batch failed after 4 attempts: {batch[:3]}…")
        return None

# Split into batches
batches = [TICKERS[i:i + BATCH_SIZE] for i in range(0, len(TICKERS), BATCH_SIZE)]
print(f"Downloading {len(TICKERS)} tickers in {len(batches)} batches of {BATCH_SIZE}…\n")

all_frames = []

for i, batch in enumerate(batches, 1):
    print(f"Batch {i}/{len(batches)}  ({batch[0]} … {batch[-1]})")
    df = download_batch(batch)
    if df is not None and not df.empty:
        all_frames.append(df)
    if i < len(batches):
        time.sleep(SLEEP_BETWEEN_BATCHES)

# Combine & save
print("\nCombining and writing to CSV…")
prices = pd.concat(all_frames, axis=1)
prices.index = pd.to_datetime(prices.index)
prices.sort_index(inplace=True)
prices.to_csv(OUTPUT_FILE)

print(f"Done. Shape: {prices.shape}")
print(f"Saved → {OUTPUT_FILE.resolve()}")
    