"""Training Clean Data with 3 functions load_data, clean_data, and save_data"""

## Assignmnents 2

import argparse
import pathlib
from pathlib import Path
import pandas as pd
from pandas import DataFrame

def load_data ():
    """ function to load data and return the data to clean, dataclean"""
    file_path = Path(__file__).parent / "data"/"eu_life_expectancy_raw.tsv"
    with open(file_path, 'r', encoding="utf-8") as file:
        dataclean= pd.read_csv(file, sep='\t', engine='python')
        return dataclean

def clean_data(region:str, dataclean:DataFrame):
    """ function clean data, receives dataclean"""
    # create new columns
    dataclean = dataclean.assign(unit=dataclean["unit,sex,age,geo\\time"].str.split(',').str[0],
                    sex=dataclean["unit,sex,age,geo\\time"].str.split(',').str[1],
                    age=dataclean["unit,sex,age,geo\\time"].str.split(',').str[2],
                    geo=dataclean["unit,sex,age,geo\\time"].str.split(',').str[3])

    # rename column geo to region
    dataclean = dataclean.rename(columns={"geo":"region"})

    # create array year
    column_year = dataclean.columns[
        ~dataclean.columns.isin(['unit,sex,age,geo\\time','unit','sex','age','region'])]

    # unpivots the date to long format,
    # following columns: unit, sex, age, region, year, value
    dataclean = dataclean.melt(id_vars=['unit','sex','age','region'],
    value_vars= column_year,
    var_name = 'year',
    value_name = 'value')

    # extract only the values that match the pattern of digits and decimal points, year is an int
    dataclean.value=dataclean.value.str.extract(r"(\d+\.\d+)")
    dataclean['year'] = dataclean['year'].astype(int)

    # remove the NaN and trasform
    #dataclean = dataclean.dropna()
    dataclean=dataclean[(dataclean.value.str.strip())!="NaN"]
    dataclean=dataclean[(dataclean.value.notnull())]
    dataclean['value'] = pd.to_numeric(dataclean['value'], errors='coerce')

    # value float
    dataclean['value'] = dataclean['value'].astype(float)

    # select region
    #dataclean = dataclean.query(f'region == "{region}"')
    cleaned_data = dataclean.dropna()
    #data = dataclean.query(f'region == "{region}"')
    data = cleaned_data[cleaned_data['region'] == region]
    return data

def save_data(datasave: DataFrame):
    """ function save data"""
# define a path and write to csv
    out_path = pathlib.Path(__file__).parent / 'data/pt_life_expectancy.csv'
 
#write to csv
    datasave.to_csv(out_path, index=False)
    data = load_data()
    cleaned_data = clean_data(data)
    save_data(cleaned_data)

def main(region: str):


    if __name__ == "__main__": # pragma: no cover
        parser = argparse.ArgumentParser()
        parser.add_argument('-region',"--region",type=str,
        help="region is a code to use on clean data",default='PT',required=False)
    args = parser.parse_args()
