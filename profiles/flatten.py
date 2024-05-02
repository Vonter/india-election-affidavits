import csv
import os
import pandas as pd
from bs4 import BeautifulSoup

def find_html_files(directory):
    """Recursively find all HTML files in a directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def html_to_dataframe(html_file):
    """Extract text from all div elements of a specific class."""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    divs = soup.find_all('div', class_="col-sm-6")
    
    texts = [div.get_text(strip=True) for div in divs]
    return texts

def main(directory):
    column_names = ["State", "Constituency", "Party", "Candidate Name", "Gender", "Age", "Address", "Application Date", "Application Status", "Father/Husband's Name"]
    candidates = pd.DataFrame(columns=column_names)

    for html_file in find_html_files(directory):
        texts = html_to_dataframe(html_file)

        candidate = [texts[13], texts[11], texts[3], texts[7], texts[24], texts[25], texts[23], texts[15], texts[17], texts[19]]
        candidate_row = pd.DataFrame([candidate], columns=column_names)

        candidates = pd.concat([candidates, candidate_row], ignore_index=True)

        print("{} candidates processed...".format(len(candidates)))

    directory = "csv"
    os.makedirs(directory, exist_ok=True)
    candidates.to_csv('csv/Candidates.csv', index=False, sep=";", quoting=csv.QUOTE_ALL)

if __name__ == "__main__":
    directory = 'raw/profiles/'  # Specify the directory containing the HTML files
    main(directory)
