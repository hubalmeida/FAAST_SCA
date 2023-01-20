"""Training Clean Data"""
## Assignmnents 1 - cleaning.py

import argparse
import pandas as pd
from pathlib import Path

def clean_data(region:str) -> None:
    """ The function clean data receives data from the original.tsv file and cleans the data.
inputs: 
data_to_clean > pandas Dataframe with diferentes types of countries and types of features; 
region_code> string - select the country we want to use.
for this exercice e wanted use PT  (for Portugal), 
But we can select others countries"""
# define a path
    file_path = Path(__file__).parent / "data"/"eu_life_expectancy_raw.tsv"
# read table
    with open(file_path, 'r', encoding="utf-8") as file:
        data = pd.read_csv(file, sep='\t', engine='python')

    # create new columns
    data = data.assign(unit=data["unit,sex,age,geo\\time"].str.split(',').str[0],
                    sex=data["unit,sex,age,geo\\time"].str.split(',').str[1],
                    age=data["unit,sex,age,geo\\time"].str.split(',').str[2],
                    geo=data["unit,sex,age,geo\\time"].str.split(',').str[3])

    # rename column geo to region
    data = data.rename(columns={"geo":"region"})

    # create array year
    column_year = data.columns[
        ~data.columns.isin(['unit,sex,age,geo\\time','unit','sex','age','region'])]

    # unpivots the date to long format,
    # following columns: unit, sex, age, region, year, value
    data = data.melt(id_vars=['unit','sex','age','region'],
    value_vars= column_year,
    var_name = 'year',
    value_name = 'value')

    # extract only the values that match the pattern of digits and decimal points, year is an int
    data.value=data.value.str.extract(r"(\d+\.\d+)")
    data['year'] = data['year'].astype(int)

    # remove the NaN and trasform
    data = data.dropna()
    data=data[(data.value.str.strip())!="NaN"]
    data=data[(data.value.notnull())]
    data['value'] = pd.to_numeric(data['value'], errors='coerce')

    # value float
    data['value'] = data['value'].astype(float)

    # select region
    data = data.query(f'region == "{region}"')
    
    # define a path and write to csv
    write_path = pathlib.Path(__file__).parent / 'data/pt_life_expectancy.csv'
    #write to csv
    data.to_csv(write_path, index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--region",
    help="region is a code to use on clean data",
    default="PT",required=False)
    args = parser.parse_args()

    clean_data(args.region)
