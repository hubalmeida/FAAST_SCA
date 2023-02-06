"""Training Clean Data with 3 functions load_data, clean_data, and save_data"""

## Assignmnents 2

import argparse
from pathlib import Path
import pandas as pd
from pandas import DataFrame

def load_data ():
    """ function to load data and return the data to clean, dataclean"""
    file_path = Path(__file__).parent / "data/eu_life_expectancy_raw.tsv"
    return pd.read_csv(file_path, sep='\t', encoding="utf-8")

def clean_data(dataclean: DataFrame, region: str):
    """ function clean data, receives dataclean"""
    # create new columns
    dataclean = dataclean.assign(unit=dataclean["unit,sex,age,geo\\time"].str.split(',').str[0],
                                 sex=dataclean["unit,sex,age,geo\\time"].str.split(',').str[1],
                                 age=dataclean["unit,sex,age,geo\\time"].str.split(',').str[2],
                                 region=dataclean["unit,sex,age,geo\\time"].str.split(',').str[3])
    dataclean = dataclean.rename(columns={"region": "region"})
    dataclean = dataclean.melt(id_vars=['unit','sex','age','region'],
                                value_vars=dataclean.columns[~dataclean.columns.isin(
                                    ['unit,sex,age,geo\\time','unit','sex','age','region'])],
                                var_name='year', value_name='value')
    dataclean.value = dataclean.value.str.extract(r"(\d+\.\d+)")
    dataclean['year'] = dataclean['year'].astype(int)
    dataclean = dataclean[(dataclean.value.str.strip() != "NaN") & (dataclean.value.notnull())]
    dataclean['value'] = pd.to_numeric(dataclean['value'], errors='coerce')
    dataclean['value'] = dataclean['value'].astype(float)
    return dataclean[dataclean['region'] == region].dropna()

def save_data(datasave):
    """function to save de data clean"""
    out_path = Path(__file__).parent / 'data/pt_life_expectancy.csv'
    datasave.to_csv(out_path, index=False)

def main(region:str):
    """defaut is region"""
    dataclean = load_data()
    cleaned_data = clean_data(dataclean,region)
    save_data(cleaned_data)
    print(region)
    input ("press enterto continue")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-region',"--region",type=str,
    help="region is a code to use on clean data",default='PT', required=False)
    args = parser.parse_args()
    main(args.region)
