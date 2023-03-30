"""Training to save data"""

from pathlib import Path
import pandas as pd

def load_data():
    """ function to load data and return the data to clean, dataclean"""
    file_path = Path(__file__).parent / "data/eu_life_expectancy_raw.tsv"
    return pd.read_csv(file_path, sep='\t', encoding="utf-8")

def save_data(datasave):
    """function to save de data clean"""
    out_path = Path(__file__).parent / 'data/pt_life_expectancy.csv'
    datasave.to_csv(out_path, index=False)
