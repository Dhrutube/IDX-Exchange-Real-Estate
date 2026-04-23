import pandas as pd
import numpy as np

dfListings = pd.read_csv('CRMLSListing.csv')
dfSold = pd.read_csv('CRMLSSold.csv')

listingsUniqueProperty = np.unique(dfListings['PropertyType'])
print('Unique Property Types in listings:\n', listingsUniqueProperty)

soldUniqueProperty = np.unique(dfSold['PropertyType'])
print('Unique Property Types in sold:\n', soldUniqueProperty)

print('Are they the same columns?', np.array_equal(listingsUniqueProperty, soldUniqueProperty))

# as provided in the handbook
keycols = set(['ClosePrice',
 'ListPrice',
 'OriginalListPrice',
 'LivingArea',
 'LotSizeAcres',
 'BedroomsTotal',
 'BathroomsTotalInteger',
 'DaysOnMarket',
 'YearBuilt'])

# identifying >90% missing columns in Listings
print('Listings\n')
missingColumnsListings= []
for col in dfListings.columns:
    missingAmount = dfListings[col].isna().sum() / dfListings.shape[0]
    print(f'{col}:', missingAmount)
    if missingAmount > 0.9:
        missingColumnsListings.append(col)
print()

# identifying >90% missing columns in Sold
print('Sold\n')
missingColumnsSold= []
for col in dfSold.columns:
    missingAmount = dfSold[col].isna().sum() / dfSold.shape[0]
    print(f'{col}:', missingAmount)
    if missingAmount > 0.9:
        missingColumnsSold.append(col)
print()

# I checked in the notebook that these columns are not part of the key columns
# I decided to drop the columns
dfListings.drop(columns=missingColumnsListings)
dfSold.drop(columns=missingColumnsSold)
dfListings = dfListings[dfListings['PropertyType'] == 'Residential']
dfSold = dfSold[dfSold['PropertyType'] == 'Residential']
print(f'Shape of Listings DataFrame: {dfListings.shape}')
print(f'Shape of Sold DataFrame: {dfSold.shape}')

print('Null counts for Listings:')
print(dfListings.isnull().sum().to_string())

print('Null counts for Sold:')
print(dfSold.isnull().sum().to_string())

desc_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
print('Listings Summary:')
print(dfListings[desc_cols].describe())
print('Sold Summary:')
print(dfSold[desc_cols].describe())


dfListings.to_csv('filteredListings.csv', index=False)
dfSold.to_csv('filteredSold.csv', index=False)