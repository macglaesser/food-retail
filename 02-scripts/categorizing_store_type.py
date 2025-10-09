import pandas as pd
import re

CUISINE_KEYWORDS = {
    # ========================================================================
    # AMERICAS
    # ========================================================================
    'Mexican': {
        'category': 'Americas',
        'subcategory': 'Latin America - Central America',
        'sub_subcategory': 'Mexico',
        'keywords': [
            'taco', 'taqueria', 'mexican', 'mexico', 'el', 'la', 'los', 'las', 'mi', 
            'michoacana', 'bodega', 'carniceria', 'mercado', 'fruteria', 'amigos',
            'jalisco', 'fiesta', 'panaderia', 'monterrey', 'azteca', 'costeno', 
            'san miguel', 'delicias', 'dulceria', 'paleteria', 'paleta'
        ]
    },
    'Central American': {
        'category': 'Americas',
        'subcategory': 'Latin America - Central America',
        'sub_subcategory': 'Other Central America',
        'keywords': [
            'pupuseria', 'guatemalteca', 'salvadoreno', 'hondureno', 'nica', 'nicaragua'
        ]
    },
    'South American': {
        'category': 'Americas',
        'subcategory': 'Latin America - South America',
        'sub_subcategory': 'Multiple South American',
        'keywords': [
            'brazilian', 'colombia', 'venezuelan', 'peruvian', 'argentina', 'empanada'
        ]
    },
    'Caribbean': {
        'category': 'Americas',
        'subcategory': 'Latin America - Caribbean',
        'sub_subcategory': 'Multiple Caribbean',
        'keywords': [
            'caribbean', 'jamaica', 'jerk', 'roti', 'afribbean', 'haitian', 'cuban'
        ]
    },
    'Latino/Hispanic (General)': {
        'category': 'Americas',
        'subcategory': 'Latin America - General',
        'sub_subcategory': None,
        'keywords': [
            'latino', 'hispana', 'hispanic'
        ]
    },
    
    # ========================================================================
    # ASIA
    # ========================================================================
    # Eastern Asia
    'Chinese': {
        'category': 'Asia',
        'subcategory': 'Eastern Asia',
        'sub_subcategory': 'China',
        'keywords': [
            'chinese', 'china', 'hong kong', 'cantonese', 'szechuan', 'hunan',
            'fortune supermarket', 'wok'
        ]
    },
    'Korean': {
        'category': 'Asia',
        'subcategory': 'Eastern Asia',
        'sub_subcategory': 'Korea',
        'keywords': [
            'korean', 'korea', 'h-mart', 'h mart', 'bbq', 'barbeque', 'kimchi',
            'somunnan', 'banchannara'
        ]
    },
    'Japanese': {
        'category': 'Asia',
        'subcategory': 'Eastern Asia',
        'sub_subcategory': 'Japan',
        'keywords': [
            'japanese', 'japan', 'sushi', 'teriyaki', 'ramen', 'tokyo', 'osaka'
        ]
    },
    'Mongolian': {
        'category': 'Asia',
        'subcategory': 'Eastern Asia',
        'sub_subcategory': 'Other Eastern Asia',
        'keywords': [
            'mongolian'
        ]
    },
    
    # South Eastern Asia
    'Vietnamese': {
        'category': 'Asia',
        'subcategory': 'South Eastern Asia',
        'sub_subcategory': 'Vietnam',
        'keywords': [
            'viet', 'pho', 'saigon', 'truong nguyen', 'duc huong', 'gio cha', 'banh mi'
        ]
    },
    'Thai': {
        'category': 'Asia',
        'subcategory': 'South Eastern Asia',
        'sub_subcategory': 'Thailand',
        'keywords': [
            'thai', 'thailand', 'pad thai', 'bangkok'
        ]
    },
    'Filipino': {
        'category': 'Asia',
        'subcategory': 'South Eastern Asia',
        'sub_subcategory': 'Philippines',
        'keywords': [
            'filipino', 'philippines', 'manila', 'pancit', 'lumpia'
        ]
    },
    
    # South Central Asia
    'Indian/South Asian': {
        'category': 'Asia',
        'subcategory': 'South Central Asia',
        'sub_subcategory': 'Multiple South Central Asian',
        'keywords': [
            'indian', 'india', 'tandoor', 'curry', 'masala', 'patel brothers', 
            'deshi bazzar', 'halal', 'pakistan', 'bangladeshi', 'desi', 'rasaili rai',
            'nepal', 'sri lanka'
        ]
    },
    
    # Western Asia
    'Middle Eastern': {
        'category': 'Asia',
        'subcategory': 'Western Asia',
        'sub_subcategory': 'Multiple Western Asian',
        'keywords': [
            'mediterranean', 'middle east', 'kebab', 'gyro', 'shawarma', 'lebanese',
            'persian', 'afghan', 'anatolia', 'zabiha', 'king zabiha', 'al markaz',
            'arab', 'falafel', 'hummus', 'georgian', 'armenian'
        ]
    },
    
    # Asian General
    'Asian (General)': {
        'category': 'Asia',
        'subcategory': 'General',
        'sub_subcategory': None,
        'keywords': [
            'asian', 'asia', '99 ranch', 'hiep', 'cocohodo'
        ]
    },
    
    # ========================================================================
    # AFRICA
    # ========================================================================
    'African': {
        'category': 'Africa',
        'subcategory': 'Multiple African Regions',
        'sub_subcategory': 'Multiple African',
        'keywords': [
            'african', 'ethiopian', 'nigerian', 'habesha', 'injera', 'somali',
            'abyssinia', 'harar', 'senga', 'sega', 'kenkey', 'eritrean', 'jollof'
        ]
    },
    
    # ========================================================================
    # EUROPE
    # ========================================================================
    # Eastern Europe
    'Eastern European': {
        'category': 'Europe',
        'subcategory': 'Eastern Europe',
        'sub_subcategory': 'Multiple Eastern European',
        'keywords': [
            'polish', 'russia', 'russian', 'ukraine', 'ukrainian', 'eastern european',
            'pierogi', 'borscht'
        ]
    },
    
    # Southern Europe
    'Italian': {
        'category': 'Europe',
        'subcategory': 'Southern Europe',
        'sub_subcategory': 'Italy',
        'keywords': [
            'italian', 'italy', 'pizza', 'pasta', 'calzone', 'pizzeria', 'romas', 
            'sicily', "domino's"
        ]
    },
}


