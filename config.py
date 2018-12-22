from collections import OrderedDict

OPTIMAL_BREAKDOWN = OrderedDict([
  ('fixed_costs', 335),
  ('investments', 300),
  ('savings_goals', 0)
])

EXPECTED_SUMMARY = {
  'week to day': {
    'Fixed Costs': {
      'amount':210,
      'percentage':17.3
    },
    'Long Term Investments': {
      'amount':250,
      'percentage':20.5
    },
    'Savings Goals': {
      'amount':250,
      'percentage':20.5
    },
    'Spending Money': {
      'amount':500,
      'percentage':41.7
    }
  },
  'month to day': {
    'Fixed Costs': {
      'amount':2700,
      'percentage':40
    },
    'Long Term Investments': {
      'amount':1000,
      'percentage':15
    },
    'Savings Goals': {
      'amount':1000,
      'percentage':15
    },
    'Spending Money': {
      'amount':2000,
      'percentage':30
    }
  },
  'last month': {
    'Fixed Costs': {
      'amount':2700,
      'percentage':40
    },
    'Long Term Investments': {
      'amount':1000,
      'percentage':15
    },
    'Savings Goals': {
      'amount':1000,
      'percentage':15
    },
    'Spending Money': {
      'amount':2000,
      'percentage':30
    }
  }
}
