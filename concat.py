import pandas as pd


dfListings = pd.DataFrame()
listings = []
for i in range(4, 5 + 1):
    for m in range(1, 12 + 1):
        temp = pd.read_csv(f'raw/CRMLSListing202{i}{m:02d}.csv')
        print(f'Shape of CRMLSListing202{i}{m:02d}: {temp.shape}')
        listings.append(temp)

# Since only 601 and 602,
for i in range(1, 2 + 1):
    temp = pd.read_csv(f'raw/CRMLSListing20260{i}.csv')
    print(f'Shape of CRMLSListing20260{i}: {temp.shape}')
    listings.append(temp)

dfListings = pd.concat(listings)
print(f'Concatenated Listings Dataframe size: dfListings.shape')
# dfListings = dfListings[dfListings['PropertyType'] == 'Residential']
# print(f'After filtering for residential: {dfListings.shape}')

dfListings.to_csv('CRMLSListing.csv', index=False)


dfSold = pd.DataFrame()
sold = []
for i in range(4, 5 + 1):
    for m in range(1, 12 + 1):
        temp = pd.read_csv(f'raw/CRMLSSold202{i}{m:02d}.csv')
        print(f'Shape of CRMLSSold202{i}{m:02d}: {temp.shape}')
        sold.append(temp)

# Since only 601 and 602,
for i in range(1, 2 + 1):
    temp = pd.read_csv(f'raw/CRMLSListing20260{i}.csv')
    print(f'Shape of CRMLSSold20260{i}: {temp.shape}')
    sold.append(temp)

dfSold = pd.concat(sold)
print(f'Concatenated Sold Dataframe size: dfSold.shape')
# dfSold = dfSold[dfSold['PropertyType'] == 'Residential']
# print(f'After filtering for residential: {dfSold.shape}')

dfSold.to_csv('CRMLSSold.csv', index=False)