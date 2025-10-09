
# **DALLAS COUNTY FOOD RETAILER LANDSCAPE**

## Dallas Food Desert Definition
Dallas food deserts are socioeconomically distressed neighborhoods where residents face systemic barriers to obtaining affordable, nutritious food. According to the U.S. Department of Agriculture, a food desert is identified as a low-income census tract with either a poverty rate of 20 percent or more, a median family income below 80 percent of the statewide median, or, in metropolitan areas, a median family income below 80 percent of the surrounding metropolitan median. In addition, these tracts are considered low-access when at least 500 people or one-third of the population live more than one mile from the nearest supermarket, supercenter, or large grocery store in urban areas. In Dallas, these conditions are compounded by geographic isolation, limited transportation options, and the high cost of healthy foods, which together restrict residents’ ability to consistently access fresh produce and other healthful options. As a result, many households in these areas are forced to rely on convenience stores and fast-food outlets, reinforcing cycles of poor nutrition and food insecurity.

## Overview
This project presents a comprehensive methodology for identifying and mapping active food retail establishments across Dallas County, Texas. The primary objective is to produce a reproducible, up-to-date map of active food retail outlets by combining two complementary data sources: USDA SNAP retailer records and Texas sales tax permit data.

A key challenge in food retail mapping lies in obtaining accurate, up-to-date data for smaller independent retailers. This project addresses that challenge through systematic geocoding, deterministic matching, and careful validation workflows. The provided datasets, code, and intermediate artifacts support full reproducibility of the analysis pipeline.

## Research Goals
- Produce a reproducible, up-to-date map of active food retail outlets in Dallas County
- Combine SNAP and sales tax data to achieve broader coverage than either source alone
- Provide code and intermediate artifacts that support reproducibility of geocoding, matching, and mapping workflows
- Generate the final dataset (local-data/foodRetailLocations.csv) for research and analysis

## Project Structure
```
priv-study/
├── 01-eda-notebooks/                                    # View Basic ERA
│   ├── active_snap.ipynb
│   ├── merging.ipynb
│   └── sales_tax.ipynb
├── 02-scripts/
│   ├── merge.py                                         # Script to Merge SNAP and Tax data
│   └── sales_tax.py                                     # Script to geocode Lat/Long for Tax Data
├── local-data/ 
│   ├── Active_Sales_Tax_Permit_Holders_20250828.csv     # Sales Tax download       
│   ├── batch_input.csv                                  # Intermidate sales tax
│   ├── final_geocoded_output.csv                        # Sales Tax with lat and long
│   ├── foodRetailLocations.csv                          # The final enriched Dataset
│   ├── geocoded_results.csv                             # Intermidiate sales tax
│   ├── merged_data.csv                                  # SNAP + Tax w/o custom store types
│   └── SNAP_Retailer_Location_Data.csv                  # Active SNAP download
├── graphs/
│   └── graphs.ipynb                                     # Example Graph for R Script  
├── README.md
└── requirements.txt
```

## Data Sources

### 1. USDA Supplemental Nutrition Assistance Program (SNAP) Data
**Source**: [USDA Retail Locator](https://www.fns.usda.gov/snap/retailer-locator). 
- **Current Data**: [Active SNAP Retailers](https://usda-snap-retailers-usda-fns.hub.arcgis.com/datasets/8b260f9a10b0459aa441ad8588c2251c/explore?location=2.901026%2C-14.737150%2C2.90)
- **Documentation**: [Data Access Instructions](https://fns-prod.azureedge.us/sites/default/files/media/file/snap-retailer-locator-2023-updates.pdf)

### 2. Taxpayers With Active Sales Tax Permits
**Source**: [data.texas.gov Active Sales Tax Permit Holders](https://data.texas.gov/Government-and-Taxes/Active-Sales-Tax-Permit-Holders/jrea-zgmq/about_data)

SNAP retailers are businesses authorized by the U.S. Department of Agriculture (USDA) to accept Supplemental Nutrition Assistance Program benefits for eligible food purchases.

**Strengths:**

- High data quality with standardized geocoding (latitude/longitude)
- Current and historical coverage (2004-2024)
- Regular updates and validation by USDA

**Limitations:**

- Limited to SNAP-authorized retailers only
- Excludes retailers that choose not to participate in SNAP
- May underrepresent higher-end retailers and specialty food stores

### Sales Tax Permit Dataset
This comprehensive dataset includes all Texas businesses with active sales tax permits, encompassing food retailers alongside other business types.

**Strengths**
- Broader coverage of retail establishments
- Current and frequently updated
- Includes retailers regardless of SNAP participation

**Limitations**
- Lacks geocoded coordinates (address-only)
- Requires filtering to isolate food retailers (NAICS code 445)
- Requires geocoding step to obtain coordinates


&nbsp;
# Methodology
## Approach 1: SNAP Retailer Data
The original methodology relied on historical SNAP retailer records, which required estimating which stores remained operational. By switching to USDA's published list of active SNAP retailers, we eliminate guesswork about store status and gain a definitive snapshot of currently operating SNAP-authorized food retailers.

The SNAP data is ready for immediate use with no missing values in fields of interest and includes pre-geocoded coordinates.

## Approach 2: Sales Tax Permit Data with Geocoding
Since the sales tax data lacks coordinates, we geocode addresses using the U.S. Census Bureau's batch geocoding service. The process involves:

1. Filtering: Extract food retailers (NAICS code 445*) in Dallas County (county code 57.0)
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

# Codebase Walk Through

## Data Files in local-data/

- `SNAP_Retailer_Location_data.csv` — Raw USDA SNAP active retailer dataset
- `Active_Sales_Tax_Permit_Holders_YYYYMMDD.csv` — Raw Texas sales tax permit dataset
- `batch_input.csv` — Prepared CSV for Census batch geocoder
- `geocoded_results.csv` — Raw response from Census batch geocoder POST request
- `final_geocoded_output.csv` — Sales tax records merged with geocoder results (includes Latitude, Longitude, Match_Status, Match_Type)
- `merged_data.csv` — Combined SNAP + non-duplicated tax records
- `foodRetailLocations.csv` — Final enriched dataset for mapping and analysis (primary output)

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
- `SNAP_Retailer_Location_data.csv` (from USDA)
- `Active_Sales_Tax_Permit_Holders_YYYYMMDD.csv` (from data.texas.gov)

```
cd 02-scripts
python sales_tax.py
```
This script:
- Filters sales tax data to food retailers (NAICS 445*) in Dallas County
- Prepares addresses for batch geocoding
- Posts to Census batch geocoder API
- Saves geocoded results with coordinates

Outputs:
- local-data/batch_input.csv
- local-data/geocoded_results.csv
- local-data/final_geocoded_output.csv

## Step 3: Merge Data
```
cd 02-scripts (if not already here)
python merge.py
```

This script:
- Compares compares existing Retail Locations in `SNAP_Retailer_Location_data.csv` with `final_geocoded_output.csv`
- If it exists in SNAP ignore, else inject into the dataframe

Outputs:
- `local-data/foodRetailLocations.csv`

## Step 4: Create Cusine Types for Ethnicity and Racial Observance
```
cd 02-scripts (if not already here)
python categorizing_store_type.py
```

This script:
- Uses predefined key words located within store names to create groups of cusine types

Outputs:
- `local-data/CusineRetailLocations.csv`