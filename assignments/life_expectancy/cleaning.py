"""Training Clean Data """

import argparse
import pandas as pd
from pandas import DataFrame
from life_expectancy.load_save import save_data,load_data

def clean_data(dataclean: DataFrame, region: str = "PT"):
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

def main(region: str = "PT")-> DataFrame:
    """defaut is region"""
    dataclean = load_data()
    cleaned_data = clean_data(dataclean,region)
    save_data(cleaned_data)
    return cleaned_data

if __name__ == '__main__': #pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument('-region',"--region",type=str,
    help="region is a code to use on clean data",
    default='PT', required=False)
    args = parser.parse_args()
    main(args.region)
