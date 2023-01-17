import pandas as pd
import string
from yaml import safe_load

def conv_to_df(file_path: str):
    with open(file_path, 'r') as file:
        df = pd.json_normalize(safe_load(file))
    return df

sf_sal = pd.read_csv('https://aicore-files.s3.amazonaws.com/Foundations/Data_Formats/Salaries.csv')

alphabet = string.ascii_uppercase
index_list = []
for first in alphabet:
    for second in alphabet:
            index_list.append(first + second)

sf_sal.set_index('Id', inplace=True)
sf_sal.to_csv('data.csv')

# print(sf_sal.describe(include='all'))

# sf_sal['Surname'] = sf_sal['EmployeeName'].apply(lambda x : x.split()[1])
# print(sf_sal.tail())

# sf_sal['isStartA'] = sf_sal['EmployeeName'].apply(lambda x : True if x.split()[1][0] == 'A' else False)
# print(sf_sal.tail())
# print(sf_sal['isStartA'].sum())

sf_sal['isPolice'] = sf_sal['JobTitle'].apply(lambda x : True if "POLICE DEPARTMENT" in x else False)
count_police = sf_sal['isPolice'].sum()

sf_sal['isFire'] = sf_sal['JobTitle'].apply(lambda x : True if "FIRE DEPARTMENT" in x else False)
count_fire = sf_sal['isFire'].sum()

print(f'The ratio of people in the fire ({count_fire}) over the police ({count_police}) department is: {count_fire} : {count_police}.')

fire_basepay_mean = sf_sal.loc[sf_sal['isFire'] == True, 'BasePay'].mean()
print(f'The mean of base salary of the people in fire department is {fire_basepay_mean}.')

unique_job_titles = sf_sal['JobTitle'].unique()
print(f'There are {len(unique_job_titles)} unique job titles in the salaries.csv database.')

