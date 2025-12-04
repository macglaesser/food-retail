# **TEXAS FOOD RETAILER LOCATION DISCOVERY**

## Document Overview
This documentation outlines the methodology behind discovering and mapping food retail establishments for counties in Texas. It details the data sources utilized, the step-by-step approach for geocoding and merging datasets, and the structure of the codebase developed to support reproducibility of the analysis.

A key challenge in food retail mapping lies in obtaining accurate, up-to-date data for smaller independent retailers. This project addresses that challenge through systematic geocoding, deterministic matching, and careful validation workflows. The provided datasets, code, and intermediate artifacts support full reproducibility of the analysis pipeline.

## Directory Structure

Below you will find the directory structure of the project, illustrating how data, scripts, and outputs are organized for clarity and ease of use. Note that some files listed below are not included in the repository due to size constraints and some are not yet set up for reproducibility. The files and scripts noted below with comments are essential for reproducing the current analysis.

```
FOOD-RETAIL/
├── assets/                                    
│   ├── dallas/
│   │     └── food_retail_locations_dallas.html                 # Primary output map for Dallas County
│   └── harris/
│        └── food_retail_locations_harris.html                  # Primary output map for Harris County   
│ 
├── graphs/                                                     # Work in Progress visualizations
│   ├── cuisine.ipynb
│   ├── location_size_map.ipynb                                          
│   └── location_size.ipynb      
│                              
├── local-data/                        
│   ├── county/  
│   │   ├── dallas/                                         
│   │   │    ├── ACCOUNT_APPRL_YEAR.csv
│   │   │    ├── ACCOUNT_INFO.csv
│   │   │    ├── COM_DETAIL.csv
│   │   │    ├── sales_tax_batch_input_dallas.csv               # Prepared batch input geocoding
│   │   │    ├── sales_tax_geocoded_final_output_dallas.csv     # Final geocoded output   
│   │   │    ├── sales_tax_geocoded_results_dallas.csv          # Raw geocoding results from Census batch geocoder
│   │   │    ├── snap_sales_cuisine_property_data_merged.csv
│   │   │    ├── snap_sales_tax_cuisine_merged_data.csv
│   │   │    ├── snap_sales_tax_merged_data_dallas.csv          # Merged SNAP + Sales Tax data
│   │   │    └── unmatched_retail_addresses.csv  
│   │   └── harris/
│   │   │    ├── building_other.csv
│   │   │    ├── building_res.csv
│   │   │    ├── real_acct.csv
│   │   │    ├── sales_tax_batch_input_harris.csv              # Prepared batch input geocoding
│   │   │    ├── sales_tax_geocoded_final_output_harris.csv    # Final geocoded output
│   │   │    ├── sales_tax_geocoded_results_harris.csv         # Raw geocoding results from Census batch geocoder
│   │   └──  └── snap_sales_tax_merged_data_harris.csv         # Merged SNAP + Sales Tax data                        
│   ├── state/  
│   │   └── texas/   
│   │        └── Active_Sales_Tax_Permit_Holders.csv          # Essential sales tax permit data source                       
│   └── united-states/   
│       └── SNAP_Retailer_Location_data.csv                   # Essential USDA SNAP retailer data source
│                        
├── scripts/
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── geocode_sales_tax.py                              # Geocoding utility functions
│   │   ├── maps.py                                           # Mapping utility functions
│   │   └── merge_snap_geocoded_sales_tax.py                  # Merging utility functions
│   ├── WIP-misc/                                             # Work in progress scripts
│   │   ├── categorizing_cuisine_geography.py
│   │   └── property_data_merge.py                            
│   ├── dallas-county.py                                      # Main script for Dallas County analysis   
│   └── harris-county.py                                      # Main script for Harris County analysis
│
├── venv/  
├── .gitignore                            
├── README.md
├── report.md
└── requirements.txt
```

