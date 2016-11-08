import pandas as pd
import csv
import ipdb


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

idx = descriptions.str.contains("Digit")
expenditures.ix[idx, "Clean Description"] = "DIGIT"

#TODO notice that the day of the week for the lyft transactions isn't usually the same as the day of the week of the index value
#expenditures['Clean Description'] = expenditures['Clean Description'].str.replace('\W\*RIDE\W\D{3}','')
idx = descriptions.str.contains("LYFT")
expenditures.ix[idx, "Clean Description"] = "LYFT"

# TODO write a nice method for all of these
idx = descriptions.str.contains("DOORDASH")
expenditures.ix[idx, "Clean Description"] = "DOORDASH"

idx = descriptions.str.contains("Audible")
expenditures.ix[idx, "Clean Description"] = "Audible"

idx = descriptions.str.contains("SEAMLESS")
expenditures.ix[idx, "Clean Description"] = "SEAMLESS"

idx = descriptions.str.contains("SUBWAY")
expenditures.ix[idx, "Clean Description"] = "SUBWAY"

idx = descriptions.str.contains("amazon",case=False)
expenditures.ix[idx, "Clean Description"] = "AMAZON"

#TODO account for J.P Licks as well
idx = descriptions.str.contains("LICKS")
expenditures.ix[idx, "Clean Description"] = "JP LICKS"

idx = descriptions.str.contains("CLOVER FOOD LAB")
expenditures.ix[idx, "Clean Description"] = "CLOVER FOOD LAB"

idx = descriptions.str.contains("GRUBHUB")
expenditures.ix[idx, "Clean Description"] = "GRUBHUB"

idx = descriptions.str.contains("STARBUCKS")
expenditures.ix[idx, "Clean Description"] = "STARBUCKS"

idx = descriptions.str.contains("WOLLASTON'S")
expenditures.ix[idx, "Clean Description"] = "WOLLASTON'S"

idx = descriptions.str.contains("Spotify")
expenditures.ix[idx, "Clean Description"] = "Spotify"

idx = descriptions.str.contains("INSTACART")
expenditures.ix[idx, "Clean Description"] = "INSTACART"
transaction_frequency = {}
for row_index, row in expenditures.iterrows(): 
  clean_description = str(row['Clean Description'])
  if clean_description not in transaction_frequency.keys():
    transaction_frequency[clean_description] = 1
  else:
    transaction_frequency[clean_description] += 1
#for merchant in transaction_frequency.keys():

ipdb.set_trace()
