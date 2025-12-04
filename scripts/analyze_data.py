import pandas as pd
import os

# Analyze Dallas County data
dallas_path = "../local-data/county/dallas/snap_sales_tax_merged_data_dallas.csv"
harris_path = "../local-data/county/harris/snap_sales_tax_merged_data_harris.csv"

print("=" * 60)
print("DALLAS COUNTY ANALYSIS")
print("=" * 60)

if os.path.exists(dallas_path):
    df_dallas = pd.read_csv(dallas_path)
    print(f"\nTotal Records: {len(df_dallas)}")
    print(f"\nColumns: {list(df_dallas.columns)}")
    
    if 'DATA_SOURCE' in df_dallas.columns:
        print(f"\nData Sources:\n{df_dallas['DATA_SOURCE'].value_counts()}")
    
    if 'STORE_TYPE' in df_dallas.columns:
        print(f"\nTop 10 Store Types:\n{df_dallas['STORE_TYPE'].value_counts().head(10)}")
    
    print(f"\nSample Data:\n{df_dallas.head()}")

print("\n" + "=" * 60)
print("HARRIS COUNTY ANALYSIS")
print("=" * 60)

if os.path.exists(harris_path):
    df_harris = pd.read_csv(harris_path)
    print(f"\nTotal Records: {len(df_harris)}")
    
    if 'DATA_SOURCE' in df_harris.columns:
        print(f"\nData Sources:\n{df_harris['DATA_SOURCE'].value_counts()}")
    
    if 'STORE_TYPE' in df_harris.columns:
        print(f"\nTop 10 Store Types:\n{df_harris['STORE_TYPE'].value_counts().head(10)}")
