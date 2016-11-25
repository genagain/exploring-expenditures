import pandas as pd
import csv
import ipdb

def replace_description(token, replacement, expenditures):
  idx = descriptions.str.contains(token,case=False)
  expenditures.ix[idx, "Clean Description"] = replacement
  return expenditures

expenditures = pd.DataFrame.from_csv('stmt.csv')
# remove weird running total nan values
idx = pd.notnull(expenditures['Running'])
expenditures = expenditures[idx]

expenditures.index = expenditures.index.str.split(',').str[0]
descriptions = expenditures['Description']
expenditures['Clean Description'] = descriptions.str.replace('CHECKCARD\W\d{4}','')
expenditures['Clean Description'] = expenditures['Clean Description'].str.extract('(\D+)')
expenditures["Clean Description"]=expenditures["Clean Description"].str.lstrip()
expenditures["Clean Description"]=expenditures["Clean Description"].str.rstrip()

token_replacements = {
    "Digit" : "DIGIT",
    "LYFT" : "LYFT",
    "DOORDASH" : "DOORDASH",
    "Audible" : "AUDIBLE",
    "SEAMLESS" : "SEAMLESS",
    "SUBWAY" : "SUBWAY",
    "amazon" : "AMAZON",
    "LICKS" : "JP LICKS",
    "CLOVER FOOD LAB" : "CLOVER FOOD LAB",
    "GRUBHUB" : "GRUBHUB",
    "STARBUCKS" : "STARBUCKS",
    "WOLLASTON'S" : "WOLLASTON'S",
    "Spotify" : "SPOTIFY",
    "INSTACART" : "INSTACART"
    }

for token, replacement in token_replacements.iteritems():
  expenditures = replace_description(token, replacement, expenditures)

expenditures.to_csv('clean_transactions.csv', columns = ['Clean Description', 'Amount', 'Running'])
