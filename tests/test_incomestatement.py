import pytest
import pandas as pd
import incomestatement

@pytest.fixture
def test_transactions():
  july = pd.read_pickle('tests/test_july_2018.pickle')
  august = pd.read_pickle('tests/test_august_2018.pickle')
  september =  pd.read_pickle('tests/test_september_2018.pickle')
  return (july, august, september)

def test_get_income(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_income(july) == 6149.52
  assert incomestatement.get_income(august) == 5516.76
  assert incomestatement.get_income(september) == 4789.53

def test_get_transportation_expenses(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_transportation_expenses(july) == 512.0
  assert incomestatement.get_transportation_expenses(august) == 651.0
  assert incomestatement.get_transportation_expenses(september) == 558.0

def test_get_utilities(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_utilities(july) == 151.36
  assert incomestatement.get_utilities(august) == 161.95
  assert incomestatement.get_utilities(september) == 67.03

def test_get_net_qapital_savings(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_net_qapital_savings(july) == 1915.0
  assert incomestatement.get_net_qapital_savings(august) == 1029.0
  assert incomestatement.get_net_qapital_savings(september) == -482.0

def test_get_net_savings(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_net_savings(july) == 2240.0
  assert incomestatement.get_net_savings(august) == 1379.0
  assert incomestatement.get_net_savings(september) == -182.0

def test_get_net_venmo(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_net_venmo(july) == -52.0
  assert incomestatement.get_net_venmo(august) == 904.0
  assert incomestatement.get_net_venmo(september) == 1033.0

def test_get_credit_card_expenses(test_transactions):
  july, august, september = test_transactions
  assert incomestatement.get_credit_card_expenses(july) == 1836.74
  assert incomestatement.get_credit_card_expenses(august) == 2056.28
  assert incomestatement.get_credit_card_expenses(september) == 2210.19
