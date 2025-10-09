import pandas as pd
import re

# ==============================================================================
# UPDATED KEYWORD DICTIONARY
# ETHNIC CATEGORIES remain separate.
# All other non-Liquor categories are consolidated into 'General Retail/Food/Other'.
# ==============================================================================
CUISINE_KEYWORDS = {
    # --------------------------------------------------------------------------
    # ETHNIC/IMMIGRANT CATEGORIES (Prioritized)
    # --------------------------------------------------------------------------
    'Mexican': [
        'taco', 'taqueria', 'mexican', 'mexico', 'el', 'la', 'los', 'las', 'mi', 
        'michoacana', 'bodega', 'carniceria', 'mercado', 'fruteria', 'amigos',
        'jalisco', 'fiesta', 'panaderia', 'monterrey', 'azteca', 'costeno', 
        'san miguel', 'delicias', 'dulceria', 'paleteria', 'paleta'
    ],
    'Central American': [
        'pupuseria', 'guatemalteca', 'salvadoreno', 'hondureno', 'nica', 'nicaragua'
    ],
    'South American': [
        'brazilian', 'colombia', 'venezuelan', 'peruvian', 'argentina', 'empanada'
    ],
    'Latino/Hispanic (General)': [
        'latino', 'hispana', 'hispanic'
    ],
    'Chinese': [
        'chinese', 'china', 'hong kong', 'cantonese', 'szechuan', 'hunan',
        'fortune supermarket', 'wok', 'mongolian'
    ],
    'Vietnamese': [
        'viet', 'pho', 'saigon', 'truong nguyen', 'duc huong', 'gio cha', 'banh mi'
    ],
    'Korean': [
        'korean', 'korea', 'h-mart', 'h mart', 'bbq', 'barbeque', 'kimchi',
        'somunnan', 'banchannara'
    ],
    'Japanese': [
        'japanese', 'japan', 'sushi', 'teriyaki', 'ramen', 'tokyo', 'osaka'
    ],
    'Thai': [
        'thai', 'thailand', 'pad thai', 'bangkok'
    ],
    'Filipino': [
        'filipino', 'philippines', 'manila', 'pancit', 'lumpia'
    ],
    'Indian/South Asian': [
        'indian', 'india', 'tandoor', 'curry', 'masala', 'patel brothers', 
        'deshi bazzar', 'halal', 'pakistan', 'bangladeshi', 'desi', 'rasaili rai',
        'nepal', 'sri lanka'
    ],
    'Middle Eastern': [
        'mediterranean', 'middle east', 'kebab', 'gyro', 'shawarma', 'lebanese',
        'persian', 'afghan', 'anatolia', 'zabiha', 'king zabiha', 'al markaz',
        'arab', 'falafel', 'hummus'
    ],
    'African': [
        'african', 'ethiopian', 'nigerian', 'habesha', 'injera', 'somali',
        'abyssinia', 'harar', 'senga', 'sega', 'kenkey', 'eritrean', 'jollof'
    ],
    'Caribbean': [
        'caribbean', 'jamaica', 'jerk', 'roti', 'afribbean', 'haitian', 'cuban'
    ],
    'Eastern European': [
        'polish', 'russia', 'russian', 'ukraine', 'ukrainian', 'eastern european',
        'pierogi', 'borscht', 'georgian', 'armenian'
    ],
    'Italian': [
        'italian', 'italy', 'pizza', 'pasta', 'calzone', 'pizzeria', 'romas', 
        'sicily', "domino's"
    ],
    'Asian (General)': [
        'asian', 'asia', '99 ranch', 'hiep', 'cocohodo'
    ],
    
    # --------------------------------------------------------------------------
    # CONSOLIDATED GENERAL RETAIL/FOOD/OTHER CATEGORY
    # All non-ethnic/non-liquor keywords are placed here.
    # --------------------------------------------------------------------------
    'General Retail/Food/Other': [
        # Seafood
        'seafood', 'fish', 'oyster', 'shrimp', 'crawfish', 'crab',
        # Bakery/Dessert/Sweets
        'bakery', 'donut', 'donuts', 'cake', 'cakes', 'sweet', 'sweets',
        'ice cream', 'dessert', 'kolache', 'candy', 'cupcake', 'pastry', 
        'creamery', 'custard', 'bundt', 'macaron', 'chocolate', 'frozen custard', 
        'shaved ice', 'frostbite', 'frostbites', 'gelato', 'frosty', 'artisan pops', 
        'praline', 'gourmet gifts', 'toffee', 'dounts', 'doughnuts', 'creamistry', 
        'hypnotic', 'sprinkles', 'baskin robbins', 'dunkin', 'shipley', 'popcorn', 
        'corn shoppe', 'cookies', 'edible arrangements', 'bakeshop', 'velvet whisk', 
        'bakes', 'treetz', 'treats', 'van leeuwen', 'laderach', 'kokopelli', 
        'macarons', 'banana bread', 'bakers dozen', 'confection', 'snacks',
        'daylight', 'cajun donuts', 'yum', 'yummy', 'yumilicious',
        # Juice/Smoothie/Coffee
        'juice', 'jamba', 'smoothie', 'pressed', 'coffee', 'espresso', 'ascension',
        'graph coffee', 'drip coffee', 'tea company', 'drip',
        # Specialty/Gourmet
        'spice', 'trading company', 'spices', 'gourmet', 'olive', 'vinegar',
        'extract', 'extracts', 'syrup', 'syrups', 'whole foods', 'sprouts', 
        'market street', 'central market', 'penzeys', 'stocks & bondy', 'infused oils', 
        'saladmaster', 'omaha steaks', 'scardello', 'jam', 'jams', 'pepper palace', 
        'canning', 'charcuterie', 'queso', 'southern spoon', 'feeding souls', 
        'french garden', 'fireworks', 'firecrackers', 'botanist brewer', 'ginger beer', 
        'booze baggers', 'beyond booze', 'marketplace', 'boxed bites', 'bits', 'bites',
        'deli', 'sub', 'subway',
        # Butcher/Meat Market & BBQ/Smokehouse
        'meat market', 'butcher', 'meat', 'sausage', 'renko sausage', 'classic meat',
        'smokehouse', 'baby back', 'bbq', 'barbeque',
        # Prepared Foods/Catering & Health/Wellness
        'catering', 'prepared', 'kitchen', 'mama technologies', 'chuchu grocery & catering',
        'snap kitchen', 'diabetes health', 'wellness', 'cbd', 'kratom',
        # Vending/Convenience Services & International Grocery
        'vending', 'ice vending', 'water', 'sparkletts', 'aqua bella', 'rapido ice',
        'luxury inn', 'dallas vending', 'jubel vending', 'frutihielo', 'mundos ice',
        'international', 'import', 'global', 'uac international', 'globex',
        'wrights family food', 'jtc bless', 'komart', 'hope & faith international',
        # Major Grocery Chains
        'kroger', 'walmart', 'target', 'costco', "sam's club", 'aldi', 'food lion', 
        'foodland', 'cash saver', 'crest foods',
        # Convenience/Gas Stations
        "braum's", 'shell', 'exxon', '7-eleven', 'chevron', 'bp', 'valero',
        'racetrac', 'qt', 'quiktrip', 'stop-n-go', 'food mart', 'beverage',
        'convenience', 'gas',
        # Discount/Dollar Stores & Chain Pharmacies
        'dollar general', 'dollar tree', 'family dollar', 'savers cost plus',
        "malone's cost plus", '99 cent', 'discount', 'dollartree',
        'cvs', 'walgreens', 'rite aid',
        # General Grocery/Market & Farmers Market/Farm Stand
        'grocery', 'market', 'superstore', 'food store', 'richland market',
        "jimmy's food", 'az food', 'dallas superstore', 'tailoring & grocery',
        'mac arthur irving', 'addison', 'carnival', 'mecato market', 'supermarket',
        'farm', 'farms', 'farmer', 'farmers', 'orchard', 'produce', 'kelley produce',
        # Religious/Cultural & Non-Food/Other
        'libreria catolica', 'san judas', 'religious', 'cultural',
        'medical', 'jewelry', 'tailoring', 'bead'
    ]
}

