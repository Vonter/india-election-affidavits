import csv
import numpy as np
import os
import pandas as pd
import re
import sys

from bs4 import BeautifulSoup

def flatten_data(folder, elections):

    folderDataFrame = pd.DataFrame()

    # Iterate over every election
    for election in elections:

        electionDataFrame = pd.DataFrame()

        # Specify the directory containing HTML files
        html_dir = "./raw/{}/{}".format(folder, election)

        # Iterate over the files in the directory
        for file_name in os.listdir(html_dir):
            # Check if the file is an HTML file
            if file_name.endswith('.html'):

                try:
                    # Construct the file path
                    file_path = os.path.join(html_dir, file_name)
                    
                    # Open and read the HTML file
                    with open(file_path, 'r') as file:
                        content = file.read()
                    
                    # Parse the HTML file
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Now you can perform operations on the parsed HTML
                    # For example, print the title tag
                    title_tag = soup.title
                except:
                    print("ERROR: Failed to parse {}".format(file_path))
                    continue

                if not "Page Not Found" in title_tag.text:
                    print(title_tag)

                    # Create an empty list to store the table data
                    data = []

                    # Create an empty list to store the table headers
                    list_header = []

                    try:
                        # Find the table and extract the headers
                        header = soup.find("table", id="table1").find("tr")
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
                        print("ERROR: Failed to parse {}".format(file_path))
                        continue

                    # Store the data into a Pandas DataFrame
                    dataFrame = pd.DataFrame(data=data, columns=list_header)

                    # Add a column for the election result
                    dataFrame['Winner'] = "No"
                    dataFrame.loc[dataFrame['Candidate'].str.contains("Winner", case=False), 'Winner'] = "Yes"
                    dataFrame['Candidate'] = dataFrame['Candidate'].str.strip("Winner").str.rstrip()

                    # Convert the assets and liabilities columns to numbers
                    pattern = r' \~.*$'
                    try:
                        dataFrame['Total Assets'] = dataFrame['Total Assets'].replace('Nil', '0')
                        dataFrame['Liabilities'] = dataFrame['Liabilities'].replace('Nil', '0')
                        dataFrame['Total Assets'] = dataFrame['Total Assets'].replace(pattern, '', regex=True).str.lstrip("Rs").str.replace(',', '').astype(int)
                        dataFrame['Liabilities'] = dataFrame['Liabilities'].replace(pattern, '', regex=True).str.lstrip("Rs").str.replace(',', '').astype(int)
                    except:
                        print(dataFrame)

                    # Add columns for election details
                    div = soup.find('div', class_='w3-light-gray')
                    try:
                        div = div.text
                        house = div.split("→")[1]
                        state = div.split("→")[2].lstrip().rstrip()
                        constituency = div.split("→")[3].lstrip().rstrip()
                        pattern = r'\d+'
                        year = re.findall(pattern, house)[0].lstrip().rstrip()
                        house = house.split(year)[0].lstrip().rstrip()

                        if ":" in constituency:
                            comment = constituency.split(":")[1].lstrip().rstrip()
                            constituency = constituency.split(":")[0].lstrip().rstrip()
                        else:
                            comment = "No Comment"
                    except:
                        print(div)
                    dataFrame['Constituency'] = constituency
                    dataFrame['State'] = state
                    dataFrame['Year'] = year
                    dataFrame['House'] = house
                    dataFrame['Comment'] = comment

                    # Replace empty strings with NaN
                    dataFrame.replace("", np.nan, inplace=True)
                    # Drop columns with all NaN values
                    dataFrame.dropna(how='all', axis=1, inplace=True)

                    # Save the DataFrame to a CSV file
                    os.makedirs("csv/{}/{}/{}".format(house, year, state), exist_ok=True)
                    dataFrame.to_csv("csv/{}/{}/{}/{}.csv".format(house, year, state, constituency), index=False, sep=";", quoting=csv.QUOTE_ALL)

                    # Aggregate every constituency DataFrame into an electionDataFrame
                    try:
                        dataFrame.reset_index(inplace=True, drop=True)
                        electionDataFrame.reset_index(inplace=True, drop=True)
                        electionDataFrame = pd.concat([electionDataFrame, dataFrame], ignore_index = True)
                    except:
                        print(dataFrame)
                        raise

        # Save the electionDataFrame
        electionDataFrame.to_csv('csv/{}/{}/Election.csv'.format(house, year), index=False, sep=";", quoting=csv.QUOTE_ALL)

        # Aggregate every electionDataFrame into a folderDataFrame
        try:
            electionDataFrame.reset_index(inplace=True, drop=True)
            folderDataFrame.reset_index(inplace=True, drop=True)
            folderDataFrame = pd.concat([folderDataFrame, electionDataFrame], ignore_index = True)
        except:
            print(electionDataFrame)
            raise

    # Save the folderDataFrame
    folderDataFrame.to_csv('csv/{}/Candidates.csv'.format(house, year), index=False, sep=";", quoting=csv.QUOTE_ALL)

flatten_data("Lok Sabha", ["2019", "2014", "2009", "2004"])
