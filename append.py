import csv
import pandas as pd

# Read the CSV files
candidates = pd.read_csv("csv/Lok Sabha/Candidates.csv", sep=";", quoting=csv.QUOTE_ALL)
shapefile = pd.read_csv("extended/source/Constituency ID mapping - 2019.csv")

# Merge using common column
merged = pd.merge(candidates, shapefile, on=['Constituency', 'State', 'Year'], how='left')

# Convert pc_id to number
merged['pc_id'] = pd.to_numeric(merged['pc_id'], errors='coerce').astype('Int64')

# Save result
merged.to_csv('extended/shapefile.csv', index=False, sep=";", quoting=csv.QUOTE_ALL)
