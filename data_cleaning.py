import numpy as np
import pandas as pd

class DataCleaning():
    def clean_user_data(df):
        # remove NULL rows
        df.replace('NULL', np.nan, inplace=True)
        df.dropna(how='all', inplace=True)
        # convert date columns
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
        # drop rows with all incorrect values and reset index
        df = df.loc[df['date_of_birth'].notna()]
        df = df.reset_index()
        df.set_index('index', inplace=True)
        # replace incorrectly typed email and country code values 
        df['email_address'] = df['email_address'].replace({'@@' : '@'}, regex=True)
        df['country_code'] = df['country_code'].replace({'GGB' : 'GB'}, regex=True)
        # optimize column dtypes
        df['country'] = df['country'].astype('category')
        df['country_code'] = df['country_code'].astype('category')
        return df

