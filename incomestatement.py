import numpy as np
import pandas as pd

def get_income(transactions):
    idx = transactions.category == 'paycheck'
    income = transactions[idx].amount.sum()
    return np.round(income, 2)

def get_transportation_expenses(transactions):
    idx = transactions.description == 'Lyft'
    expenses = transactions[idx].amount.sum()
    return np.round(expenses, 2)
