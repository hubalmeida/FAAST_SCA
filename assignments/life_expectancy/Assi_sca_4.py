
from enum import Enum
import json
import zipfile

class Country(Enum):
    AUSTRIA = "Austria"
    BELGIUM = "Belgium"
    BULGARIA = "Bulgaria"
    CROATIA = "Croatia"
    CYPRUS = "Cyprus"
    CZECHIA = "Czechia"
    DENMARK = "Denmark"
    ESTONIA = "Estonia"
    FINLAND = "Finland"
    FRANCE = "France"
    GERMANY = "Germany"
    GREECE = "Greece"
    HUNGARY = "Hungary"
    IRELAND = "Ireland"
    ITALY = "Italy"
    LATVIA = "Latvia"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MALTA = "Malta"
    NETHERLANDS = "Netherlands"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    ROMANIA = "Romania"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SPAIN = "Spain"
    SWEDEN = "Sweden"
    
    @classmethod
    def actual_countries(cls):
        return [c.value for c in cls if c.value not in ["EU27_2020", "EU28", "EU27", "EA19", "EFTA", "EU", "Euro area (EA11-2000, EA12-2006, EA13-2007, EA16-2010, EA17-2013, EA18-2014, EA19)"]]
    
class DataFormatStrategy:
    def load_data(self, filename: str, country: Country) -> dict:
        pass

class JSONFormatStrategy(DataFormatStrategy):
    def load_data(self, filename: str, country: Country) -> dict:
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filename) as z:
                with z.open(z.namelist()[0]) as f:
                    data = json.load(f)
        else:
            with open(filename) as f:
                data = json.load(f)
        return data[country.value]

class CSVFormatStrategy(DataFormatStrategy):
    def load_data(self, filename: str, country: Country) -> dict:
        # Implement CSV loading logic here
        pass

class DataLoader:
    def __init__(self, format_strategy: DataFormatStrategy):
        self.format_strategy = format_strategy

    def load_data(self, filename: str, country: Country) -> dict:
        data = self.format_strategy.load_data(filename, country)
        return data

    def print_data(self, filename: str, country: Country) -> None:
        data = self.load_data(filename, country)
        print(data)

# Test
def test_actual_countries():
    actual_countries = Country.actual_countries()
    assert "Greece" in actual_countries
    assert "EU27_2020" not in actual_countries
    assert "EFTA" not in actual_countries

def test_json_format_strategy():
    json_loader = DataLoader(JSONFormatStrategy())
    data = json_loader.load_data('eurostat_life_expect.zip', Country.GREECE)
    assert isinstance(data, dict)
    assert "2019" in data
    assert "2020" in data

test_actual_countries()
test_json_format_strategy()