import mintapi
import os

def get_transactions():
    mint = mintapi.Mint(os.environ['EMAIL'], os.environ['PASSWORD'])
    mint.initiate_account_refresh()
    transactions = mint.get_transactions()
    transactions.drop_duplicates(['date','original_description','amount'], inplace=True)
    return transactions

def get_accounts():
    mint = mintapi.Mint(os.environ['EMAIL'], os.environ['PASSWORD'])
    mint.initiate_account_refresh()
    return mint.get_accounts()
