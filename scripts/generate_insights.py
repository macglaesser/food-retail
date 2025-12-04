import pandas as pd

# Load both datasets
df_dallas = pd.read_csv('../local-data/county/dallas/snap_sales_tax_merged_data_dallas.csv')
df_harris = pd.read_csv('../local-data/county/harris/snap_sales_tax_merged_data_harris.csv')

print("=" * 70)
print("COMPREHENSIVE TEXAS FOOD RETAIL ANALYSIS")
print("=" * 70)

# County comparisons
print("\n### COUNTY COMPARISON ###")
print(f"Dallas County Total Retailers: {len(df_dallas):,}")
print(f"Harris County Total Retailers: {len(df_harris):,}")
print(f"Combined Total: {len(df_dallas) + len(df_harris):,}")

# Store type distribution comparison
print("\n### STORE TYPE DISTRIBUTION ###")
print("\nDallas County:")
print(df_dallas['STORE_TYPE'].value_counts())
print("\nHarris County:")
print(df_harris['STORE_TYPE'].value_counts())

# Calculate percentages for convenience stores
dallas_convenience_pct = (df_dallas['STORE_TYPE'].value_counts().get('Convenience Store', 0) / len(df_dallas)) * 100
harris_convenience_pct = (df_harris['STORE_TYPE'].value_counts().get('Convenience Store', 0) / len(df_harris)) * 100

dallas_supermarket_pct = (df_dallas['STORE_TYPE'].value_counts().get('Supermarket', 0) / len(df_dallas)) * 100
harris_supermarket_pct = (df_harris['STORE_TYPE'].value_counts().get('Supermarket', 0) / len(df_harris)) * 100

print(f"\n### PERCENTAGE ANALYSIS ###")
print(f"Dallas - Convenience Stores: {dallas_convenience_pct:.1f}%")
print(f"Harris - Convenience Stores: {harris_convenience_pct:.1f}%")
print(f"\nDallas - Supermarkets: {dallas_supermarket_pct:.1f}%")
print(f"Harris - Supermarkets: {harris_supermarket_pct:.1f}%")

# Check for data source if available
if 'DATA_SOURCE' in df_dallas.columns:
    print(f"\n### DATA SOURCE BREAKDOWN (Dallas) ###")
    print(df_dallas['DATA_SOURCE'].value_counts())

# Geographic coverage
print(f"\n### GEOGRAPHIC COVERAGE ###")
dallas_with_coords = df_dallas[['LATITUDE', 'LONGITUDE']].dropna()
harris_with_coords = df_harris[['LATITUDE', 'LONGITUDE']].dropna()
print(f"Dallas - Geocoded locations: {len(dallas_with_coords):,} ({(len(dallas_with_coords)/len(df_dallas))*100:.1f}%)")
print(f"Harris - Geocoded locations: {len(harris_with_coords):,} ({(len(harris_with_coords)/len(df_harris))*100:.1f}%)")

# Healthy food access (Supermarkets vs Convenience Stores ratio)
dallas_healthy_ratio = df_dallas['STORE_TYPE'].value_counts().get('Supermarket', 0) / df_dallas['STORE_TYPE'].value_counts().get('Convenience Store', 1)
harris_healthy_ratio = df_harris['STORE_TYPE'].value_counts().get('Supermarket', 0) / df_harris['STORE_TYPE'].value_counts().get('Convenience Store', 1)

print(f"\n### HEALTHY FOOD ACCESS INDICATOR ###")
print(f"Supermarket-to-Convenience Store Ratio:")
print(f"  Dallas: 1:{1/dallas_healthy_ratio:.2f} (1 supermarket per {1/dallas_healthy_ratio:.1f} convenience stores)")
print(f"  Harris: 1:{1/harris_healthy_ratio:.2f} (1 supermarket per {1/harris_healthy_ratio:.1f} convenience stores)")
