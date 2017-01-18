import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipdb

def monthly_total(month):
   idx = withdrawals["Month"] == month
   return (month, abs(withdrawals[idx]["Amount"].sum()))

data = pd.DataFrame.from_csv('clean_transactions.csv')

idx = data['Amount'] < 0
withdrawals = data[idx]

months = withdrawals.index.month
month_labels = withdrawals.index.strftime('%B')
withdrawals.loc[:,('Month')] = months
uniq_months = np.unique(months)
uniq_month_labels = np.unique(month_labels)

monthly_totals = map(lambda m: monthly_total(m), uniq_months)
monthly_totals_df = pd.DataFrame(monthly_totals, columns=['Month', 'Total'])

fig = plt.figure()

ax = fig.add_subplot(111)

plt.bar(monthly_totals_df['Month'], monthly_totals_df['Total'], align='center')
plt.xticks(monthly_totals_df['Month'], uniq_month_labels)
ax.set_title('Withdrawals by month')
ax.set_xlabel('Months')
ax.set_ylabel('Withdrawals ($)')

plt.show()
