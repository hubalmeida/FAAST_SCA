
## Assignmnents 1 - cleaning.py

import pandas as pd
def clean_data():
    

    # read table
    data = pd.read_csv('/nfs/workstation/wb_mkte/scalmeida/FAAST_SCA/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv',sep='\t',engine ='python')

    # data clean ':'
    #data= data.apply(lambda x: x.str.strip().replace(':', "NaN"))
    data.value=data.value.str.extract(r"(\d+\.\d+)")
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

    # remove the NaN and trasform 
    data = data.dropna()
    # data=data[(data.value.str.strip())!="NaN"]
    #data=data[(data.value.notnull())]
    data['value'] = pd.to_numeric(data['value'], errors='coerce')

    # value float
    data['value'] = data['value'].astype(float)

    # select region
    data = data.query('region == "PT"')

    data.to_csv('/nfs/workstation/wb_mkte/scalmeida/FAAST_SCA/assignments/life_expectancy/data/pt_life_expectancy.csv', index=False)
    print (data)