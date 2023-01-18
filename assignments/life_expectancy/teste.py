
import pandas as pd
import os

file_path = '/nfs/workstation/wb_mkte/scalmeida/FAAST_SCA/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv'

with open(file_path, 'r') as file:
    data = pd.read_csv(file, sep='\t', engine='python', na_values=':', keep_default_na=False, usecols =['unit,sex,age,geo\\time',*range(1961,2019)], skiprows = lambda i: i in [0,1])

# create new column
data = data.assign(unit=data["unit,sex,age,geo\\time"].str.split(',').str[0],
               sex=data["unit,sex,age,geo\\time"].str.split(',').str[1],
               age=data["unit,sex,age,geo\\time"].str.split(',').str[2],
               geo=data["unit,sex,age,geo\\time"].str.split(',').str[3])

# rename column geo to region
data = data.rename(columns={"geo":"region"})

# create array year
column_year = data.columns[~data.columns.isin(['unit,sex,age,geo\\time','unit','sex','age','region'])]

#Unpivots the date to long format, so that we have the following columns: unit, sex, age, region, year, value
unpivoted_df = data = data.melt(id_vars=['unit','sex','age','region'],
value_vars= column_year,
var_name = 'year',
value_name = 'value')

# year is an int 
data['year'] = data['year'].astype(int)

# remove the NaN
data=data[(data.value.notnull())]
data['value'] = pd.to_numeric(data['value'], errors='coerce')

output_path = os.path.join('/nfs/workstation/wb_mkte/scalmeida/FAAST_SCA/assignments/life_expectancy/data/', 'pt_life_expectancy.csv')

data.to_csv(output_path, index=False)
