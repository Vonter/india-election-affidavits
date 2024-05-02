# india-election-affidavits

Dataset of candidate affidavits filed during elections. Sourced from [MyNeta](https://myneta.info/), an open data repository platform of [Association for Democratic Reforms (ADR)](https://adrindia.org). Information submitted by candidates in their affidavits are not guaranteed to match reality.

Browse the dataset using the below links:
- [Lok Sabha](https://flatgithub.com/Vonter/india-election-affidavits?filename=csv/Lok%20Sabha/Candidates.csv&stickyColumnName=Candidate)
- [State Assemblies](https://flatgithub.com/Vonter/india-election-affidavits?filename=csv/State%20Assemblies/Candidates.csv&stickyColumnName=Candidate)
- [All Candidates](https://flatgithub.com/Vonter/india-election-affidavits?filename=csv/Candidates.csv&stickyColumnName=Candidate)

More CSV files can be found under the [csv/](csv) folder in this repository.

## Scripts

- [fetch.py](fetch.py): Fetches the raw HTML pages from [MyNeta](https://myneta.info/)
- [flatten.py](flatten.py): Parses the raw HTML pages, and generates the CSV dataset
- [append.py](append.py): Extends the base CSV dataset with additional columns

## Extended

The base CSV dataset has been extended with additional columns in [extended/Candidates.csv](extended/Candidates.csv) - for mapping with other datasets:
- `pc_id` for mapping to [Parliamentary Constituencies Shapefile (2019)](https://github.com/datameet/maps/blob/master/parliamentary-constituencies/india_pc_2019_simplified.geojson)
- `Code` for mapping to [LGD Codes](https://ramseraph.github.io/opendata/lgd/)
- `Status` to indicate if the constituency has been abolished

Thanks to [planemad](https://github.com/Vonter/india-election-affidavits/pull/3) for the mapping columns

## Candidate Profiles

Candidate profiles dataset and related scripts can be found under the [profiles/](profiles/) folder. The dataset includes information shown under the candidate's profile page on the ECI website (name, party name, age, gender, address). `*.sh` scripts fetch data from the ECI website. `flatten.py` parses the fetched HTML pages, and generates the CSV dataset.

Browse the Candidate Profiles dataset using the below links:
- [Parliamentary Elections](https://flatgithub.com/Vonter/india-election-affidavits?filename=profiles/csv/Candidates.csv&stickyColumnName=Candidate%20Name)

## License

This india-election-affidavits dataset is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. 
Users of this data should attribute Association for Democratic Reforms (ADR): https://adrindia.org

You are free:

* **To share**: To copy, distribute and use the database.
* **To create**: To produce works from the database.
* **To adapt**: To modify, transform and build upon the database.

As long as you:

* **Attribute**: You must attribute any public use of the database, or works produced from the database, in the manner specified in the ODbL. For any use or redistribution of the database, or works produced from it, you must make clear to others the license of the database and keep intact any notices on the original database.
* **Share-Alike**: If you publicly use any adapted version of this database, or works produced from an adapted database, you must also offer that adapted database under the ODbL.
* **Keep open**: If you redistribute the database, or an adapted version of it, then you may use technological measures that restrict the work (such as DRM) as long as you also redistribute a version without such measures.

## Generating

Ensure you have `python` installed with the required libraries:

```
# Fetch the data
python fetch.py

# Generate the CSV
python flatten.py

# Include additional columns
python append.py
```

The fetch script sources data from MyNeta (https://myneta.info/)

## TODO

- Local Bodies
- Rajya Sabha
- Election Expenses
- Detailed affidavit information

## Credits

- [MyNeta](https://myneta.info/)
- [Association for Democratic Reforms (ADR)](https://adrindia.org)
