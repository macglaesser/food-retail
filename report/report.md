# FOOD RETAIL AVAILABILITY REPORT
## Executive summary
This project assembles a reproducible pipeline to geocode and merge administrative datasets to produce a reproducible, up-to-date map of food retail establishments in a given County, contingent on data availability. The developed methodology provides a framework for researchers and policymakers to identify locations within a given county that are underserved or lack adequate food retail options.

## Essential Data Sources for Reproducibility
The methodology relies on two primary data sources for reproducing the food retail mapping:
1. **USDA SNAP Retailer Data**: This dataset provides information on retailers authorized to accept Supplemental Nutrition Assistance Program (SNAP) benefits. It includes retailer names, addresses, and geocoded locations (latitude/longitude).
2. **Sales Tax Permit Data**: This dataset contains information on businesses with active sales tax permits, which can be used to identify active retail establishments. It includes business names, addresses, and permit status.

The next three data sources are optional but can enhance the analysis particularly in understanding business characteristics:

3. **Account Appraisal Year**: This dataset provides appraisal values and property characteristics for businesses, which can help in assessing the economic status of food retail establishments.
4. **Account Information**: This dataset contains detailed information about business accounts, specifically their addresses for merging with the parent dataset, which can be useful for identifying and categorizing food retail establishments.
5. **Commercial Detail**: This dataset offers information on GROSS_BLDG_AREA and other commercial property details that can be useful for understanding the scale of food retail operations.

## Methodology Overview
The methodology involves several key steps to ensure accurate identification and mapping of food retail establishments:
1. **Data Acquisition**: Download the latest versions of the USDA SNAP retailer data and sales tax permit data.
2. **Data Cleaning and Preprocessing**: Standardize and clean the datasets to ensure consistency in formats, particularly for addresses.
3. **Geocoding**: Use geocoding services to obtain latitude and longitude for addresses in the sales tax permit dataset that lack geocoded information.
4. **Deterministic Matching**: Implement deterministic matching techniques to link records from the SNAP dataset with the sales tax permit dataset based on standardized business names and addresses.
5. **Data Integration**: Merge the datasets to create a comprehensive list of food retail establishments, ensuring that duplicates are handled appropriately.
6. **Cuisine Type Sold**: Analyze the combined dataset to identify the types of cuisine sold at each establishment.
7. **Retail Size Classification**: Classify food retail establishments based on size, appraisal, and location metrics.
8. **Mapping and Visualization**: Create maps and visualizations to illustrate the distribution of food retail establishments within the specified county.

# Dallas County, Texas Food Retail Mapping
This section provides the deliverables and insights of the above methodology applied to Dallas County, Texas. Please review the README.md for more information on project structure, data sources, and scripts used in the analysis. 