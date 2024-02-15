import csv
import pandas as pd

# Read the CSV files
candidates = pd.read_csv("csv/Lok Sabha/Candidates.csv", sep=";", quoting=csv.QUOTE_ALL)
mapping = pd.read_csv("extended/source/Constituency ID mapping - 2019.csv")

# Merge using common column
merged = pd.merge(candidates, mapping, on=['Constituency', 'State'], how='left')

# Convert pc_id to number
merged['pc_id'] = pd.to_numeric(merged['pc_id'], errors='coerce').astype('Int64')
merged['Code'] = pd.to_numeric(merged['Code'], errors='coerce').astype('Int64')

# Drop duplicate year column
merged = merged.drop('Year_y', axis=1)

# Save result
merged.to_csv('extended/Candidates.csv', index=False, sep=";", quoting=csv.QUOTE_ALL)
