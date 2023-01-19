"""Training Clean Data"""
## Assignmnents 1 - cleaning.py

import argparse
import pandas as pd

def clean_data(region:str) -> None:
    """ Clean data  """
# read table

    file_path = './life_expectancy/data/eu_life_expectancy_raw.tsv'
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

    data.to_csv('./life_expectancy/data/pt_life_expectancy.csv', index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--region",
    help="region is a code to use on clean data",
    default="PT",required=False)
    args = parser.parse_args()

    clean_data(args.region)
