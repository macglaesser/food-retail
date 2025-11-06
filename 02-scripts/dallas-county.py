from utils.geocode_sales_tax import geocode_sales_tax_data
from utils.merge_snap_geocoded_sales_tax import merge_snap_sales_tax
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