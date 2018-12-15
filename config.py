from collections import OrderedDict

OPTIMAL_BREAKDOWN = OrderedDict([
  ('fixed_costs', 540),
  ('investments', 200),
  ('savings_goals', 100)
])

EXPECTED_SUMMARY = {
  'week to day': {
    'Fixed Costs': {
      'amount':175,
      'percentage':15.2
    },
    'Long Term Investments': {
      'amount':300,
      'percentage':26.1
    },
    'Savings Goals': {
      'amount':375,
      'percentage':32.6
    },
    'Spending Money': {
      'amount':300,
      'percentage':26.1
    }
  },
  'month to day': {
    'Fixed Costs': {
      'amount':2800,
      'percentage':41.5
    },
    'Long Term Investments': {
      'amount':1200,
      'percentage':17
    },
    'Savings Goals': {
      'amount':1500,
      'percentage':23
    },
    'Spending Money': {
      'amount':1250,
      'percentage':18.5
    }
  },
  'last month': {
    'Fixed Costs': {
      'amount':2800,
      'percentage':41.5
    },
    'Long Term Investments': {
      'amount':1200,
      'percentage':17
    },
    'Savings Goals': {
      'amount':1500,
      'percentage':23
    },
    'Spending Money': {
      'amount':1250,
      'percentage':18.5
    }
  }
}
