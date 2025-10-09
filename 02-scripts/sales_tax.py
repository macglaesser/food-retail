import pandas as pd
import requests

# Load Raw Data
print("==== LOADING RAW DATA ====")
file_path = "../local-data/Active_Sales_Tax_Permit_Holders_20250828.csv"
df = pd.read_csv(file_path, low_memory=False)

# Standardize Cols
print("==== PROCESSING RAW DATA ====")
cols_to_str = ['Outlet County Code', 'Outlet NAICS Code']
for col in cols_to_str:
    df[col] = df[col].fillna(0).astype(str)
df.columns = df.columns.str.upper().str.replace(' ', '_')

# Select Food Retail on NAICS in Dallas County
df = df[df['OUTLET_NAICS_CODE'].str.startswith('445')]
df = df[df['OUTLET_COUNTY_CODE'] == '57.0']

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
batch_file = "../local-data/batch_input.csv"
batch_df.to_csv(batch_file, index=False, header=False)

# Now that we have our configured package, we can send a POST request to geocode batch processing
# pass locations to get just geocoding response
print("==== SEDNING PACKAGE AS POST REQUEST TO CENSUS GEOCODER ====")
url = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
files = {'addressFile': open(batch_file, 'rb')}
data = {
    'returntype': 'locations',
    'benchmark': 'Public_AR_Current'
}
response = requests.post(url, files=files, data=data)

# Now we have the responses so lets save them and parse them
print("==== SAVING AND PARSING RESULTS ====")
output_file = "../local-data/geocoded_results.csv"
with open(output_file, 'wb') as f:
    f.write(response.content)
geocoded_df = pd.read_csv(output_file, header=None)
geocoded_df.columns = [
    'ID', 'Input_Address', 'Match_Status', 'Match_Type', 'Matched_Address',
    'Coordinates', 'TIGER_Line_ID', 'Side'
]

# seperate cordinates into individual columns
geocoded_df[['Longitude', 'Latitude']] = geocoded_df['Coordinates'].str.split(',', expand=True)

# Merge the data with the original dataframe on ID
df['ID'] = df['ID'].astype(str)
geocoded_df['ID'] = geocoded_df['ID'].astype(str)
final_df = df.merge(geocoded_df[['ID', 'Latitude', 'Longitude', 'Match_Status', 'Match_Type']], on='ID', how='left')

# Save the final Data File
final_df.to_csv("../local-data/final_geocoded_output.csv", index=False)
print("Geocoding complete. Results saved to final_geocoded_output.csv")