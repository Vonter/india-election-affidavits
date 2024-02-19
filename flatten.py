import csv
import glob
import logging
import numpy as np
import os
import pandas as pd
import re
import sys
import zipfile

from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

def read_html(file_content):
    try:
        # Parse the HTML file
        soup = BeautifulSoup(file_content, 'html.parser')
    except:
        logging.error("Failed to parse HTML")
        raise

    return soup

def parse_html(soup):
    # Create an empty list to store the table data
    data = []

    # Create an empty list to store the table headers
    list_header = []

    try:
        # Find the table and extract the headers
        header = soup.find("table", id="table1").find("tr")
    except:
        logging.warning("No table found")
        raise

    try:
        for items in header:
            try:
                if items.get_text().rstrip() != '':
                    list_header.append(items.get_text().rstrip())
            except:
                continue

        # Find the data rows in the table
        HTML_data = soup.find("table", id="table1").find_all("tr")[1:]
        for element in HTML_data:
            sub_data = []
            for sub_element in element:
                try:
                    if sub_element.get_text().rstrip() != '':
                        sub_data.append(sub_element.get_text().rstrip())
                except:
                    continue
            data.append(sub_data)
    except:
        logging.error("Failed to parse table")
        raise

    return (list_header, data)

def init_dataframe(list_header, data):
    # Store the data into a Pandas DataFrame
    constituencyDataFrame = pd.DataFrame(data=data, columns=list_header)

    # Add a column for the election result
    constituencyDataFrame['Winner'] = "No"
    constituencyDataFrame.loc[constituencyDataFrame['Candidate'].str.contains("Winner", case=False), 'Winner'] = "Yes"
    constituencyDataFrame['Candidate'] = constituencyDataFrame['Candidate'].str.strip("Winner").str.rstrip()

    # Convert the assets and liabilities columns to numbers
    pattern = r' \~.*$'
    try:
        constituencyDataFrame['Total Assets'] = constituencyDataFrame['Total Assets'].replace('Nil', '0')
        constituencyDataFrame['Liabilities'] = constituencyDataFrame['Liabilities'].replace('Nil', '0')
        constituencyDataFrame['Total Assets'] = constituencyDataFrame['Total Assets'].replace(pattern, '', regex=True).str.lstrip("Rs").str.replace(',', '').astype(int)
        constituencyDataFrame['Liabilities'] = constituencyDataFrame['Liabilities'].replace(pattern, '', regex=True).str.lstrip("Rs").str.replace(',', '').astype(int)
    except:
        logging.error("Failed to parse table")
        logging.error(constituencyDataFrame)
        raise

    # Replace empty strings with NaN
    constituencyDataFrame.replace("", np.nan, inplace=True)
    # Drop columns with all NaN values
    constituencyDataFrame.dropna(how='all', axis=1, inplace=True)

    return constituencyDataFrame

def election_details_dataframe(constituencyDataFrame, soup):
    # Add columns for election details
    div = soup.find('div', class_='w3-light-gray')
    try:
        pattern = r'\d+'
        div = div.text

        election = div.split("→")[1].lstrip().rstrip()
        year = re.findall(pattern, election)[0].lstrip().rstrip()
        house = election.strip(year).replace("Election", "").lstrip().rstrip()

        if "Lok Sabha" in div or "Loksabha" in div:
            state = div.split("→")[2].lstrip().rstrip()
            district = ""
        else:
            state = house
            district = div.split("→")[2].lstrip().rstrip()

        constituency = div.split("→")[3].lstrip().rstrip()
        if ":" in constituency:
            comment = constituency.split(":")[1].lstrip().rstrip()
            constituency = constituency.split(":")[0].lstrip().rstrip()
        else:
            comment = "No Comment"

        if house == "Loksabha":
            house = "Lok Sabha"
        if house == "Himacha":
            house = "Himachal Pradesh"
    except:
        logging.error("Failed to parse div")
        logging.error(div)
        raise

    constituencyDataFrame['Constituency'] = constituency.upper()
    constituencyDataFrame['State'] = state.upper()
    constituencyDataFrame['District'] = district.upper()
    constituencyDataFrame['Year'] = year
    constituencyDataFrame['House'] = house
    constituencyDataFrame['Comment'] = comment

    return constituencyDataFrame