def classify_cuisine(row):
    """
    Classifies the cuisine type based on store name and store type.
    1. Prioritizes ethnic/specific food type matches by store name.
    2. Uses STORE_TYPE for a general category fallback.
    """
    store_name = str(row['STORE_NAME']).lower()
    store_type = str(row['STORE_TYPE']).lower() if 'STORE_TYPE' in row else ''

    for cuisine, keywords in CUISINE_KEYWORDS.items():
        for keyword in keywords:
            pattern = r'(?<![a-z])' + re.escape(keyword) + r'(?![a-z])'
            if re.search(pattern, store_name):
                return cuisine
    
    
    if 'liquor' in store_type or 'liquor' in store_name:
        return 'Liquor Store'
        
    if 'convenience' in store_type or 'gas' in store_type or 'supermarket' in store_type or 'market' in store_type or 'grocery' in store_type:
        return 'General Retail/Food/Other'
    
    return 'Uncategorized'

try:
    df = pd.read_csv('../local-data/foodRetailLocations.csv')
    df = df[~df['STORE_NAME'].str.contains("BATH & BODY WORKS", case=False, na=False)]    
    df = df[~df['STORE_NAME'].str.contains("DALLAS NOVELTIES & BEAUTY SUPPLY", case=False, na=False)]
    print("CSV loaded successfully. Shape:", df.shape)

    print("Classifying rows... this may take a moment.")
    df['CUISINE_TYPE'] = df.apply(classify_cuisine, axis=1)
    
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