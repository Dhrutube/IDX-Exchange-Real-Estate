import pandas as pd

'''
Monthly Dataset Aggregation
'''
# key columns as defined by the primer
# these columns should not be dropped even if there are a large number of missing values
keycols = set(('ListingKey', 
           'ListingContractDate', 
           'ListPrice',
           'ClosePrice',
           'PurchaseContractDate',
           'CloseDate',
           'LivingArea',
           'BedroomsTotal',
           'BathroomsTotalInteger',
           'Longitude',
           'Latitude',
           'UnparsedAddress',
           'ListAgentAOR'
           'DaysOnMarket'))


# reading in all listings datasets
dfListings = pd.DataFrame()
listings = []
for i in range(4, 6 + 1):
    try:
        for m in range(1, 12 + 1):
            temp = pd.read_csv(f'raw/CRMLSListing202{i}{m:02d}.csv')
            print(f'Shape of CRMLSListing202{i}{m:02d}: {temp.shape}')
            listings.append(temp)
    except FileNotFoundError:
        break

# concatenating all listings
dfListings = pd.concat(listings)
print(f'Concatenated Listings Dataframe size: {dfListings.shape}')

# The handbook mentions to filter to only 'Residential' property types
dfListings = dfListings[dfListings['PropertyType'] == 'Residential']
print(f'After filtering by "Residential": {dfListings.shape}')
dfListings.to_csv('filtered/filteredListings.csv')

# reading all sold datasets
dfSold = pd.DataFrame()
sold = []
for i in range(4, 5 + 1):
    try:
        for m in range(1, 12 + 1):
            temp = pd.read_csv(f'raw/CRMLSSold202{i}{m:02d}.csv')
            print(f'Shape of CRMLSSold202{i}{m:02d}: {temp.shape}')
            sold.append(temp)
    except FileNotFoundError:
        break

# concatenating all sold
dfSold = pd.concat(sold)
print(f'Concatenated Sold Dataframe size: {dfSold.shape}')

# The handbook mentions to filter to only 'Residential' property types
dfSold = dfSold[dfSold['PropertyType'] == 'Residential']
print(f'After filtering by "Residential": {dfSold.shape}')
dfSold.to_csv('filtered/filteredSold.csv')

'''
Fetching raw data from API
'''
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=["observation_date"])
mortgage.columns = ["date", "rate_30yr_fixed"]

mortgage["year_month"] = mortgage["date"].dt.to_period("M")
mortgage_monthly = (
mortgage.groupby("year_month")["rate_30yr_fixed"]
.mean().reset_index()
)

listings = pd.read_csv('filtered/filteredListings.csv')
sold = pd.read_csv('filtered/filteredSold.csv')

# Sold dataset — key off CloseDate
sold["year_month"] = pd.to_datetime(sold["CloseDate"]).dt.to_period("M")
# Listings dataset — key off ListingContractDate
listings["year_month"] = pd.to_datetime(
listings["ListingContractDate"]).dt.to_period("M")

sold_with_rates = sold.merge(mortgage_monthly, on="year_month", how="left")
listings_with_rates = listings.merge(mortgage_monthly, on="year_month", how="left")

# Check for any unmatched rows (rate should not be null)
print(sold_with_rates["rate_30yr_fixed"].isnull().sum())
print(listings_with_rates["rate_30yr_fixed"].isnull().sum())

# Preview
print(sold_with_rates[["CloseDate", "year_month", "ClosePrice",
"rate_30yr_fixed"]].head())

listings_with_rates.to_csv("filtered/listings_with_rates.csv")
sold_with_rates.to_csv("filtered/sold_with_rates.csv")

dfListings = pd.read_csv('filtered/listings_with_rates.csv')
dfSold = pd.read_csv('filtered/sold_with_rates.csv')

# since column.1 are duplicate columns in listings, dropping them
# also dropping columns with >90% missing values
toDropL = set()
for col in dfListings.columns:
    if col[-2:] == '.1':
        toDropL.add(col)
    if dfListings[col].isna().sum() > 0.90:
        if col in keycols:
            print(f'Key column in Listings with >90% missing values: {col}')
            continue
        else:
            toDropL.add(col)
dfListings.drop(columns=toDropL, inplace=True)
print(f'Number of columns after dropping >90% missing = {dfListings.shape[1]}')

# converting date columns to datetime format
dfListings['CloseDate'] = pd.to_datetime(dfListings['CloseDate'])
dfListings['PurchaseContractDate'] = pd.to_datetime(dfListings['PurchaseContractDate'])
dfListings['ListingContractDate'] = pd.to_datetime(dfListings['ListingContractDate'])


# dropping columns not part of key columns with >90% missing values
toDropS = set()
for col in dfSold.columns:
    if col[-2:] == '.1':
        toDropS.add(col)
    if dfSold[col].isna().sum() > 0.90:
        if col in keycols:
            print(f'Key column in Sold with >90% missing values: {col}')
            continue
        else:
            toDropS.add(col)
dfSold.drop(columns=toDropS, inplace=True)
print(f'Number of columns after dropping >90% missing = {dfSold.shape[1]}')

# converting date columns to datetime format
dfSold['CloseDate'] = pd.to_datetime(dfSold['CloseDate'])
# dfSold['ContractStatusChangeDate'] = pd.to_datetime(dfSold['ContractStatusChangeDate'])
dfSold['PurchaseContractDate'] = pd.to_datetime(dfSold['PurchaseContractDate'])
dfSold['ListingContractDate'] = pd.to_datetime(dfSold['ListingContractDate'])

'''
Feature Engineering and Market Metrics
'''
dfSold['Price Ratio'] = dfSold['ClosePrice'] / dfSold['ListPrice']  # measures negotiation strength
dfSold['Price Per Sq Ft'] = dfSold['ClosePrice'] / dfSold['LivingArea']  # normalizes price across sizes
dfSold['Year'] = dfSold['CloseDate'].dt.year
dfSold['Month'] = dfSold['CloseDate'].dt.month
dfSold['YrMo'] = dfSold['CloseDate'].dt.to_period('M')

# saving to new file
dfListings.to_csv('filtered/featuresListings.csv', index=False)
dfSold.to_csv('filtered/featuresSold.csv', index=False)
