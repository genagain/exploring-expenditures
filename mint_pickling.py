import mintapi
import pickle
import os

mint = mintapi.Mint(os.environ['EMAIL'], os.environ['PASSWORD'])
transactions = mint.get_transactions()
pickle.dump(transactions, open('transactions.pickle', 'wb'))
