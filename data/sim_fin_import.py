import simfin as sf 

sf.set_api_key('c98a6aa1-8571-4012-8c33-12456c0419f8')
sf.set_data_dir('../data/simfin_data/')
df_income = sf.load_income(variant='quarterly', market='us')
df_cashflow = sf.load_cashflow(variant='quarterly', market='us')
df_balance = sf.load_balance(variant='quarterly', market='us')
#print(df_income.columns)
#print(df_cashflow.columns)
print(df_balance.loc['AAPL'])