def classify_cuisine(row):
    """
    Classifies the cuisine type based on store name and store type.
    Returns a tuple: (cuisine_type, category, subcategory, sub_subcategory)
    1. Prioritizes ethnic/specific food type matches by store name.
    2. Uses STORE_TYPE for a general category fallback.
    """
    store_name = str(row['STORE_NAME']).lower()
    store_type = str(row['STORE_TYPE']).lower() if 'STORE_TYPE' in row else ''

    # Check for ethnic/cuisine matches
    for cuisine, details in CUISINE_KEYWORDS.items():
        for keyword in details['keywords']:
            pattern = r'(?<![a-z])' + re.escape(keyword) + r'(?![a-z])'
            if re.search(pattern, store_name):
                return (
                    cuisine,
                    details['category'],
                    details['subcategory'],
                    details['sub_subcategory']
                )
    
    # Fallback categories
    if 'liquor' in store_type or 'liquor' in store_name:
        return ('Liquor Store', None, None, None)
        
    if 'convenience' in store_type or 'gas' in store_type or 'supermarket' in store_type or 'market' in store_type or 'grocery' in store_type:
        return ('General Retail/Food/Other', None, None, None)
    
    return ('Uncategorized', None, None, None)


try:
    df = pd.read_csv('../local-data/foodRetailLocations.csv')
    df = df[~df['STORE_NAME'].str.contains("BATH & BODY WORKS", case=False, na=False)]    
    df = df[~df['STORE_NAME'].str.contains("DALLAS NOVELTIES & BEAUTY SUPPLY", case=False, na=False)]
    print("CSV loaded successfully. Shape:", df.shape)

    print("Classifying rows... this may take a moment.")
    
    # Apply classification and unpack results into separate columns
    classification_results = df.apply(classify_cuisine, axis=1)
    df['CUISINE_TYPE'] = classification_results.apply(lambda x: x[0])
    df['CATEGORY'] = classification_results.apply(lambda x: x[1])
    df['SUBCATEGORY'] = classification_results.apply(lambda x: x[2])
    df['SUB_SUBCATEGORY'] = classification_results.apply(lambda x: x[3])
    
    output_filename = '../local-data/CuisineRetailLocations2.csv'
    df.to_csv(output_filename, index=False)
    
    print(f"\nProcessing complete! New file saved as '{output_filename}'")
    
    ethnic_categories = [
        'Mexican', 'Central American', 'South American', 'Latino/Hispanic (General)',
        'Chinese', 'Vietnamese', 'Korean', 'Japanese', 'Thai', 'Filipino',
        'Indian/South Asian', 'Middle Eastern', 'African', 'Caribbean',
        'Eastern European', 'Italian', 'Asian (General)'
    ]
    
    print("\n" + "="*60)
    print("ETHNIC/IMMIGRANT ESTABLISHMENT DISTRIBUTION")
    print("(Primary categories for census correlation)")
    print("="*60)
    ethnic_df = df[df['CUISINE_TYPE'].isin(ethnic_categories)]
    print(ethnic_df['CUISINE_TYPE'].value_counts())
    print(f"\nTotal Ethnic Establishments: {len(ethnic_df)}")
    
    print("\n" + "="*60)
    print("HIERARCHICAL CATEGORY BREAKDOWN")
    print("="*60)
    print("\nBy Main Category:")
    print(df[df['CATEGORY'].notna()]['CATEGORY'].value_counts())
    print("\nBy Subcategory:")
    print(df[df['SUBCATEGORY'].notna()]['SUBCATEGORY'].value_counts())
    print("\nBy Sub-Subcategory:")
    print(df[df['SUB_SUBCATEGORY'].notna()]['SUB_SUBCATEGORY'].value_counts())
    
    print("\n" + "="*60)
    print("ALL CATEGORIES DISTRIBUTION (Showing Consolidation)")
    print("="*60)
    print(df['CUISINE_TYPE'].value_counts())
    
    uncategorized = df[df['CUISINE_TYPE'] == 'Uncategorized']['STORE_NAME'].unique()
    if len(uncategorized) > 0:
        print(f"\n\nRemaining Uncategorized Stores ({len(uncategorized)}):")
        print(uncategorized[:50])

except FileNotFoundError:
    print("Error: 'foodRetailLocations.csv' not found. Please make sure the file is in the correct directory.")
except Exception as e:
    print(f"An error occurred: {e}")