## Essential Data Sources for Reproducibility
The methodology relies on two primary data sources for reproducing the food retail mapping:
1. **USDA SNAP Retailer Data**: This dataset provides information on retailers authorized to accept Supplemental Nutrition Assistance Program (SNAP) benefits. It includes retailer names, addresses, and geocoded locations (latitude/longitude).
2. **Sales Tax Permit Data**: This dataset contains information on businesses with active sales tax permits, which can be used to identify active retail establishments. It includes business names, addresses, and permit status.

The next three data sources are optional and not reproducible as of now, but can enhance the analysis particularly in understanding business characteristics:

3. **Account Appraisal Year**: This dataset provides appraisal values and property characteristics for businesses, which can help in assessing the economic status of food retail establishments.
4. **Account Information**: This dataset contains detailed information about business accounts, specifically their addresses for merging with the parent dataset, which can be useful for identifying and categorizing food retail establishments.
5. **Commercial Detail**: This dataset offers information on GROSS_BLDG_AREA and other commercial property details that can be useful for understanding the scale of food retail operations.

## Accessing the Data Sources
### 1. USDA Supplemental Nutrition Assistance Program (SNAP) Data
**Source**: [USDA Retail Locator](https://www.fns.usda.gov/snap/retailer-locator). 
- **Current Data**: [Active SNAP Retailers](https://usda-snap-retailers-usda-fns.hub.arcgis.com/datasets/8b260f9a10b0459aa441ad8588c2251c/explore?location=2.901026%2C-14.737150%2C2.90)
- **Documentation**: [Data Access Instructions](https://fns-prod.azureedge.us/sites/default/files/media/file/snap-retailer-locator-2023-updates.pdf)

### 2. Taxpayers With Active Sales Tax Permits
**Source**: [data.texas.gov Active Sales Tax Permit Holders](https://data.texas.gov/Government-and-Taxes/Active-Sales-Tax-Permit-Holders/jrea-zgmq/about_data)

## Methodology Overview
The methodology involves several key steps to ensure accurate identification and mapping of food retail establishments:
1. **Data Acquisition**: Download the latest versions of the USDA SNAP retailer data and sales tax permit data.
2. **Data Cleaning and Preprocessing**: Standardize and clean the datasets to ensure consistency in formats, particularly for addresses.
3. **Geocoding**: Use geocoding services to obtain latitude and longitude for addresses in the sales tax permit dataset that lack geocoded information.
4. **Deterministic Matching**: Implement deterministic matching techniques to link records from the SNAP dataset with the sales tax permit dataset based on standardized business names and addresses.
5. **Data Integration**: Merge the datasets to create a comprehensive list of food retail establishments, ensuring that duplicates are handled appropriately.
6. **Cuisine Type Sold (optional)**: Analyze the combined dataset to identify the types of cuisine sold at each establishment.
7. **Retail Size Classification (optional)**: Classify food retail establishments based on size, appraisal, and location metrics.
8. **Mapping and Visualization**: Create maps and visualizations to illustrate the distribution of food retail establishments within the specified county.

# Specific Methodology for Data Merging and Geocoding
## SNAP Retailer Data
The SNAP data is ready for immediate use with pre-geocoded coordinates.

## Sales Tax Permit Data with Geocoding
Since the sales tax data lacks coordinates, we geocode addresses using the U.S. Census Bureau's batch geocoding service. The process involves:

1. Filtering: Extract food retailers (NAICS code 445*) in a County (ex: Dallas County Code 57.0)
2. Preparation: Format addresses for batch geocoding
3. Geocoding: Submit addresses to Census batch geocoder via POST request
4. Quality Control: Review match status and match type from geocoder

[Batch Processing Documentation](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf)

## Combining Data Sources
The merge process uses deterministic matching based on composite keys (address + city + state) to identify unique retailers:

1. Standardize address fields in both datasets (uppercase, consistent formatting)
2. Create composite keys for exact matching
3. Identify tax records not already present in SNAP data
4. Map NAICS codes to store types
5. Combine datasets into unified schema

This conservative approach avoids fuzzy matching to minimize false positives while capturing retailers missing from SNAP data.

# Reproducing the Analysis

## Step 1: Installation
Create a virtual environment and install dependencies
```
`python -m venv venv`
`venv\Scripts\activate`
`pip install -r requirements.txt`
```

## Step 2: Prepare Data
Ensure the following raw data files are in `local-data/`:
- `united-states/SNAP_Retailer_Location_data.csv` (from USDA)
- `state/texas/Active_Sales_Tax_Permit_Holders_YYYYMMDD.csv` (from data.texas.gov)

## Step 3: Set Up Directory Structure for Your County

Before running the analysis, you need to establish the proper directory structure for your target county (e.g., Harris County, Travis County, etc.).

### 3.1 Create County-Specific Script
Create a new Python file in the `scripts/` directory named after your county:
```
scripts/<county-name>-county.py
```
Example: `scripts/harris-county.py` or `scripts/travis-county.py`

### 3.2 Create County Data Directories
Set up the required folder structure in both `assets/` and `local-data/`:

```bash
# Create asset directory for map outputs
mkdir assets/<county-name>

# Create data directory for intermediate files
mkdir local-data/county/<county-name>
```

## Step 4: Configure County Script Template

Copy and modify the template below into the python script you previously created for your target county. You'll need to update:
- **County Code**: Find the appropriate FIPS code from the sales tax permit data
- **County Name**: Use the official county name (e.g., 'HARRIS', 'TRAVIS')
- **Geographic Bounds**: Define lat/lon boundaries that encompass your county
- **File Paths**: Update all paths to reference your county directory

**Example Structure for Dallas:**

```python
from utils.geocode_sales_tax import geocode_sales_tax_data
from utils.merge_snap_geocoded_sales_tax import merge_snap_sales_tax
from utils.maps import map_retail_locations
import pandas as pd

# For Dallas County (original)
geocode_sales_tax_data(
    inputData="../local-data/state/texas/Active_Sales_Tax_Permit_Holders_20251106.csv",
    countyCode='57.0',
    naicsCode='445',
    batchOutputPath="../local-data/county/dallas/sales_tax_batch_input_dallas.csv",
    geocodedOutputPath="../local-data/county/dallas/sales_tax_geocoded_results_dallas.csv",
    finalOutputPath="../local-data/county/dallas/sales_tax_geocoded_final_output_dallas.csv"
)

# Dallas County bounds
dallas_bounds = {
    'lat_min': 32.0,
    'lat_max': 33.5,
    'lon_min': -97.5,
    'lon_max': -96.0
}

# Run merge for Dallas County
merge_snap_sales_tax(
    snapPath="../local-data/united-states/SNAP_Retailer_Location_data.csv",
    taxPath="../local-data/county/dallas/sales_tax_geocoded_final_output_dallas.csv",
    county='DALLAS',
    state='TX',
    latMin=dallas_bounds['lat_min'],
    latMax=dallas_bounds['lat_max'],
    lonMin=dallas_bounds['lon_min'],
    lonMax=dallas_bounds['lon_max'],
    outputPath="../local-data/county/dallas/snap_sales_tax_merged_data_dallas.csv"
)

map_retail_locations(
    inputPath="../local-data/county/dallas/snap_sales_tax_merged_data_dallas.csv",
    location=[32.7767, -96.7970],
    outputPath="../assets/dallas/food_retail_locations_dallas.html"
)
```

## Step 5: Run Scripts
Execute your county-specific script to run the full analysis pipeline:
```
cd scripts
python <county-name>-county.py
```

## Step 6: Review Outputs
Once you run this script successfully, you will find:
- Merged data in `local-data/county/<county-name>/snap_sales_tax_merged_data_<county-name>.csv`
- Interactive map in `assets/<county-name>/food_retail_locations_<county-name>.html`