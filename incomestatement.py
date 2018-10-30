import numpy as np
import pandas as pd


def get_income(transactions):
    idx = transactions.category == 'paycheck'
    income = transactions[idx].amount.sum()
    return np.round(income, 2)

def get_transportation_expenses(transactions):
    idx = transactions.original_description.str.contains('LYFT')
    expenses = transactions[idx].amount.sum()
    return np.round(expenses, 2)

def get_net_qapital_savings(transactions):
    withdrawal_idx = transactions.original_description.str.contains('QAPITAL') & transactions.category.isin(['savings', 'deposit'])
    withdrawals = transactions[withdrawal_idx].amount.sum()
    deposits_idx = transactions.original_description.str.contains('QAPITAL') & transactions.category.isin(['income', 'transfer'])
    deposits = transactions[deposits_idx].amount.sum()
    return np.round(withdrawals - deposits)

def get_net_savings(transactions):
    qapital_savings = get_net_qapital_savings(transactions)
    vanguard_idx = transactions.original_description.str.contains('VANGUARD')
    vanguard_savings = transactions[vanguard_idx].amount.sum()
    business_idx = (transactions.original_description.str.contains('Online scheduled transfer from CHK 4604')) & (transactions.account_name == 'Business Fundamentals Chk')
    business_investment = transactions[business_idx].amount.sum()
    return np.round(qapital_savings + vanguard_savings + business_investment)

def get_credit_card_expenses(transactions):
    idx = transactions.account_name == 'nRewards Visa'
    expenses = transactions[idx].amount.sum()
    return np.round(expenses, 2)

def get_net_venmo(transactions):
    withdrawal_idx = transactions.original_description.str.contains('VENMO DES:PAYMENT')
    withdrawals = transactions[withdrawal_idx].amount.sum()
    deposits_idx = transactions.original_description.str.contains('VENMO DES:CASHOUT')
    deposits = transactions[deposits_idx].amount.sum()
    return np.round(deposits - withdrawals)

def get_utilities(transactions):
    idx = (transactions.account_name == 'Bills') & (transactions.original_description.str.contains('COMCAST|EVERSOURCE'))
    expenses = transactions[idx].amount.sum()
    return np.round(expenses, 2)
