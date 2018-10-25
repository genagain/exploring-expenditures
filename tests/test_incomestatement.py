import pytest
import pandas as pd
import incomestatement

def test_get_income():
  transactions = pd.read_pickle('tests/test_september_2018.pickle')
  assert incomestatement.get_income(transactions) == 4789.53

def test_get_transportation_expenses():
  transactions = pd.read_pickle('tests/test_september_2018.pickle')
  assert incomestatement.get_transportation_expenses(transactions) == 528
