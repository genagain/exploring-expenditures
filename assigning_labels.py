import pandas as pd
import incomestatement

transactions = pd.read_csv('manually_assigning_every_transaction_november.csv')

transactions['Automatic Label'] = ''

# This needs to go before getting investments
idx = incomestatement.get_transfers(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Transfer'

idx = incomestatement.get_overdraft_no_fees(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Overdraft'

idx = incomestatement.get_unnecessary_fees(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Fee'

idx = incomestatement.get_nfcu_payments(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Credit Card Payment'

idx = incomestatement.get_savings_goals(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Savings Goal'

idx = incomestatement.get_income(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Income'

vanguard_savings, business_investment = incomestatement.get_investments(transactions, return_selected=True)
transactions.loc[transactions.index.isin(list(vanguard_savings.index)), 'Automatic Label'] = 'Investment'
transactions.loc[transactions.index.isin(list(business_investment.index)), 'Automatic Label'] = 'Investment'

idx = incomestatement.get_discretionary_spending(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Spending Money'

idx = incomestatement.get_fixed_costs(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Fixed Cost'

withdrawals, deposits = incomestatement.get_net_qapital_savings(transactions, return_selected=True)
transactions.loc[transactions.index.isin(list(withdrawals.index)), 'Automatic Label'] = 'Qapital'
transactions.loc[transactions.index.isin(list(deposits.index)), 'Automatic Label'] = 'Qapital'

venmo_deposits, _ = incomestatement.get_net_venmo(transactions, return_selected=True)
transactions.loc[transactions.index.isin(list(venmo_deposits.index)), 'Automatic Label'] = 'Venmo Deposit'

idx = incomestatement.get_debitize_payments(transactions, return_selected=True).index
transactions.loc[transactions.index.isin(list(idx)), 'Automatic Label'] = 'Debitize'

transactions.to_csv('automatically_assigning_every_transaction_november.csv')

