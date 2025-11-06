from utils.geocode_sales_tax import geocode_sales_tax_data
from utils.merge_snap_geocoded_sales_tax import merge_snap_sales_tax
import pandas as pd

# For harris County (original)
geocode_sales_tax_data(
    inputData="../local-data/state/texas/Active_Sales_Tax_Permit_Holders_20251106.csv",
    countyCode='101.0',
    naicsCode='445',
    batchOutputPath="../local-data/county/harris/sales_tax_batch_input_harris.csv",
    geocodedOutputPath="../local-data/county/harris/sales_tax_geocoded_results_harris.csv",
    finalOutputPath="../local-data/county/harris/sales_tax_geocoded_final_output_harris.csv"
)

# Harris County bounds
harris_bounds = {
    'lat_min': 29.5,
    'lat_max': 30.3,
    'lon_min': -95.8,
    'lon_max': -94.9
}

# Run merge for harris County
merge_snap_sales_tax(
    snapPath="../local-data/united-states/SNAP_Retailer_Location_data.csv",
    taxPath="../local-data/county/harris/sales_tax_geocoded_final_output_harris.csv",
    county='HARRIS',
    state='TX',
    latMin=harris_bounds['lat_min'],
    latMax=harris_bounds['lat_max'],
    lonMin=harris_bounds['lon_min'],
    lonMax=harris_bounds['lon_max'],
    outputPath="../local-data/county/harris/snap_sales_tax_merged_data_harris.csv"
)