import pandas as pd
import re

# ============================================================
# 1. LOAD DATA
# ============================================================
print("Loading data files...")
foodRetailLocations = pd.read_csv('../local-data/snap_sales_tax_cusine_merged_data.csv')
accountINFO = pd.read_csv('../local-data/ACCOUNT_INFO.csv', low_memory=False)
comDetail = pd.read_csv('../local-data/COM_DETAIL.CSV')
accountApprl = pd.read_csv('../local-data/ACCOUNT_APPRL_YEAR.CSV')

print(f"Loaded {len(foodRetailLocations)} retail locations")
print(f"Loaded {len(accountINFO)} property accounts")
print(f"Loaded {len(comDetail)} commercial detail records")
print(f"Loaded {len(accountApprl)} appraisal records\n")

# ============================================================
# 2. STANDARDIZE COLUMN NAMES
# ============================================================
foodRetailLocations.columns = foodRetailLocations.columns.str.upper().str.replace(' ', '_')
accountINFO.columns = accountINFO.columns.str.upper().str.replace(' ', '_') 
comDetail.columns = comDetail.columns.str.upper().str.replace(' ', '_')
accountApprl.columns = accountApprl.columns.str.upper().str.replace(' ', '_')

# ============================================================
# 3. MERGE PROPERTY DATA
# ============================================================
print("Merging property datasets...")
accountINFO = pd.merge(accountINFO, accountApprl[['ACCOUNT_NUM', 'TOT_VAL']], 
                       on='ACCOUNT_NUM', how='left')
extraDetail = pd.merge(comDetail, accountINFO, on='ACCOUNT_NUM', how='left')
print(f"Created extraDetail with {len(extraDetail)} records\n")

# ============================================================
# 4. ADDRESS STANDARDIZATION FUNCTION
# ============================================================
def standardize_address(address):
    """Standardize address format for better matching"""
    if pd.isna(address):
        return ""
    
    address = str(address).upper().strip()
    
    # Common abbreviations
    replacements = {
        r'\bSTREET\b': 'ST',
        r'\bAVENUE\b': 'AVE',
        r'\bBOULEVARD\b': 'BLVD',
        r'\bDRIVE\b': 'DR',
        r'\bROAD\b': 'RD',
        r'\bLANE\b': 'LN',
        r'\bCOURT\b': 'CT',
        r'\bCIRCLE\b': 'CIR',
        r'\bPARKWAY\b': 'PKWY',
        r'\bNORTH\b': 'N',
        r'\bSOUTH\b': 'S',
        r'\bEAST\b': 'E',
        r'\bWEST\b': 'W',
    }
    
    for pattern, replacement in replacements.items():
        address = re.sub(pattern, replacement, address)
    
    # Remove extra spaces and punctuation
    address = re.sub(r'[.,#]', '', address)
    address = re.sub(r'\s+', ' ', address)
    
    return address.strip()

# ============================================================
# 5. CREATE COMPOSITE KEYS WITH STANDARDIZATION
# ============================================================
print("Creating composite address keys...")

# For property data
extraDetail['STREET_NUM_CLEAN'] = extraDetail['STREET_NUM'].astype(str).str.strip()
extraDetail['FULL_STREET_NAME_CLEAN'] = extraDetail['FULL_STREET_NAME'].apply(standardize_address)
extraDetail['PROPERTY_CITY_CLEAN'] = extraDetail['PROPERTY_CITY'].apply(standardize_address)

extraDetail['SNAP_COMPOSITE_KEY'] = (
    extraDetail['STREET_NUM_CLEAN'] + " " +
    extraDetail['FULL_STREET_NAME_CLEAN'] + " " +
    extraDetail['PROPERTY_CITY_CLEAN']
)

# For retail locations - check which columns exist
if 'STORE_STREET_ADDRESS' in foodRetailLocations.columns:
    address_col = 'STORE_STREET_ADDRESS'
