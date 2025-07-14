import pandas as pd
from datetime import datetime

# Load cleaned data
df = pd.read_csv('covid_cleaned.csv', sep=';')
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Step 1: Create Dimension Tables

# dim_country: Use 'code' as the unique identifier (no artificial country_id needed)
dim_country = df[['country', 'code', 'continent', 'population', 'population_density',
                  'median_age', 'gdp_per_capita']].drop_duplicates().reset_index(drop=True)

# dim_date
dim_date = df[['date']].drop_duplicates()
dim_date['year'] = dim_date['date'].dt.year
dim_date['month'] = dim_date['date'].dt.month
dim_date['quarter'] = dim_date['date'].dt.quarter
dim_date['week'] = dim_date['date'].dt.isocalendar().week
dim_date['day'] = dim_date['date'].dt.day
dim_date = dim_date.rename(columns={'date': 'date_id'})

# Step 2: Create Fact Table

# Merge code into fact table (no country_id needed)
df_fact = df.merge(dim_country, on=['country', 'code', 'continent', 'population',
                                    'population_density', 'median_age', 'gdp_per_capita'])

# Merge on date_id
df_fact = df_fact.merge(dim_date, left_on='date', right_on='date_id')

# Create fact_covid
fact_covid = df_fact[[
    'code', 'date_id',
    'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
    'stringency_index',
    'total_tests', 'new_tests', 'positive_rate', 'tests_per_case',
    'total_vaccinations', 'people_vaccinated',
    'people_fully_vaccinated', 'new_vaccinations'
]]

# Step 3: Export All Tables to CSV

dim_country.to_csv('dim_country.csv', index=False)
dim_date.to_csv('dim_date.csv', index=False)
fact_covid.to_csv('fact_covid.csv', index=False)

print("CSVs created successfully");