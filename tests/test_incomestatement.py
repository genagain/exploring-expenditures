import pytest
import pandas as pd
import incomestatement
from collections import OrderedDict

@pytest.fixture
def test_transactions():
  # TODO verify in B of A and Mint transactions for every single assertion
  july = pd.read_pickle('tests/test_july_2018.pickle')
  august = pd.read_pickle('tests/test_august_2018.pickle')
  september =  pd.read_pickle('tests/test_september_2018.pickle')
  return (july, august, september)

def test_get_income(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_income(july) == 6149.52
  assert incomestatement.get_income(august) == 5516.76
  assert incomestatement.get_income(september) == 4789.53

def test_get_income_returned_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_income(month, return_selected=True)
    assert selected_records.category.unique() == ['paycheck']

def test_get_transportation_expenses(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_transportation_expenses(july) == 512.0
  assert incomestatement.get_transportation_expenses(august) == 651.0
  assert incomestatement.get_transportation_expenses(september) == 558.0

def test_get_transportation_expenses_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_transportation_expenses(month, return_selected=True)
    descriptions = selected_records.original_description.unique()
    assert all(['LYFT' in description for description in descriptions])

def test_get_utilities(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_utilities(july) == 151.36
  assert incomestatement.get_utilities(august) == 161.95
  assert incomestatement.get_utilities(september) == 67.03

def test_get_utilities_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_utilities(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['COMCAST' in description or 'EVERSOURCE' in description for description in descriptions])

def test_get_net_qapital_savings(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_net_qapital_savings(july) == 1915.0
  assert incomestatement.get_net_qapital_savings(august) == 1029.0
  assert incomestatement.get_net_qapital_savings(september) == -482.0

def test_get_net_qapital_savings_return_selected(test_transactions):
  july, august, september = test_transactions
  for month in test_transactions:
    withdrawals, deposits = incomestatement.get_net_qapital_savings(month, return_selected=True)
    assert [category in ['savings', 'deposit'] for category in withdrawals.category.unique()]
    assert [category in ['income', 'transfer'] for category in deposits.category.unique()]
    assert all(['QAPITAL' in description for description in withdrawals.original_description.unique()])
    assert all(['QAPITAL' in description for description in deposits.original_description.unique()])

# TODO similate different investment scenarios bad, optimal, exceptional

def test_get_net_qapital_breakdown(test_transactions):
  july, august, september = test_transactions

  expected_breakdowns = [
    OrderedDict([('transactions', july), ('fixed_costs', 540), ('investments', 200), ('savings_goals', 100)]),
    OrderedDict([('transactions', august), ('fixed_costs', 540), ('investments', 200), ('savings_goals', 100)]),
    OrderedDict([('transactions', september), ('fixed_costs', -482.0), ('investments', 0), ('savings_goals', 0)]),
  ]

  for expected_breakdown in expected_breakdowns:
    month = expected_breakdown.pop('transactions')
    breakdown = incomestatement.get_net_qapital_breakdown(month)
    assert breakdown == expected_breakdown

def test_get_net_venmo(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_net_venmo(july) == -52.0
  assert incomestatement.get_net_venmo(august) == 904.0
  assert incomestatement.get_net_venmo(september) == 1033.0

def test_get_net_venmo_return_selected(test_transactions):
  july, august, september = test_transactions
  for month in test_transactions:
    deposits, withdrawals = incomestatement.get_net_venmo(month, return_selected=True)
    assert all(['VENMO DES:PAYMENT' in description for description in withdrawals.original_description.unique()])
    assert all(['VENMO DES:CASHOUT' in description for description in deposits.original_description.unique()])

def test_get_credit_card_expenses(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_credit_card_expenses(july) == 1836.74
  assert incomestatement.get_credit_card_expenses(august) == 2056.28
  assert incomestatement.get_credit_card_expenses(september) == 2210.19

def test_get_credit_card_expenses_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_credit_card_expenses(month, return_selected=True)
    accounts = selected_records.account_name.unique()
    assert ['nRewards Visa'] == accounts

def test_get_rent(test_transactions):
  _, august, september = test_transactions
  assert incomestatement.get_rent(august) == 2500.00
  assert incomestatement.get_rent(september) == 2600.00

def test_get_rent_return_selected(test_transactions):
  _, august, september = test_transactions
  for month in (august, september):
    selected_records = incomestatement.get_rent(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['willow' in description.lower() for description in descriptions])

def test_get_phone_bill(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_phone_bill(july) == 71.52
  assert incomestatement.get_phone_bill(august) == 79.11
  assert incomestatement.get_phone_bill(september) == 87.35

def test_get_phone_bill_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_phone_bill(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['project fi' in description.lower() for description in descriptions])

def test_get_groceries(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_groceries(july) == 173.98
  assert incomestatement.get_groceries(august) == 122.43
  assert incomestatement.get_groceries(september) == 39.60

def test_get_groceries_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_groceries(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['INSTACART' in description or 'STAR MARKET' in description for description in descriptions])

def test_fixed_costs(test_transactions):
  july, august, september = test_transactions

  expected_fixed_costs = [
    {'transactions': july, 'expected_cost': 936.86},
    {'transactions': august, 'expected_cost': 3403.49},
    {'transactions': september, 'expected_cost': 2311.98},
  ]

  for fixed_cost in expected_fixed_costs:
    month = fixed_cost['transactions']
    rent = incomestatement.get_rent(month)
    utilities = incomestatement.get_utilities(month)
    phone_bill = incomestatement.get_phone_bill(month)
    groceries = incomestatement.get_groceries(month)
    breakdown = incomestatement.get_net_qapital_breakdown(month)
    assert incomestatement.get_fixed_costs(month) == rent + utilities + phone_bill + groceries + breakdown['fixed_costs']
    assert incomestatement.get_fixed_costs(month) == fixed_cost['expected_cost']

def test_get_investments(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_investments(july) == 525
  assert incomestatement.get_investments(august) == 550
  assert incomestatement.get_investments(september) == 300

def test_get_investments_select_returned(test_transactions):
  for month in test_transactions:
    vanguard_savings, business_investment = incomestatement.get_investments(month, return_selected=True)
    assert all(['VANGUARD' in description for description in vanguard_savings.original_description])
    assert all(['Online scheduled transfer from CHK 4604' in description for description in business_investment.original_description])
    assert ['Business Fundamentals Chk'] == business_investment.account_name.unique()

def test_get_savings_goals(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_savings_goals(july) == 100
  assert incomestatement.get_savings_goals(august) == 100
  assert incomestatement.get_savings_goals(september) == 0

