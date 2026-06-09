import pandas as pd
import json

def load_json(path):
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    balance = load_json("./jsonfiles/balance_sheet.json")
    cash = load_json("./jsonfiles/cash_flow.json")
    income = load_json("./jsonfiles/income_statement.json")

    df = pd.read_json("./jsonfiles/balance_sheet.json")
    print(df)