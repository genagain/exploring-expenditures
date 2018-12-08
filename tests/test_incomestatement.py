from datetime import datetime
from freezegun import freeze_time
import pytest
import pandas as pd
import incomestatement
from collections import OrderedDict

import utilities

# TODO refactor with a config file of tokens for each aggregation
# TODO ensure that all assertions have two decimal places unless it's zero
# TODO only use october, november, december
# TODO think about how to account for cashing out wayfair stocks

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
  assert incomestatement.get_groceries(july) == 271.04
  assert incomestatement.get_groceries(august) == 122.43
  assert incomestatement.get_groceries(september) == 218.22

def test_get_groceries_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_groceries(month, return_selected=True)
    descriptions = selected_records.original_description
    # TODO figure out a better way of doing this
    assert all(['INSTACART' in description or 'STAR MARKET' in description or 'WEGMANS' in description for description in descriptions])

def test_get_debitize_payments(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_debitize_payments(july) == 200
  assert incomestatement.get_debitize_payments(august) == 1359.88
  assert incomestatement.get_debitize_payments(september) == 1248.08

def test_get_debitize_payments_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_debitize_payments(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['debitize' in description.lower() for description in descriptions])

def test_get_nfcu_payments(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_nfcu_payments(july) == 1395.65
  assert incomestatement.get_nfcu_payments(august) == 775.23
  assert incomestatement.get_nfcu_payments(september) == 986.01

def test_get_nfcu_payments_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_nfcu_payments(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['PAYMENT' in description for description in descriptions])

def test_get_nfcu_interest(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_nfcu_interest(july) == 0.23
  assert incomestatement.get_nfcu_interest(august) == 0.04
  assert incomestatement.get_nfcu_interest(september) == 0.0

def test_get_nfcu_interest_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_nfcu_interest(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['INTEREST CHARGE' in description for description in descriptions])

def test_get_unnecessary_fees(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_unnecessary_fees(july) == 101.5
  assert incomestatement.get_unnecessary_fees(august) == 164.88
  assert incomestatement.get_unnecessary_fees(september) == 90.03

def test_get_unnecessary_fees_return_selected(test_transactions):
  for month in test_transactions:
    selected_records = incomestatement.get_unnecessary_fees(month, return_selected=True)
    descriptions = selected_records.original_description
    assert all(['fee' in description.lower() for description in descriptions])

def test_fixed_costs(test_transactions):
  july, august, september = test_transactions

  expected_fixed_costs = [
    {'transactions': july, 'expected_cost': 1033.92},
    {'transactions': august, 'expected_cost': 3403.49},
    {'transactions': september, 'expected_cost': 2490.6},
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

def test_fixed_costs_return_selected(test_transactions):
  for month in test_transactions:
    rent = incomestatement.get_rent(month, return_selected=True)
    utilities = incomestatement.get_utilities(month, return_selected=True)
    phone_bill = incomestatement.get_phone_bill(month, return_selected=True)
    groceries = incomestatement.get_groceries(month, return_selected=True)

    fixed_costs_records = incomestatement.get_fixed_costs(month, return_selected=True)

    expected_fixed_cost_records = pd.concat([rent, utilities, phone_bill, groceries])
    assert fixed_costs_records.equals(expected_fixed_cost_records)

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

def test_get_discretionary_spending(test_transactions):
  # TODO revisit these assertions after going over all of the transactions
  july, august, september = test_transactions
  assert incomestatement.get_discretionary_spending(july) == 4743.44
  assert incomestatement.get_discretionary_spending(august) == 6034.55
  assert incomestatement.get_discretionary_spending(september) == 8526.0

def test_get_discretionary_spending_return_selected(test_transactions):
  for month in test_transactions:
    income = incomestatement.get_income(month, return_selected=True)
    fixed_costs = incomestatement.get_fixed_costs(month, return_selected=True)
    vanguard_savings, business_investment = incomestatement.get_investments(month, return_selected=True)
    qapital_withdrawals, qapital_deposits = incomestatement.get_net_qapital_savings(month, return_selected=True)
    venmo_deposits, venmo_withdrawals = incomestatement.get_net_venmo(month, return_selected=True)

    discretionary_spending = incomestatement.get_discretionary_spending(month, return_selected=True)

    expenses = [
      income,
      fixed_costs,
      vanguard_savings,
      business_investment,
      qapital_withdrawals,
      qapital_deposits,
      venmo_deposits
    ]

    for expense in expenses:
      overlap = discretionary_spending.isin(expense).all(axis=None)
      assert overlap == False


# TODO test Sunday
# TODO test another day later than monday
@freeze_time("Sept 23rd, 2018")
def test_week_to_day_transactions(monkeypatch):
    def mock_get_transactions():
      transactions = pd.read_pickle('tests/transactions.pickle')
      return transactions

    monkeypatch.setattr(utilities,'get_transactions', mock_get_transactions)

    expected_start_date = datetime(2018, 9, 16)
    expected_end_date = datetime(2018, 9, 22)

    weeks_transactions = incomestatement.week_to_day_transactions()

    actual_start_date = weeks_transactions.date.min()
    actual_end_date = weeks_transactions.date.max()

    assert expected_start_date.year == actual_start_date.year
    assert expected_start_date.month == actual_start_date.month
    assert expected_start_date.day <= actual_start_date.day

    assert expected_end_date.year == actual_end_date.year
    assert expected_end_date.month == actual_end_date.month
    assert expected_end_date.day >= actual_end_date.day

@freeze_time("Sept 26rd, 2018")
def test_week_to_day_transactions(monkeypatch):
    def mock_get_transactions():
      transactions = pd.read_pickle('tests/transactions.pickle')
      return transactions

    monkeypatch.setattr(utilities,'get_transactions', mock_get_transactions)

    expected_start_date = datetime(2018, 9, 23)
    expected_end_date = datetime(2018, 9, 25)

    weeks_transactions = incomestatement.week_to_day_transactions()

    actual_start_date = weeks_transactions.date.min()
    actual_end_date = weeks_transactions.date.max()

    assert expected_start_date.year == actual_start_date.year
    assert expected_start_date.month == actual_start_date.month
    assert expected_start_date.day <= actual_start_date.day

    assert expected_end_date.year == actual_end_date.year
    assert expected_end_date.month == actual_end_date.month
    assert expected_end_date.day >= actual_end_date.day
