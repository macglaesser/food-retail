import pandas as pd 
import uuid

def gen_id(): 
    return uuid.uuid4().int >> 64

def merge_snap_sales_tax(snapPath, taxPath, county, state, latMin, latMax, lonMin, lonMax, outputPath):
    """
    Merge SNAP retailer data with geocoded sales tax data for a specific county.
    
    Parameters:
    - snapPath: Path to the SNAP retailer CSV file
    - taxPath: Path to the geocoded sales tax CSV file
    - county: County name (e.g., 'DALLAS')
    - state: State abbreviation (e.g., 'TX')
    - latMin: Minimum latitude for geographic bounding box
    - latMax: Maximum latitude for geographic bounding box
    - lonMin: Minimum longitude for geographic bounding box
    - lonMax: Maximum longitude for geographic bounding box
    - outputPath: Path to save the merged output CSV file
    
    Returns:
    - merged_data: DataFrame containing the merged data
    """
    
    # Read the datasets
    print(f"==== LOADING DATA FOR {county} COUNTY, {state} ====")
    snap = pd.read_csv(snapPath, encoding='latin-1')
    tax = pd.read_csv(taxPath)

    # Filter SNAP data for specified County and State
    snap = snap[(snap['County'] == county.upper()) & (snap['State'] == state.upper())]

    # Standardize column names - convert to uppercase and replace spaces with underscores
    snap.columns = snap.columns.str.upper().str.replace(' ', '_')
    tax.columns = tax.columns.str.upper().str.replace(' ', '_')

    # Standardize address fields to uppercase for better matching
    snap_upper_cols = ['STORE_STREET_ADDRESS', 'CITY', 'STATE']
    for col in snap_upper_cols:
        if col in snap.columns:
            snap[col] = snap[col].astype(str).str.upper()

    tax_upper_cols = ['OUTLET_ADDRESS', 'OUTLET_CITY', 'OUTLET_STATE']
    for col in tax_upper_cols:
        if col in tax.columns:
            tax[col] = tax[col].astype(str).str.upper()

    # Create composite keys for matching
    snap['SNAP_COMPOSITE_KEY'] = (
        snap['STORE_STREET_ADDRESS'].astype(str) + " " + 
        snap['CITY'].astype(str) + " " + 
        snap['STATE'].astype(str)
    )

    tax['TAX_COMPOSITE_KEY'] = (
        tax['OUTLET_ADDRESS'].astype(str) + " " +  
        tax['OUTLET_CITY'].astype(str) + " " + 
        tax['OUTLET_STATE'].astype(str)
    )

    # Enhanced NAICS to store type mapping
    naics_to_store_type = {
        445110: 'Supermarket',
        445120: 'Convenience Store',
        445210: 'Meat Market',
        445220: 'Seafood Market',
        445230: 'Produce Market',
        445291: 'Bakery',
        445292: 'Confectionery',
        445299: 'Specialty Food',
        445310: 'Liquor Store',
        445000: 'Food Store',
        445100: 'Grocery Store'
    }

    # Convert NAICS codes to numeric and map to store types
    tax['OUTLET_NAICS_CODE_NUMERIC'] = pd.to_numeric(tax['OUTLET_NAICS_CODE'], errors='coerce')
    tax['STORE_TYPE'] = tax['OUTLET_NAICS_CODE_NUMERIC'].map(naics_to_store_type)

    # Fill remaining unmapped with 'Other'
    tax['STORE_TYPE'] = tax['STORE_TYPE'].fillna('Other')

    # Find unmatched tax records
    tax_unmatched = tax[~tax['TAX_COMPOSITE_KEY'].isin(snap['SNAP_COMPOSITE_KEY'])].copy()

    print("\nDiagnostic information:")
    print(f"Original SNAP records ({county} County): {len(snap)}")
    print(f"Original tax records ({county} County, NAICS 445*): {len(tax)}")
    print(f"Unmatched tax records: {len(tax_unmatched)}")

    # Clean coordinate data
    print(f"\nCoordinate checks:")
    print(f"Records with missing Latitude: {tax_unmatched['LATITUDE'].isnull().sum()}")
    print(f"Records with missing Longitude: {tax_unmatched['LONGITUDE'].isnull().sum()}")

    # Remove records with missing or invalid coordinates
    tax_unmatched = tax_unmatched.dropna(subset=['LATITUDE', 'LONGITUDE'])
    tax_unmatched['LATITUDE'] = pd.to_numeric(tax_unmatched['LATITUDE'], errors='coerce')
    tax_unmatched['LONGITUDE'] = pd.to_numeric(tax_unmatched['LONGITUDE'], errors='coerce')
    tax_unmatched = tax_unmatched.dropna(subset=['LATITUDE', 'LONGITUDE'])

    # Filter by geographic bounding box
    valid_coords = (
        (tax_unmatched['LATITUDE'] >= latMin) &
        (tax_unmatched['LATITUDE'] <= latMax) &
        (tax_unmatched['LONGITUDE'] >= lonMin) &
        (tax_unmatched['LONGITUDE'] <= lonMax)
    )
    tax_unmatched = tax_unmatched[valid_coords]

    print(f"Records after coordinate validation: {len(tax_unmatched)}")

    if len(tax_unmatched) > 0:
        print(f"Latitude range: {tax_unmatched['LATITUDE'].min():.4f} to {tax_unmatched['LATITUDE'].max():.4f}")
        print(f"Longitude range: {tax_unmatched['LONGITUDE'].min():.4f} to {tax_unmatched['LONGITUDE'].max():.4f}")
        
        print(f"\nStore types being added:")
        store_type_counts = tax_unmatched['STORE_TYPE'].value_counts()
        print(store_type_counts)

        # Create new records with unique IDs
        tax_unmatched['RECORD_ID'] = [gen_id() for _ in range(len(tax_unmatched))]

        # Map tax columns to SNAP columns
        tax_mapped = pd.DataFrame({
            'RECORD_ID': tax_unmatched['RECORD_ID'],
            'STORE_NAME': tax_unmatched['OUTLET_NAME'],
            'STORE_STREET_ADDRESS': tax_unmatched['OUTLET_ADDRESS'],
            'ADDITONAL_ADDRESS': '',  # Note: keeping original typo for consistency
            'CITY': tax_unmatched['OUTLET_CITY'],
            'STATE': tax_unmatched['OUTLET_STATE'],
            'ZIP_CODE': tax_unmatched['OUTLET_ZIP_CODE'],
            'ZIP4': '',
            'COUNTY': county.upper(),
            'STORE_TYPE': tax_unmatched['STORE_TYPE'],
            'LATITUDE': tax_unmatched['LATITUDE'],
            'LONGITUDE': tax_unmatched['LONGITUDE'],
            'INCENTIVE_PROGRAM': '',
            'GRANTEE_NAME': '',
            'OBJECTID': None
        })

        # Ensure all columns exist in both datasets before concatenation
        snap_columns = set(snap.columns)
        mapped_columns = set(tax_mapped.columns)
        
        # Add missing columns to tax_mapped
        for col in snap_columns - mapped_columns:
            if col != 'SNAP_COMPOSITE_KEY':  
                tax_mapped[col] = None
        
        # Add missing columns to snap
        for col in mapped_columns - snap_columns:
            snap[col] = None
        
        # Reorder columns to match
        common_columns = list(snap_columns | mapped_columns)
        if 'SNAP_COMPOSITE_KEY' in common_columns:
            common_columns.remove('SNAP_COMPOSITE_KEY')
        
        snap_reordered = snap[common_columns]
        tax_mapped_reordered = tax_mapped[common_columns]
        
        # Combine datasets
        merged_data = pd.concat([snap_reordered, tax_mapped_reordered], ignore_index=True)
        
        # Enhance store type categorization
        merged_data.loc[
            (merged_data['STORE_TYPE'] == 'Other') & 
            (merged_data['STORE_NAME'].str.lower().str.contains('dollar', case=False, na=False)), 
            'STORE_TYPE'
        ] = 'Discount Retail'

        merged_data.loc[
            (merged_data['STORE_TYPE'] == 'Other') & 
            (merged_data['STORE_NAME'].str.lower().str.contains('walgreens|cvs', case=False, na=False)), 
            'STORE_TYPE'
        ] = 'Pharmacy'

        print(f"\nFinal dataset:")
        print(f"Original SNAP records: {len(snap)}")
        print(f"Added tax records: {len(tax_mapped)}")
        print(f"Total records: {len(merged_data)}")
        print(f"\nStore types in final dataset:")
        final_store_counts = merged_data['STORE_TYPE'].value_counts()
        print(final_store_counts)
        
        # Save merged data
        merged_data.to_csv(outputPath, index=False)
        print(f"\nMerged data saved to {outputPath}")
        
        return merged_data
        
    else:
        print("\nNo valid records to add after filtering.")
        snap.to_csv(outputPath, index=False)
        print(f"Saved original SNAP data to {outputPath}")
        return snap