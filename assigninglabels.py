import pandas as pd
import incomestatement
from datetime import datetime

def label(transactions, timeframe):
  transactions['automatic_label'] = ''

  transactions = transactions.drop('description', axis=1)
  transactions = transactions.drop('transaction_type', axis=1)

  # This needs to go before getting investments
  idx = incomestatement.get_transfers(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Transfer'

  idx = incomestatement.get_overdraft_no_fees(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Overdraft'

  idx = incomestatement.get_unnecessary_fees(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Fee'

  idx = incomestatement.get_nfcu_payments(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Credit Card Payment'

  idx = incomestatement.get_savings_goals(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Savings Goal'

  idx = incomestatement.get_income(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Income'

  vanguard_savings, business_investment = incomestatement.get_investments(transactions, return_selected=True)
  transactions.loc[transactions.index.isin(list(vanguard_savings.index)), 'automatic_label'] = 'Investment'
  transactions.loc[transactions.index.isin(list(business_investment.index)), 'automatic_label'] = 'Investment'

  idx = incomestatement.get_discretionary_spending(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Spending Money'

  idx = incomestatement.get_fixed_costs(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Fixed Cost'

  withdrawals, deposits = incomestatement.get_net_qapital_savings(transactions, return_selected=True)
  transactions.loc[transactions.index.isin(list(withdrawals.index)), 'automatic_label'] = 'Qapital'
  transactions.loc[transactions.index.isin(list(deposits.index)), 'automatic_label'] = 'Qapital'

  venmo_deposits, _ = incomestatement.get_net_venmo(transactions, return_selected=True)
  transactions.loc[transactions.index.isin(list(venmo_deposits.index)), 'automatic_label'] = 'Venmo Deposit'

  idx = incomestatement.get_debitize_payments(transactions, return_selected=True).index
  transactions.loc[transactions.index.isin(list(idx)), 'automatic_label'] = 'Debitize'

  today = datetime.today()
  output_file = '{}_maintainance_{}_{}_{}.csv'.format(timeframe.replace(' ', '_'), today.day, today.month, today.year)
  transactions.to_csv(output_file, index=False)