def merge_data_frame(dataFrame, constituencyDataFrame):
    try:
        # Aggregate every constituency DataFrame into an dataFrame
        constituencyDataFrame.reset_index(inplace=True, drop=True)
        dataFrame.reset_index(inplace=True, drop=True)
        dataFrame = pd.concat([dataFrame, constituencyDataFrame], ignore_index = True)
    except:
        logging.error("Failed to concatenate: {}".format(file_path))
        logging.error(constituencyDataFrame)
        raise
    
    return dataFrame

def log_data_frame(dataFrame):
    try:
        logging.info("Candidates: {}".format(len(dataFrame)))
        logging.info("Constituencies: {}".format(len(dataFrame[['House', 'Year', 'Constituency']].drop_duplicates())))
        logging.info("Elections: {}".format(len(dataFrame[['House', 'Year']].drop_duplicates())))
        logging.info("List: {}".format(', '.join(dataFrame['House'].drop_duplicates())))
    except:
        pass

def save_data_frame(legislature, dataFrame):
    # Create the directory
    directory = "csv/{}".format(legislature)
    os.makedirs(directory, exist_ok=True)
    # Sort the dataFrame by year, state, district and constituency
    dataFrame = dataFrame.sort_values(by=['Year', 'State', 'District', 'Constituency'], ascending=[False, True, True, True])
    # Save the dataFrame
    dataFrame.to_csv('{}/Candidates.csv'.format(directory), index=False, sep=";", quoting=csv.QUOTE_ALL)

def build_date_frame(legislature):

    zip_file_path = "raw/{}.zip".format(legislature)
    dataFrame = pd.DataFrame()

    # Open the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Iterate over the files in the zip file
        for file_name in zip_ref.namelist():
            # Read the content of the file
            file_content = zip_ref.read(file_name)

            try:
                # Read the file as HTML
                soup = read_html(file_content)
                # Parse the HTML to extract table data
                (list_header, data) = parse_html(soup)
                # Initialize a dataframe with table data
                constituencyDataFrame = init_dataframe(list_header, data)
                # Include election details in the dataframe
                constituencyDataFrame = election_details_dataframe(constituencyDataFrame, soup)
                # Merge constituency dataframe with combined data frame
                dataFrame = merge_data_frame(dataFrame, constituencyDataFrame)
            except:
                logging.info("Skipping {}".format(file_name))

    try:
        # Log the data frame statistics
        log_data_frame(dataFrame)
    except:
        pass

    return dataFrame

def flatten_lok_sabha():
    legislature = "Lok Sabha"
    dataFrame = build_date_frame(legislature)
    save_data_frame(legislature, dataFrame)

def flatten_state_assemblies():
    baseLegislature = "State Assemblies"
    # Iterate over the files in the directory
    for filename in os.listdir("./raw/{}".format(baseLegislature)):
        # Check if the file has a .zip extension
        if filename.endswith('.zip'):
            # Construct the full legislature path
            legislature = os.path.join(baseLegislature, filename.replace(".zip", ""))
            dataFrame = build_date_frame(legislature)
            save_data_frame(legislature, dataFrame)

def merge_csvs_in_directory(directory):
	# Define the directory path where you want to start the search for CSV files
    directory_path = './csv/{}'.format(directory)
	# Use glob.glob with the ** pattern to recursively find all CSV files
    csv_files = glob.glob(os.path.join(directory_path, '*/*.csv'), recursive=True)
	# Initialize an empty list to hold the dataframes
    dataframes = []
	# Read each CSV file into a pandas DataFrame and append it to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=";", quoting=csv.QUOTE_ALL)
        dataframes.append(df)
	# Concatenate all DataFrames into one
    merged_dataframe = pd.concat(dataframes, ignore_index=True)
	# Write the merged DataFrame to a new CSV file
    save_data_frame(directory, merged_dataframe)

def merge_csvs():
    merge_csvs_in_directory("./State Assemblies")
    merge_csvs_in_directory("")

def flatten():
    flatten_lok_sabha()
    flatten_state_assemblies()
    merge_csvs()

if __name__ == "__main__":
    flatten()
