import pandas as pd

# merge on ACCOUNT_NUM
# Account_INFO must create a full address line to match enriched data foodRetailLocations.csv
foodRetailLocations = pd.read_csv('../local-data/foodRetailLocations.csv')
accountINFO = pd.read_csv('../local-data/ACCOUNT_INFO.csv')
comDetail = pd.read_csv('../local-data/COM_DETAIL.CSV')

foodRetailLocations.columns = foodRetailLocations.columns.str.upper().str.replace(' ', '_')
accountINFO.columns = accountINFO.columns.str.upper().str.replace(' ', '_') 
comDetail.columns = comDetail.columns.str.upper().str.replace(' ', '_')

extraDetail = pd.merge(comDetail, accountINFO, on='ACCOUNT_NUM', how='left')


# Standardize address fields to uppercase for better matching
detail_upper_cols = ['STORE_STREET_ADDRESS', 'CITY', 'STATE']
for col in detail_upper_cols:
    if col in extraDetail.columns:
        extraDetail[col] = extraDetail[col].astype(str).str.upper()

food_upper_cols = ['OUTLET_ADDRESS', 'OUTLET_CITY', 'OUTLET_STATE']
for col in food_upper_cols:
    if col in foodRetailLocations.columns:
        foodRetailLocations[col] = foodRetailLocations[col].astype(str).str.upper()

# Create composite keys for matching
extraDetail['SNAP_COMPOSITE_KEY'] = (
    extraDetail['STREET_NUM'].astype(str) + " " +
    extraDetail['FULL_STREET_NAME'].astype(str) + " " +
    extraDetail['PROPERTY_CITY'].astype(str)
)

foodRetailLocations['FOOD_COMPOSITE_KEY'] = (
    foodRetailLocations['STORE_STREET_ADDRESS'].astype(str) + " " +
    foodRetailLocations['CITY'].astype(str)
)

finalMerged = pd.merge(foodRetailLocations, extraDetail, left_on='FOOD_COMPOSITE_KEY', right_on='SNAP_COMPOSITE_KEY', how='left', suffixes=('_SNAP', '_FOOD'))

# Save merged data
finalMerged.to_csv("../local-data/property_size_merged.csv", index=False)
print(f"\nMerged data saved to ../local-data/property_size_merged.csv")