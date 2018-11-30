from collections import OrderedDict

import numpy as np
import pandas as pd
from config import OPTIMAL_BREAKDOWN

def sum_amounts(transactions, return_selected=False):
    if return_selected:
      return transactions
    else:
      total_amount = transactions.amount.sum()
      return np.round(total_amount, 2)

def get_income(transactions, return_selected=False):
    idx = transactions.category == 'paycheck'
    return sum_amounts(transactions[idx], return_selected)

def get_transportation_expenses(transactions, return_selected=False):
    idx = transactions.original_description.str.contains('(?i)lyft')
    return sum_amounts(transactions[idx], return_selected)

def get_utilities(transactions, return_selected=False):
    idx = (transactions.account_name == 'Bills') & (transactions.original_description.str.contains('COMCAST|EVERSOURCE'))
    return sum_amounts(transactions[idx], return_selected)

def get_net_qapital_savings(transactions, return_selected=False):
    withdrawal_idx = transactions.original_description.str.contains('QAPITAL') & transactions.category.isin(['savings', 'deposit'])
    withdrawals = sum_amounts(transactions[withdrawal_idx], return_selected)
    deposits_idx = transactions.original_description.str.contains('QAPITAL') & transactions.category.isin(['income', 'transfer'])
    deposits = sum_amounts(transactions[deposits_idx], return_selected)
    return (withdrawals, deposits) if return_selected else np.round(withdrawals - deposits)

def get_net_qapital_breakdown(transactions, return_selected=False):
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

def get_investments(transactions, return_selected=False):
    qapital_investments= get_net_qapital_breakdown(transactions)['investments']
    vanguard_idx = transactions.original_description.str.contains('VANGUARD')
    vanguard_savings = sum_amounts(transactions[vanguard_idx], return_selected)
    business_idx = (transactions.original_description.str.contains('Online scheduled transfer from CHK 4604')) & (transactions.account_name == 'Business Fundamentals Chk')
    business_investment = sum_amounts(transactions[business_idx], return_selected)
    return (vanguard_savings, business_investment) if return_selected else np.round(qapital_investments+ vanguard_savings + business_investment)

def get_credit_card_expenses(transactions, return_selected=False):
    idx = transactions.account_name == 'nRewards Visa'
    return sum_amounts(transactions[idx], return_selected)

def get_net_venmo(transactions, return_selected=False):
    withdrawal_idx = transactions.original_description.str.contains('VENMO DES:PAYMENT')
    withdrawals = sum_amounts(transactions[withdrawal_idx], return_selected)
    deposits_idx = transactions.original_description.str.contains('VENMO DES:CASHOUT')
    deposits = sum_amounts(transactions[deposits_idx], return_selected)
    return (deposits, withdrawals) if return_selected else np.round(deposits - withdrawals)

def get_rent(transactions, return_selected=False):
    idx = transactions.original_description.str.contains('(?i)willow')
    return sum_amounts(transactions[idx], return_selected)

def get_phone_bill(transactions, return_selected=False):
    idx = transactions.original_description.str.contains('(?i)project fi')
    return sum_amounts(transactions[idx], return_selected)

def get_groceries(transactions, return_selected=False):
    idx = transactions.original_description.str.contains('(?i)instacart|star market|wegmans')
    return sum_amounts(transactions[idx], return_selected)

def get_debitize_payments(transactions, return_selected=False):
    idx = transactions.original_description.str.contains('(?i)debitize')
    return sum_amounts(transactions[idx], return_selected)

def get_nfcu_payments(transactions, return_selected=False):
   # TODO rethink how this is computed while selecting all of the relevant records
   idx = transactions.original_description.str.contains('(?i)nfcu ach des:payment|payment received')
   return sum_amounts(transactions[idx], return_selected)

def get_nfcu_interest(transactions, return_selected=False):
   idx = transactions.original_description.str.contains('(?i)interest charge-cash')
   return sum_amounts(transactions[idx], return_selected)

def get_unnecessary_fees(transactions, return_selected=False):
   # The space in the regex might be necessary to exclude the token 'coffee'
   idx = transactions.original_description.str.contains('(?i) fee')
   return sum_amounts(transactions[idx], return_selected)

def get_fixed_costs(transactions, return_selected=False):
    rent = get_rent(transactions, return_selected)
    utilities = get_utilities(transactions, return_selected)
    phone_bill = get_phone_bill(transactions, return_selected)
    groceries = get_groceries(transactions, return_selected)
    breakdown = get_net_qapital_breakdown(transactions, return_selected)

    if return_selected:
      return pd.concat([rent, utilities, phone_bill, groceries])
    else:
      return rent + utilities + phone_bill + groceries + breakdown['fixed_costs']

def get_savings_goals(transactions, return_selected=False):
    # TODO add HSBC stuff
    breakdown = get_net_qapital_breakdown(transactions)
    return breakdown['savings_goals']

def get_discretionary_spending(transactions, return_selected=False):
    income = get_income(transactions, return_selected=True)
    rent = get_rent(transactions, return_selected=True)
    utilities = get_utilities(transactions, return_selected=True)
    phone_bill = get_phone_bill(transactions, return_selected=True)
    groceries = get_groceries(transactions, return_selected=True)
    transportation = get_transportation_expenses(transactions, return_selected=True)
    debitize_payments = get_debitize_payments(transactions, return_selected=True)
    nfcu_payments = get_nfcu_payments(transactions, return_selected=True)
    unnecessary_fees = get_unnecessary_fees(transactions, return_selected=True)

    qapital_withdrawals, qapital_deposits = get_net_qapital_savings(transactions, return_selected=True)
    venmo_deposits, _ = get_net_venmo(transactions, return_selected=True)
    vanguard_savings, business_investment = get_investments(transactions, return_selected=True)

    necessary_spending = pd.concat([
      income,
      rent,
      utilities,
      phone_bill,
      groceries,
      transportation,
      qapital_withdrawals,
      qapital_deposits,
      venmo_deposits,
      vanguard_savings,
      business_investment,
      debitize_payments,
      nfcu_payments,
      unnecessary_fees
    ])

    discretionary_transactions = transactions[~transactions.isin(necessary_spending)].dropna()

    # Drop transfers here to no interfere with my investments logic
    idx = ~(discretionary_transactions.original_description.str.contains('(?i)transfer|wire type:intl in date|irs des:usataxpymt|return of posted check'))
    discretionary_transactions = discretionary_transactions[idx]
    return sum_amounts(discretionary_transactions, return_selected)
