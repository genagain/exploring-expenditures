import pytest
import pandas as pd
import incomestatement

@pytest.fixture
def september_transactions():
  return pd.read_pickle('tests/test_september_2018.pickle')

def test_get_income(september_transactions):
  transactions = september_transactions
  assert incomestatement.get_income(transactions) == 4789.53

def test_get_transportation_expenses(september_transactions):
  transactions = september_transactions
  assert incomestatement.get_transportation_expenses(transactions) == 528

def test_get_net_savings(september_transactions):
  transactions = september_transactions
  assert incomestatement.get_net_qapital_savings(transactions) == 3678.0
