# Exploring Expenditures

This repository contains the code I'm writing to explore my debit card transactions. I downloaded a CSV file containing all of my debit card transactions. This file is not included in this repository because of privacy concerns. 

The `cleaning.py` file cleans the data and writes the cleaned data to a new file called `clean_transactions.csv`. 

The `monthly_spending.py` file then calculates my monthly expenditures and plots them on a bar chart, using the `clean_transactions.csv` file.

The `income-statement.py` file calculates my income and breaks down my expenses into the following categories:
  * Transportation - DONE
  * Subscriptions
  * Groceries
  * Eating out
  * Utilities -  DONE
  * Credit card - DONE
  * Net Savings - DONE
  * Net Qapital Savings - DONE
  * Net Venmo - DONE
  * Miscellaneous

The `balance-sheet.py` calculates my assets and liabilities.

Please note that this is a work in progress, because there are more insights I intend on extracting from my debit card transactions. 
