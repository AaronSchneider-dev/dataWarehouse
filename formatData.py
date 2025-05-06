import csv
import pandas as pd
from collections import defaultdict

# Step 1: Read the CSV and build yearly country counts
yearly_counts = defaultdict(lambda: defaultdict(int))
all_countries = set()

country_mapping = {
    "Austria-Hungary": "Austria",
    "Austrian Empire": "Austria",
    "Bavaria": "Germany",
    "Belgian Congo": "Belgium",
    "Bosnia": "Bosnia and Herzegovina",
    "British India": "India",
    "British Mandate of Palestine": "Israel",
    "British Protectorate of Palestine": "Israel",
    "British West Indies": "United Kingdom",
    "Burma": "Myanmar",
    "Czechoslovakia": "Czech Republic",
    "East Friesland": "Germany",
    "East Timor": "Timor-Leste",
    "Faroe Islands (Denmark)": "Denmark",
    "Free City of Danzig": "Poland",
    "French Algeria": "Algeria",
    "German-occupied Poland": "Poland",
    "Gold Coast": "Ghana",
    "Hesse-Kassel": "Germany",
    "Java, Dutch East Indies": "Indonesia",
    "Korea": "South Korea",
    "Mecklenburg": "Germany",
    "Ottoman Empire": "Turkey",
    "Persia": "Iran",
    "Prussia": "Germany",
    "Russian Empire": "Russia",
    "USSR": "Russia",
    "West Germany": "Germany",
    "Württemberg": "Germany",
    "Tuscany": "Italy",
    "the Netherlands": "Netherlands"
}

with open('data/rawnobel.csv', mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    for row in reader:
        if len(row) < 26:
            continue
        year = row[0].strip()
        country = row[25].strip()
        country = country_mapping.get(country, country)
        if year and country:
            yearly_counts[year][country] += 1
            all_countries.add(country)

# Step 2: Sort years and countries
years = sorted(yearly_counts.keys())
countries = sorted(all_countries)

# Step 3: Build cumulative data
cumulative_data = []
totals = {country: 0 for country in countries}

for year in years:
    row = {"Jahr": year}
    for country in countries:
        totals[country] += yearly_counts[year].get(country, 0)
        row[country] = totals[country]
    cumulative_data.append(row)

# Step 4: Convert to DataFrame and write to Excel
df = pd.DataFrame(cumulative_data)
df.to_excel("data/nobel.xlsx", index=False)