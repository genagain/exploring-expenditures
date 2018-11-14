from collections import OrderedDict

import numpy as np
import pandas as pd
from config import OPTIMAL_BREAKDOWN

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

def get_net_qapital_breakdown(transactions):
    residual_savings = get_net_qapital_savings(transactions)

    breakdown = OrderedDict([ (category, 0) for category in OPTIMAL_BREAKDOWN.keys() ])
    for category, amount in OPTIMAL_BREAKDOWN.iteritems():
        if residual_savings >= amount:
            breakdown[category] = amount
            residual_savings -= amount
        else:
            breakdown[category] = residual_savings
            return breakdown

    return breakdown

def get_investments(transactions):
    qapital_investments= get_net_qapital_breakdown(transactions)['investments']
    vanguard_idx = transactions.original_description.str.contains('VANGUARD')
    vanguard_savings = transactions[vanguard_idx].amount.sum()
    business_idx = (transactions.original_description.str.contains('Online scheduled transfer from CHK 4604')) & (transactions.account_name == 'Business Fundamentals Chk')
    business_investment = transactions[business_idx].amount.sum()
    return np.round(qapital_investments+ vanguard_savings + business_investment)

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

def get_rent(transactions):
    idx = transactions.original_description.str.contains('(?i)willow')
    rent = transactions[idx].amount.sum()
    return np.round(rent, 2)

def get_phone_bill(transactions):
    idx = transactions.original_description.str.contains('(?i)project fi')
    phone_bill = transactions[idx].amount.sum()
    return np.round(phone_bill, 2)

def get_groceries(transactions):
    idx = transactions.original_description.str.contains('(?i)instacart|star market')
    groceries = transactions[idx].amount.sum()
    return np.round(groceries, 2)

def get_fixed_costs(transactions):
    rent = get_rent(transactions)
    utilities = get_utilities(transactions)
    phone_bill = get_phone_bill(transactions)
    groceries = get_groceries(transactions)
    breakdown = get_net_qapital_breakdown(transactions)

    return rent + utilities + phone_bill + groceries + breakdown['fixed_costs']

def get_savings_goals(transactions):
    breakdown = get_net_qapital_breakdown(transactions)
    return breakdown['savings_goals']
