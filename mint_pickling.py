import mintapi
import pickle
import os

mint = mintapi.Mint(os.environ['EMAIL'], os.environ['PASSWORD'])
transactions = mint.get_transactions()
transactions.drop_duplicates(['date','original_description','amount'], inplace=True)
transactions = transactions.drop(['labels','notes'], 1)
pickle.dump(transactions, open('transactions.pickle', 'wb'))
