import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def total(merchant):
    idx = withdrawals['Clean Description'] == merchant
    return (merchant, withdrawals[idx]['Amount'].sum())

data = pd.DataFrame.from_csv('clean_transactions.csv')

idx = data['Amount'] < 0
withdrawals = data[idx]

merchants = np.unique(data['Clean Description'])
merchant_spending = map(total, merchants)
sorted_merchants = pd.DataFrame(merchant_spending, columns=['Merchant', 'Total']).sort(['Total'], ascending=True)
