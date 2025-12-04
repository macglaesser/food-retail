# **TEXAS FOOD RETAIL LANDSCAPE REPORT**

## Contents of this Report
1. [Executive Summary](#executive-summary)
2. [Understanding Food Deserts in Texas](#understanding-food-deserts-in-texas)
3. [Study Overview](#study-overview)
4. [Key Findings](#key-findings)
5. [County-Specific Insights](#county-specific-insights)
6. [Implications for Public Health](#implications-for-public-health)
7. [Interactive Maps](#interactive-maps)

---

## Executive Summary

This report presents findings from a comprehensive mapping study of food retail establishments across two major Texas counties: Dallas and Harris. Using a combination of USDA SNAP retailer data and Texas sales tax permit records, we identified and geocoded **9,071 food retail locations**, providing unprecedented insight into the food retail landscape of these urban regions.

**Key Highlights:**
- **3,157 food retailers** mapped in Dallas County
- **5,914 food retailers** mapped in Harris County
- **43% of all locations** are convenience stores, significantly outnumbering supermarkets
- Supermarket-to-convenience store ratios reveal potential food access challenges in both counties

This analysis provides a foundation for understanding food accessibility patterns and identifying areas where residents may face barriers to obtaining nutritious, affordable food.

---

## Understanding Food Deserts in Texas

Food deserts are socioeconomically distressed neighborhoods where residents face systemic barriers to obtaining affordable, nutritious food. According to the U.S. Department of Agriculture, a food desert is identified as a low-income census tract with either a poverty rate of 20 percent or more, a median family income below 80 percent of the statewide median, or, in metropolitan areas, a median family income below 80 percent of the surrounding metropolitan median. 

In addition, these tracts are considered low-access when at least 500 people or one-third of the population live more than one mile from the nearest supermarket, supercenter, or large grocery store in urban areas. In Texas, these conditions are compounded by geographic isolation, limited transportation options, and the high cost of healthy foods, which together restrict residents' ability to consistently access fresh produce and other healthful options. As a result, many households in these areas are forced to rely on convenience stores and fast-food outlets, reinforcing cycles of poor nutrition and food insecurity.

---

## Study Overview

This study combines two authoritative data sources to create a comprehensive map of food retail establishments:

1. **USDA SNAP Retailer Data**: Locations authorized to accept Supplemental Nutrition Assistance Program benefits
2. **Texas Sales Tax Permit Data**: Active food retail businesses with valid sales tax permits (NAICS code 445*)

By merging these datasets through deterministic address matching and geocoding unmatched locations via the U.S. Census Bureau's batch geocoding service, we achieved a solid coverage fo food retail locations for both counties, ensuring that every identified retailer can be mapped and analyzed spatially.

For detailed methodology, data sources, and reproducibility instructions, please refer to [README.md](README.md).

---

## Key Findings

### Regional Coverage

The analysis covered two of Texas's most populous counties, revealing the scale and complexity of urban food retail systems:

| County | Total Retailers | Population (2020 Census) | Retailers per 10,000 Residents |
|--------|-----------------|--------------------------|-------------------------------|
| **Dallas County** | 3,157 | 2,613,539 | 12.1 |
| **Harris County** | 5,914 | 4,731,145 | 12.5 |
| **Combined** | 9,071 | 7,344,684 | 12.4 |

Both counties show similar retailer density, with approximately 12 food retail establishments per 10,000 residents. However, the *type* of retailers available varies significantly, which has important implications for food access quality.

### Store Type Distribution

The composition of food retail options reveals a landscape dominated by convenience stores rather than full-service supermarkets:

#### Dallas County Store Types
| Store Type | Count | Percentage |
|------------|-------|------------|
| Convenience Store | 1,360 | 43.1% |
| Supermarket | 365 | 11.6% |
| Liquor Store | 249 | 7.9% |
| Discount Retail | 242 | 7.7% |
| Specialty Food | 231 | 7.3% |
| Super Store | 186 | 5.9% |
| Pharmacy | 129 | 4.1% |
| Grocery Store | 93 | 2.9% |
| Other Categories | 302 | 9.6% |

#### Harris County Store Types
| Store Type | Count | Percentage |
|------------|-------|------------|
| Convenience Store | 2,589 | 43.8% |
| Supermarket | 641 | 10.8% |
| Liquor Store | 697 | 11.8% |
| Discount Retail | 349 | 5.9% |
| Specialty Food | 263 | 4.4% |
| Super Store | 249 | 4.2% |
| Pharmacy | 239 | 4.0% |
| Grocery Store | 310 | 5.2% |
| Other Categories | 577 | 9.8% |

**Key Observation**: In both counties, convenience stores represent more than **4 out of every 10 food retailers**, while full-service supermarkets account for only about **1 in 10** establishments.

### Food Access Patterns

The ratio of supermarkets to convenience stores serves as an indicator of healthy food access within a community. Supermarkets typically offer a wider variety of fresh produce, whole grains, and lean proteins at competitive prices, while convenience stores often stock primarily processed foods with limited fresh options.

**Supermarket-to-Convenience Store Ratios:**
- **Dallas County**: 1:3.7 (1 supermarket for every 3.7 convenience stores)
- **Harris County**: 1:4.0 (1 supermarket for every 4.0 convenience stores)

These ratios suggest that residents in both counties have significantly more access to convenience stores than to full-service supermarkets. This pattern is particularly concerning for low-income neighborhoods where transportation barriers may limit residents' ability to travel longer distances to reach supermarkets with healthier, more affordable food options.

---

## County-Specific Insights

### Dallas County, Texas

**Total Food Retail Locations**: 3,157

Dallas County exhibits a diverse food retail landscape, with significant representation across multiple store categories. However, the dominance of convenience stores (43.1%) compared to supermarkets (11.6%) raises concerns about equitable access to healthy food options.

**Notable Features:**
- Strong presence of specialty food retailers (231 locations, 7.3%), indicating diverse culinary preferences and potentially serving specific ethnic communities
- 186 super stores provide bulk purchasing options, beneficial for families with transportation access
- Pharmacy food sections (129 locations) supplement traditional grocery channels
- 79 bakeries and 45 produce markets offer specialized fresh food access points

**Interactive Map**: [View Dallas County Food Retail Map](../assets/dallas/food_retail_locations_dallas.html)

#### Dallas County Advanced Analysis: Socioeconomic Correlations

Detailed statistical analysis was conducted to examine potential relationships between median income and food retail availability in Dallas County. Two key analyses were performed:

**1. Median Income vs. Store Counts**

A correlation analysis between census tract median income and the count of food retail establishments by store type revealed **no meaningful correlations**. This finding suggests that the absolute number of food retail locations is distributed relatively uniformly across Dallas County regardless of neighborhood income levels.

![Median Income vs Store Type Distribution](./assets/dallas/median_income_census_tract.png)

**2. Median Income vs. Store Densities**

Analysis of store densities (retailers per 1,000 residents) relative to median income also returned **no meaningful correlations**. This indicates that retail density patterns do not demonstrate a strong direct relationship with neighborhood wealth in Dallas County.

**Interpretation:**

The absence of significant income-based correlations is itself an important finding. It suggests that:
- Food retail distribution in Dallas is driven more by factors other than income (e.g., population density, zoning, development patterns)
- Income level alone is not a strong predictor of food retail availability in this county
- Disparities in food access are likely influenced by **store type composition** (convenience vs. supermarket) rather than total retail count or density
- Even neighborhoods with adequate retail presence may lack access to healthy food options if those retailers are primarily convenience stores

#### Dallas County: Store Type Characteristics

The following visualizations examine how different store types are distributed across Dallas County and how they relate to neighborhood characteristics:

![Gross Building Area by Store Type](./assets/dallas/gross_building_area_store_type.png)

**Key Insight**: The variation in building sizes by store type reveals important operational differences. Supermarkets and super stores show significantly larger building areas compared to convenience stores, which has implications for product selection and shopping experience.

![Gross Building Area by Cuisine Type](./assets/dallas/gross_building_area_cuisine_type.png)

**Cuisine Diversity Finding**: Dallas County shows diverse specialty food retailers across different cuisine types. The variation in building sizes across cuisine categories suggests varying operational scales for ethnic and specialty markets, reflecting the county's cultural diversity and the economic viability of different food retail niche markets.

#### Dallas County: Ethnic Cuisine Distribution and Immigration Patterns

Beyond traditional store types, Dallas County's food retail landscape reflects significant ethnic and cultural diversity. Analysis of specialty food retailers categorized by ethnic cuisine reveals distinctive geographic patterns:

![Store Locations by Ethnic Cuisine Type](./assets/dallas/store_location_ethic_cuisine.png)

**Ethnic Cuisine Patterns**: The visualization demonstrates clustering of specific cuisine types across Dallas County neighborhoods, including Americas → Central America → Mexico classifications. These patterns can be overlayed with immigrant census data potentially revealing:

- **Geographic Concentration**: Specific ethnic food retailers cluster in particular neighborhoods, suggesting established ethnic enclaves
- **Community Infrastructure**: Concentrations indicate areas where immigrant communities have developed food supply networks tailored to their cultural needs
- **Market Viability**: The presence and scale of ethnic retailers demonstrates demand for culturally appropriate foods within these communities

**Potential for Advanced Analysis**:

This data opens significant opportunities for deeper sociodemographic analysis:

1. **PowerBI Integration**: The geocoded store locations by ethnic cuisine can be visualized in PowerBI dashboards for:
   - Interactive filtering and exploration of ethnic food retail by neighborhood and cuisine type
   - Real-time updates as new stores open or close
   - Multi-layered analysis combining store density, building size, and cuisine type

2. **Immigration Census Overlay**: Future work can integrate this store data with Census Bureau immigration and ancestry data to:
   - Identify alignment between immigrant population locations and ethnic food retail availability
   - Assess whether immigrant communities have adequate access to culturally appropriate foods
   - Detect potential food access gaps in neighborhoods with significant immigrant populations but limited ethnic retail options
   - Evaluate food retail accessibility as a measure of community integration and cultural economic activity

3. **Policy Applications**:
   - Identify emerging immigrant communities and their food infrastructure needs
   - Support business development for ethnic entrepreneurs
   - Understand health and nutrition patterns in relation to food retail diversity
   - Inform immigrant integration and community development programs

This approach transforms food retail data from a simple health metrics tool into a sophisticated instrument for understanding community demographics, cultural economics, and immigrant integration patterns.

### Harris County, Texas

**Total Food Retail Locations**: 5,914

As Texas's most populous county and home to Houston, Harris County shows the largest absolute number of food retailers in this study. The retail distribution mirrors Dallas County's patterns but at a larger scale.

**Notable Features:**
- Higher absolute number of supermarkets (641) provides more options in aggregate, but ratio to convenience stores remains challenging
- Significant liquor store presence (697 locations, 11.8%) may indicate mixed-use retail patterns
- Strong specialty food and ethnic market representation (263 locations) reflects Houston's cultural diversity
- 310 grocery stores supplement supermarket access, though these may be smaller format stores

**Interactive Map**: [View Harris County Food Retail Map](../assets/harris/food_retail_locations_harris.html)



---

## Implications for Public Health

The findings from this study have several important implications for public health policy and food security interventions:

1. **Convenience Store Dependency**: With more than 40% of food retailers being convenience stores, many residents—particularly those without reliable transportation—may rely heavily on stores that typically offer limited fresh produce and healthy options at higher per-unit costs.

2. **Geographic Disparities**: While this report presents county-level statistics, the interactive maps reveal significant spatial clustering of different store types. Neighborhood-level analysis would likely reveal areas where supermarket access is severely limited.

3. **SNAP Retailer Coverage**: By including both SNAP-authorized retailers and those with sales tax permits, this study captures a more complete picture of food retail than either data source alone. This is particularly important for understanding food access among low-income populations who rely on SNAP benefits.

4. **Policy Opportunities**: 
   - Incentive programs could encourage supermarket development in underserved areas
   - Supporting convenience stores in adopting healthy food options (fresh produce, whole grains) could improve access where they are the primary option
   - Transportation initiatives could better connect residents to existing supermarkets

5. **Data Foundation**: The geocoded datasets created through this study provide a foundation for spatial analysis to identify specific food desert areas by overlaying with census data.

---

## Interactive Maps

Explore the full spatial distribution of food retailers through our interactive web maps:

- **[Dallas County Interactive Map](../assets/dallas/food_retail_locations_dallas.html)**: Click on markers to see store names and types. Use layer controls to filter by store category.
  
- **[Harris County Interactive Map](../assets/harris/food_retail_locations_harris.html)**: Click on markers to see store names and types. Use layer controls to filter by store category.

These maps allow users to:
- Visualize the concentration of different store types across the county
- Identify potential food deserts (areas with low supermarket density)
- Explore neighborhood-level retail patterns
- Assess proximity of food retailers to specific addresses or areas of interest

---

## Methodology and Reproducibility

For complete documentation of data sources, geocoding procedures, merging methodology, and instructions to reproduce this analysis for other Texas counties, please refer to **[README.md](README.md)**.

The analysis pipeline includes:
- Automated geocoding via U.S. Census Bureau batch geocoder
- Deterministic address-based matching to avoid duplicates
- NAICS code mapping to standardized store type categories
- Interactive map generation using Folium

All code is available in the `scripts/` directory of this repository.
