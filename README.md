# postcode-processing-ONS
process UK postcodes downloaded from ONS

Processes ONS Postcode Directory(Aug 2025) data to enrich postcodes with:
- Country
- Region
- County
- Rural/Urban classification
- Postcode district
- latitude
- longitude

Where to download the data:
ONS postcode directory
https://geoportal.statistics.gov.uk/datasets/ons-postcode-directory-august-2025-for-the-uk/about

Also join population density data based on LAD (Local Authority District). Please note this is district level, not postcode level, which means population density is repeated across rows. When aggregating data, can take min/max/first/last.

ONS population density
https://www.ons.gov.uk/datasets/TS006/editions/2021/versions/4