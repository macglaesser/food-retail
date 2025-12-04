import pandas as pd
import requests

def geocode_sales_tax_data(inputData, countyCode, naicsCode, batchOutputPath, geocodedOutputPath, finalOutputPath):
    """
    Geocode sales tax permit holders data for a specific county and NAICS code.
    
    Parameters:
    - inputData: Path to the input CSV file containing sales tax permit holders data.
    - countyCode: The county code to filter the data (as string, e.g., '57.0').
    - naicsCode: The NAICS code prefix to filter the data (as string, e.g., '445').
    - batchOutputPath: Path to save the batch CSV file for geocoding.
    - geocodedOutputPath: Path to save the geocoded results CSV file.
    - finalOutputPath: Path to save the final merged CSV file.
    
    Returns:
    - final_df: The final merged dataframe with geocoded results.
    """
    
    # Load Raw Data
    print("==== LOADING RAW DATA ====")
    df = pd.read_csv(inputData, low_memory=False)

    # Standardize Cols
    print("==== PROCESSING RAW DATA ====")
    cols_to_str = ['Outlet County Code', 'Outlet NAICS Code']
    for col in cols_to_str:
        df[col] = df[col].fillna(0).astype(str)
    df.columns = df.columns.str.upper().str.replace(' ', '_')

    # Select Food Retail on NAICS in specified County
    df = df[df['OUTLET_NAICS_CODE'].str.startswith(str(naicsCode))]
    df = df[df['OUTLET_COUNTY_CODE'] == str(countyCode)]
    
    print(f"Found {len(df)} records for county {countyCode} and NAICS {naicsCode}")
    
    if len(df) == 0:
        print("Warning: No records found matching the filters!")
        return None

    # Create a Unique ID for each record
    df = df.reset_index(drop=True)
    df['ID'] = df.index.astype(str)

    # Census Geocoding requires the columns below as csv for batch processing
    print("==== CREATING BATCH DF ====")
    batch_df = pd.DataFrame({
        0: df['ID'],
        1: df['OUTLET_ADDRESS'],
        2: df['OUTLET_CITY'],
        3: df['OUTLET_STATE'],
        4: df['OUTLET_ZIP_CODE'].astype(str)
    })
    batch_df.to_csv(batchOutputPath, index=False, header=False)

    # Now that we have our configured package, we can send a POST request to geocode batch processing
    print("==== SENDING PACKAGE AS POST REQUEST TO CENSUS GEOCODER ====")
    url = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
    
    with open(batchOutputPath, 'rb') as f:
        files = {'addressFile': f}
        data = {
            'returntype': 'locations',
            'benchmark': 'Public_AR_Current'
        }
        response = requests.post(url, files=files, data=data)
    
    if response.status_code != 200:
        print(f"Error: Geocoding request failed with status code {response.status_code}")
        return None

    # Now we have the responses so lets save them and parse them
    print("==== SAVING AND PARSING RESULTS ====")
    with open(geocodedOutputPath, 'wb') as f:
        f.write(response.content)
    
    geocoded_df = pd.read_csv(geocodedOutputPath, header=None)
    geocoded_df.columns = [
        'ID', 'Input_Address', 'Match_Status', 'Match_Type', 'Matched_Address',
        'Coordinates', 'TIGER_Line_ID', 'Side'
    ]
    
    # Separate coordinates into individual columns
    geocoded_df[['Longitude', 'Latitude']] = geocoded_df['Coordinates'].str.split(',', expand=True)
    
    # Merge the data with the original dataframe on ID
    df['ID'] = df['ID'].astype(str)
    geocoded_df['ID'] = geocoded_df['ID'].astype(str)
    final_df = df.merge(geocoded_df[['ID', 'Latitude', 'Longitude', 'Match_Status', 'Match_Type']], on='ID', how='left')
    
    # Save the final Data File
    final_df.to_csv(finalOutputPath, index=False)
    print(f"Geocoding complete. Results saved to {finalOutputPath}")
    
    return final_df