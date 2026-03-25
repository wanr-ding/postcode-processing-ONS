import polars as pl 
import time
start_time = time.time()

df_pc = pl.read_csv('data/raw/ONSPD_AUG_2025_UK.csv', dtypes={'ruc21ind': pl.Utf8})
df_pc = df_pc.select(["pcds", "ctry25cd", "rgn25cd", "cty25cd", "ruc21ind", "lat", "long"])
df_country = pl.read_csv('data/raw/CTRY Country names and codes UK as at 05_25.csv', has_header=True)
df_region = pl.read_csv('data/raw/RGN Region names and codes EN as at 05_25.csv', has_header=True)
df_county = pl.read_csv('data/raw/CTY County names and codes UK as at 05_25.csv', has_header=True)
df_ruc_ew = pl.read_csv('data/raw/RUC21 Rural Urban (2021) Indicator names and codes EW as at 05_25.csv', has_header=True)
df_ruc_sc = pl.read_csv('data/raw/RUC21 Rural Urban (2021) Indicator names and codes SC as at 05_25.csv', has_header=True)
df_ruc_sc = df_ruc_sc.with_columns(pl.Series('Urban_rural_flag', ['Urban', 'Urban', 'Rural', 'Rural', 'Rural', 'Rural']))
df_ruc21 = pl.concat([df_ruc_ew, df_ruc_sc], how='vertical')
df_pc = df_pc.join(df_country, left_on='ctry25cd', right_on='CTRY25CD', how='left')
df_pc = df_pc.join(df_region, left_on='rgn25cd', right_on='RGN25CD', how='left')
df_pc = df_pc.join(df_county, left_on='cty25cd', right_on='CTY25CD', how='left')
df_pc = df_pc.join(df_ruc21, left_on='ruc21ind', right_on='RUC21IND', how='left')
df_pc = df_pc.select(["pcds", "CTRY25NM", "RGN25NM", "CTY25NM", "RUC21DESC", "Urban_rural_flag", "lat", "long"])
df_pc.write_csv('data/output/ons_postcode_processed_polars.csv')

end_time = time.time()
print(f"Processing time (polars): {end_time-start_time:.2f} seconds")