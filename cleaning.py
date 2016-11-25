import pandas as pd
import csv
import ipdb

def replace_description(token, replacement, expenditures):
  idx = descriptions.str.contains(token)
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

expenditures = replace_description("Digit", "DIGIT", expenditures)

#TODO notice that the day of the week for the lyft transactions isn't usually the same as the day of the week of the index value
expenditures = replace_description("LYFT", "LYFT", expenditures)

expenditures = replace_description("DOORDASH", "DOORDASH", expenditures)

expenditures = replace_description("Audible", "AUDIBLE", expenditures)

expenditures = replace_description("SEAMLESS", "SEAMLESS", expenditures)

expenditures = replace_description("SUBWAY", "SUBWAY", expenditures)

idx = descriptions.str.contains("amazon",case=False)
expenditures.ix[idx, "Clean Description"] = "AMAZON"

#TODO account for J.P Licks as well
expenditures = replace_description("LICKS", "JP LICKS", expenditures)

expenditures = replace_description("CLOVER FOOD LAB", "CLOVER FOOD LAB", expenditures)

expenditures = replace_description("GRUBHUB", "GRUBHUB", expenditures)

expenditures = replace_description("STARBUCKS", "STARBUCKS", expenditures)

expenditures = replace_description("WOLLASTON'S", "WOLLASTON'S", expenditures)

expenditures = replace_description("Spotify", "SPOTIFY", expenditures)

expenditures = replace_description("INSTACART", "INSTACART", expenditures)


ipdb.set_trace()
transaction_frequency = {}
for row_index, row in expenditures.iterrows(): 
  clean_description = str(row['Clean Description'])
  if clean_description not in transaction_frequency.keys():
    transaction_frequency[clean_description] = 1
  else:
    transaction_frequency[clean_description] += 1
#for merchant in transaction_frequency.keys():

