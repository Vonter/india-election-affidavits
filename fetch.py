import os
import requests
import zipfile

from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import quote

def fetch_constituencies(constituencies, election, state, raw_dir):
    for constituency in constituencies:
        # Create directory for the constituency
        constituency_dir = os.path.join(raw_dir, state, election, constituency)
        os.makedirs(constituency_dir, exist_ok=True)

        # Construct and encode the URL for the constituency
        constituency_base_url = "https://myneta.info/{election}/index.php?action=show_candidates&constituency_id={constituency}"
        encoded_constituency_url = constituency_base_url.format(election=quote(election), constituency=quote(constituency))

        # Check if the index.html file exists for the constituency, if not download it
        constituency_index_file = os.path.join(constituency_dir, "index.html")
        if not os.path.exists(constituency_index_file):
            print(encoded_constituency_url)
            response = requests.get(encoded_constituency_url)
            with open(constituency_index_file, 'wb') as f:
                f.write(response.content)
            sleep(5)

def fetch_elections(elections, state, raw_dir):
    for election in elections:
        # Create directory for the election
        election_dir = os.path.join(raw_dir, state, election)
        os.makedirs(election_dir, exist_ok=True)

        # Construct and encode the URL for the election
        election_base_url = "https://myneta.info/{election}/"
        encoded_election_url = election_base_url.format(election=quote(election))

        # Check if the index.html file exists for the election, if not download it
        election_index_file = os.path.join(election_dir, "index.html")
        if not os.path.exists(election_index_file):
            print(encoded_election_url)
            response = requests.get(encoded_election_url)
            with open(election_index_file, 'wb') as f:
                f.write(response.content)
            sleep(5)

        # Parse the HTML to extract the constituencies
        with open(election_index_file, 'r') as f:
            html_content = f.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all(class_="w3-padding-small")
        hrefs = [link.get('href') for link in links if link.get('href') is not None]
        constituencies = sorted(list(set([href.split("=")[2] for href in hrefs if "show_candidates" in href])))

        fetch_constituencies(constituencies, election, state, raw_dir)

def fetch_states(states, raw_dir):
    for state in states:
        # Create directory for the state
        base_dir = os.path.join(raw_dir, state)
        os.makedirs(base_dir, exist_ok=True)

        # Encode the state name for the URL
        state_base_url = "https://myneta.info/state_assembly.php?state={state}"
        url = state_base_url.format(state=quote(state))

        # Check if the index.html file exists, if not download it
        index_file = os.path.join(base_dir, "index.html")
        if not os.path.exists(index_file):
            print(url)
            response = requests.get(url)
            with open(index_file, 'wb') as f:
                f.write(response.content)
            sleep(5)

        # Parse the HTML to extract the elections
        with open(index_file, 'r') as f:
            html_content = f.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all(class_="w3-block")
        hrefs = [div.get('href') for div in divs if div.get('href') is not None]
        elections = sorted(list(set([href.split('/')[1] for href in hrefs])))

        fetch_elections(elections, state, raw_dir)

        # Create a new zip file
        state_dir = os.path.join(raw_dir, state)
        with zipfile.ZipFile(os.path.join(raw_dir, "{}.zip".format(state)), 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the directory structure of the folder
            for root, dirs, files in os.walk(state_dir):
                # Add each file to the zip file
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, state_dir))

def fetch_lok_sabha(html_content):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    divs = soup.find(id="ls").find_next('div').find_all(class_="w3-padding-small")
    hrefs = [div.get('href') for div in divs if div.get('href') is not None]
    # include lsdiv in separate sibling div
    sibling_divs = soup.find(id="ls").find_next_siblings('div')[1].find_all(class_="w3-padding-small")
    sibling_hrefs = [sibling_div.get('href') for sibling_div in sibling_divs if sibling_div.get('href') is not None]

    hrefs = hrefs + [sibling_hrefs[0]]
    elections = sorted(list(set([href.split('/')[3] for href in hrefs])))
    raw_dir = "raw/Lok Sabha"

    fetch_elections(elections, "", raw_dir)

    # Create a new zip file
    with zipfile.ZipFile(os.path.join("raw", "Lok Sabha.zip"), 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the directory structure of the folder
        for root, dirs, files in os.walk(raw_dir):
            # Add each file to the zip file
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, raw_dir))

def fetch_state_assemblies(html_content):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    divs = soup.find(id="sa").find_next('div').find_all(class_="w3-padding-small")
    hrefs = [div.get('href') for div in divs if div.get('href') is not None]
    states = sorted(list(set([href.split('=')[1] for href in hrefs])))
    raw_dir = "raw/State Assemblies"

    fetch_states(states, raw_dir)

def fetch():
    # Directory to save the HTML files
    raw_dir = "raw"

    # Base URL
    base_url = "https://myneta.info/"

    # Check if the index.html file exists, if not download it
    index_file = os.path.join(raw_dir, "index.html")
    if not os.path.exists(index_file):
        print(base_url)
        response = requests.get(base_url)
        with open(index_file, 'wb') as f:
            f.write(response.content)
        sleep(5)

    # Parse the HTML to extract the elections
    with open(index_file, 'r') as f:
        html_content = f.read()

    fetch_lok_sabha(html_content)
    fetch_state_assemblies(html_content)

if __name__ == "__main__":
    fetch()