elif 'OUTLET_ADDRESS' in foodRetailLocations.columns:
    address_col = 'OUTLET_ADDRESS'
else:
    # Find the most likely address column
    address_cols = [col for col in foodRetailLocations.columns if 'ADDRESS' in col]
    if address_cols:
        address_col = address_cols[0]
        print(f"Warning: Using {address_col} as address column")
    else:
        raise ValueError("Cannot find address column in retail locations data")

if 'CITY' in foodRetailLocations.columns:
    city_col = 'CITY'
elif 'OUTLET_CITY' in foodRetailLocations.columns:
    city_col = 'OUTLET_CITY'
else:
    city_cols = [col for col in foodRetailLocations.columns if 'CITY' in col]
    if city_cols:
        city_col = city_cols[0]
        print(f"Warning: Using {city_col} as city column")
    else:
        raise ValueError("Cannot find city column in retail locations data")

foodRetailLocations['ADDRESS_CLEAN'] = foodRetailLocations[address_col].apply(standardize_address)
foodRetailLocations['CITY_CLEAN'] = foodRetailLocations[city_col].apply(standardize_address)

foodRetailLocations['FOOD_COMPOSITE_KEY'] = (
    foodRetailLocations['ADDRESS_CLEAN'] + " " +
    foodRetailLocations['CITY_CLEAN']
)

# ============================================================
# 6. QUALITY CHECK BEFORE MERGE
# ============================================================
print("\n" + "="*60)
print("PRE-MERGE QUALITY CHECKS")
print("="*60)

# Check for blank/null addresses
print(f"\nRetail locations with missing addresses: {foodRetailLocations[address_col].isna().sum()}")
print(f"Property records with missing addresses: {extraDetail['FULL_STREET_NAME'].isna().sum()}")

# Sample composite keys
print("\nSample retail composite keys:")
print(foodRetailLocations['FOOD_COMPOSITE_KEY'].head(5).tolist())
print("\nSample property composite keys:")
print(extraDetail['SNAP_COMPOSITE_KEY'].head(5).tolist())

# Check for potential duplicates
retail_dupes = foodRetailLocations['FOOD_COMPOSITE_KEY'].duplicated().sum()
property_dupes = extraDetail['SNAP_COMPOSITE_KEY'].duplicated().sum()
print(f"\nDuplicate retail addresses: {retail_dupes}")
print(f"Duplicate property addresses: {property_dupes}")

# ============================================================
# 7. PERFORM MERGE
# ============================================================
print("\n" + "="*60)
print("PERFORMING MERGE")
print("="*60)

# First, deduplicate property data by keeping highest value per address
print("Deduplicating property records by address...")
extraDetail_deduped = extraDetail.sort_values('TOT_VAL', ascending=False).groupby('SNAP_COMPOSITE_KEY').first().reset_index()
print(f"Reduced property records from {len(extraDetail)} to {len(extraDetail_deduped)} unique addresses\n")

finalMerged = pd.merge(
    foodRetailLocations, 
    extraDetail_deduped, 
    left_on='FOOD_COMPOSITE_KEY', 
    right_on='SNAP_COMPOSITE_KEY', 
    how='left', 
    suffixes=('_RETAIL', '_PROPERTY')
)

# ============================================================
# 8. POST-MERGE QUALITY CHECKS
# ============================================================
print("\n" + "="*60)
print("POST-MERGE QUALITY CHECKS")
print("="*60)

total_retail = len(foodRetailLocations)
matched = finalMerged['SNAP_COMPOSITE_KEY'].notna().sum()
match_rate = (matched / total_retail) * 100

print(f"\nTotal retail locations: {total_retail}")
print(f"Successfully matched: {matched} ({match_rate:.1f}%)")
print(f"Unmatched: {total_retail - matched} ({100-match_rate:.1f}%)")

