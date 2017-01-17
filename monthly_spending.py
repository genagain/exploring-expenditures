import pandas as pd
import numpy as np
import ipdb

def monthly_total(month):
   idx = withdrawals["Month"] == month
   return (month, withdrawals[idx]["Amount"].sum())

data = pd.DataFrame.from_csv('clean_transactions.csv')

idx = data['Amount'] < 0
withdrawals = data[idx]

months = withdrawals.index.month
withdrawals.loc[:,('Month')] = months
uniq_months = np.unique(months)

monthly_totals = map(lambda m: monthly_total(m), uniq_months)
monthly_totals_df = pd.DataFrame(monthly_totals, columns=['Month', 'Total'])
