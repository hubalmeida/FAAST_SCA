import argparse
from pathlib import Path
import pandas as pd
import pytest
import unittest
from unittest.mock import patch, mock_open


@pytest.fixture
def load_data():
    def _load_data():
        file_path = Path(__file__).parent / "data/eu_life_expectancy_raw.tsv"
        return pd.read_csv(file_path, sep='\t', encoding="utf-8")
    return _load_data

def test_clean_data(load_data):
    from life_expectancy.data_cleaning import clean_data
    
    # Mock external dependencies
    with patch('builtins.open', mock_open(read_data='unit,sex,age,geo\\time\t2000\t2001\t2002\t2003\nNR\tF\tTOTAL\tPT\t81.3\t81.5\t81.9\t81.9\n')):
        data = clean_data("path/to/mock/file.tsv", "PT")
        
        expected_data = pd.DataFrame({
            'unit': ['NR', 'NR', 'NR', 'NR'],
            'sex': ['F', 'F', 'F', 'F'],
            'age': ['TOTAL', 'TOTAL', 'TOTAL', 'TOTAL'],
            'region': ['PT', 'PT', 'PT', 'PT'],
            'year': [2000, 2001, 2002, 2003],
            'value': [81.3, 81.5, 81.9, 81.9]
        })

    pd.testing.assert_frame_equal(data, expected_data)


if __name__ == '__main__':
    unittest.main()