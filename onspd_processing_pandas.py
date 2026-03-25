import pandas as pd
import time

start_time = time.time()

# Load the main ONS postcode data with GSS codes
df_pc = pd.read_csv("data/raw/ONSPD_AUG_2025_UK.csv")
# Select relevant columns
df_pc = df_pc[["pcds", "ctry25cd", "rgn25cd", "cty25cd", "ruc11ind", "ruc21ind", "lat", "long"]]

# load lookup tables: country, region, county
df_country = pd.read_csv('data/raw/CTRY Country names and codes UK as at 05_25.csv', usecols=['CTRY25CD', 'CTRY25NM'])
df_region = pd.read_csv('data/raw/RGN Region names and codes EN as at 05_25.csv', usecols=['RGN25CD', 'RGN25NM'])
df_county = pd.read_csv('data/raw/CTY County names and codes UK as at 05_25.csv', usecols=['CTY25CD', 'CTY25NM'])

# load lookup tables: rural/urban classification for England/Wales and Scotland, and combine them into one table
df_ruc_ew = pd.read_csv('data/raw/RUC21 Rural Urban (2021) Indicator names and codes EW as at 05_25.csv')
df_ruc_sc = pd.read_csv('data/raw/RUC21 Rural Urban (2021) Indicator names and codes SC as at 05_25.csv')
# Add a new column to indicate urban/rural status for Scotland
df_ruc_sc['Urban_rural_flag'] = ['Urban', 'Urban', 'Rural', 'Rural', 'Rural', 'Rural']
# Combine the England/Wales and Scotland rural/urban classification tables
df_ruc21 = pd.concat([df_ruc_ew, df_ruc_sc], axis=0, ignore_index=True)

# Merge the lookup tables with the main postcode dataframe
df_pc = df_pc.merge(df_country, left_on='ctry25cd', right_on='CTRY25CD', how='left')
df_pc = df_pc.merge(df_region, left_on='rgn25cd', right_on='RGN25CD', how='left')
df_pc = df_pc.merge(df_county, left_on='cty25cd', right_on='CTY25CD', how='left')
df_pc = df_pc.merge(df_ruc21, left_on='ruc21ind', right_on='RUC21IND', how='left')

# Select and reorder columns for the final output
df_pc = df_pc[["pcds", "CTRY25NM", "RGN25NM", "CTY25NM", "RUC21DESC", "Urban_rural_flag", "lat", "long"]]

rename_columns = {
    "pcds": "postcode",
    "CTRY25NM": "country",
    "RGN25NM": "region",
    "CTY25NM": "county",
    "RUC21DESC": "rural_urban_classification"
}
df_pc = df_pc.rename(columns=rename_columns)

# Save the processed dataframe to a new CSV file
df_pc.to_csv('data/output/ons_postcode_processed.csv', index=False)

end_time = time.time()
print(f"Processing time: {end_time-start_time:.2f} seconds")