# Show sample of unmatched addresses
unmatched = finalMerged[finalMerged['SNAP_COMPOSITE_KEY'].isna()]
if len(unmatched) > 0:
    print("\nSample of unmatched retail addresses:")
    print(unmatched[[address_col, city_col, 'FOOD_COMPOSITE_KEY']].head(10))

# Check for property values
if 'TOT_VAL' in finalMerged.columns:
    has_value = finalMerged['TOT_VAL'].notna().sum()
    print(f"\nRetail locations with property values: {has_value} ({(has_value/total_retail)*100:.1f}%)")

# ============================================================
# 9. CLEAN UP COLUMNS
# ============================================================
print("\n" + "="*60)
print("CLEANING UP COLUMNS")
print("="*60)

# Columns to drop
drop_cols = [
    'SNAP_COMPOSITE_KEY', 'FOOD_COMPOSITE_KEY', 
    'ADDRESS_CLEAN', 'CITY_CLEAN',
    'STREET_NUM_CLEAN', 'FULL_STREET_NAME_CLEAN', 'PROPERTY_CITY_CLEAN',
    'TAX_OBJ_ID', 'BLDG_CLASS_DESC', 'YEAR_BUILT', 'REMODEL_YR', 
    'FOUNDATION_TYP_DESC', 'FOUNDATION_AREA', 'BASEMENT_DESC', 'BASEMENT_AREA', 
    'NUM_STORIES', 'CONSTR_TYP_DESC', 'HEATING_TYP_DESC', 'AC_TYP_DESC', 
    'NUM_UNITS', 'NET_LEASE_AREA', 'PROPERTY_NAME', 'PROPERTY_QUAL_DESC', 
    'PROPERTY_COND_DESC', 'PHYS_DEPR_PCT', 'FUNCT_DEPR_PCT', 'EXTRNL_DEPR_PCT', 
    'TOT_DEPR_PCT', 'APPR_METHOD_DESC', 'COMPARABILITY_CD', 'PCT_COMPLETE', 
    'DIVISION_CD', 'BIZ_NAME', 'OWNER_NAME1', 'OWNER_NAME2', 'EXCLUDE_OWNER', 
    'OWNER_ADDRESS_LINE1', 'OWNER_ADDRESS_LINE2', 'OWNER_ADDRESS_LINE3', 
    'OWNER_ADDRESS_LINE4', 'OWNER_CITY', 'OWNER_STATE', 'OWNER_ZIPCODE', 
    'OWNER_COUNTRY', 'BLDG_ID', 'UNIT_ID', 'MAPSCO', 'NBHD_CD', 
    'LEGAL1', 'LEGAL2', 'LEGAL3', 'LEGAL4', 'LEGAL5', 'DEED_TXFR_DATE', 
    'GIS_PARCEL_ID', 'PHONE_NUM', 'LMA', 'IMA'
]

# Only drop columns that exist
existing_drop_cols = [col for col in drop_cols if col in finalMerged.columns]
cleanedMerged = finalMerged.drop(columns=existing_drop_cols)

print(f"Dropped {len(existing_drop_cols)} columns")
print(f"Final dataset has {len(cleanedMerged.columns)} columns")

# ============================================================
# 10. SAVE RESULTS
# ============================================================
output_path = "../local-data/snap_sales_cusine_property_data_merged.csv"
cleanedMerged.to_csv(output_path, index=False)

print("\n" + "="*60)
print("MERGE COMPLETE")
print("="*60)
print(f"Saved to: {output_path}")
print(f"Final dataset: {len(cleanedMerged)} rows × {len(cleanedMerged.columns)} columns")

# Save unmatched addresses for review
if len(unmatched) > 0:
    unmatched_path = "../local-data/unmatched_retail_addresses.csv"
    unmatched_export = unmatched[[address_col, city_col, 'FOOD_COMPOSITE_KEY']].copy()
    unmatched_export.to_csv(unmatched_path, index=False)
    print(f"\nUnmatched addresses saved to: {unmatched_path}")
    print("Review these addresses to improve matching quality")