import pandas as pd
import numpy as np

# Load the CSV file (adjust separator if needed)
df = pd.read_csv('covid.csv', sep=';')
print("NaN percentage before cleaning:")
print((df.isna().mean() * 100).sort_values(ascending=False))

# List of columns to delete based on your analysis
cols_to_drop = [
    'human_development_index',
    'life_expectancy',
    'icu_patients',
    'hosp_patients',
    'total_boosters',
    'handwashing_facilities',
    'extreme_poverty',
    'hospital_beds_per_thousand',
    'reproduction_rate'
]

# Drop only these columns if they exist in the DataFrame
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

# Remove rows where code is NaN or empty
df = df[df['code'].notna() & (df['code'] != '')]

# Remove aggregates and regions (optional, but recommended)
aggregates = [
    "World", "European Union (27)", "Europe", "Asia", "Africa", "Oceania", "North America", "South America"
]
df_cleaned = df[~df['country'].isin(aggregates)]

# Remove rows where population or continent is NaN
df_cleaned = df_cleaned[df_cleaned['population'].notna() & df_cleaned['continent'].notna()]

# Forward fill cumulative columns within each country, then fill remaining NaN with 0
cumulative_cols = [
    'total_vaccinations', 'total_cases', 'total_deaths',
    'people_vaccinated', 'people_fully_vaccinated', 'total_tests'
]
for col in cumulative_cols:
    if col in df_cleaned.columns:
        df_cleaned.loc[:, col] = df_cleaned.groupby('country')[col].ffill()
        df_cleaned.loc[:, col] = df_cleaned[col].fillna(0)

# Remove duplicate rows
df_cleaned = df_cleaned.drop_duplicates()

# Ensure date is datetime and sort
df_cleaned['date'] = pd.to_datetime(df_cleaned['date'], errors='coerce')
df_cleaned = df_cleaned.sort_values(['country', 'date'])

print("\nNaN percentage after cleaning:")
print((df_cleaned.isna().mean() * 100).sort_values(ascending=False))

# Save the cleaned DataFrame
df_cleaned.to_csv('covid_cleaned.csv', sep=';', index=False)