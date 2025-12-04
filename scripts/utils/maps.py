import pandas as pd
import folium

def map_retail_locations(inputPath, location, outputPath):
    df = pd.read_csv(inputPath)
    m = folium.Map(location=location, zoom_start=10)

    store_types = df['STORE_TYPE'].unique()

    store_type_colors = {
        'Convenience Store': 'red',
        'Discount Retail': 'darkblue',
        'Pharmacy': 'lightgreen',
        'Supermarket': 'blue',
        'Other': 'green',
        'Grocery Store': 'purple',
        'Super Store': 'orange',
        'Farmers and Markets': 'gray',
        'Specialty Store': 'pink',
        'Liquor Store': 'darkred',        
        'Confectionery': 'purple',        
        'Food Store': 'darkgreen',        
        'Produce Market': 'lightgreen',   
        'Seafood Market': 'cadetblue',    
        'Meat Market': 'darkred',
        'Bakery': 'lightblue',         
        'Specialty Food': 'darkgreen'
    }

    feature_groups = {}
    for store_type in store_types:
        feature_groups[store_type] = folium.FeatureGroup(name=store_type, show=False)

    for idx, row in df.iterrows():
        if pd.notna(row['LATITUDE']) and pd.notna(row['LONGITUDE']):
            store_type = row['STORE_TYPE']
            popup_text = f"<b>{row['STORE_NAME']}</b><br>Type: {store_type}"
            
            folium.Marker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color=store_type_colors[store_type], icon='info-sign')
            ).add_to(feature_groups[store_type])

    for fg in feature_groups.values():
        fg.add_to(m)

    folium.LayerControl().add_to(m)
    
    # Save the map as an HTML file
    m.save(outputPath)