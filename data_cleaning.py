import calendar
import numpy as np
import pandas as pd
from datetime import datetime

class DataCleaning():
    def clean_user_data(user_df):
        # remove NULL rows
        user_df.replace('NULL', np.nan, inplace=True)
        user_df.dropna(how='all', inplace=True)
        # convert date columns
        user_df['date_of_birth'] = pd.to_datetime(user_df['date_of_birth'], errors='coerce')
        user_df['join_date'] = pd.to_datetime(user_df['join_date'], errors='coerce')
        # drop rows with all incorrect values and reset index
        user_df = user_df.loc[user_df['date_of_birth'].notna()]
        user_df = user_df.reset_index(drop=True)
        # replace incorrectly typed email and country code values 
        user_df['email_address'] = user_df['email_address'].replace({'@@' : '@'}, regex=True)
        user_df['country_code'] = user_df['country_code'].replace({'GGB' : 'GB'}, regex=True)
        # optimize column dtypes
        user_df['country'] = user_df['country'].astype('category')
        user_df['country_code'] = user_df['country_code'].astype('category')
        return user_df

    def clean_card_data(card_df):
        # convert date columns
        card_df['date_payment_confirmed'] = pd.to_datetime(card_df['date_payment_confirmed'], errors='coerce')
        # drop rows with all incorrect values and reset index
        card_df = card_df.loc[card_df['date_payment_confirmed'].notna()]
        card_df = card_df.reset_index()
        card_df.set_index('index', inplace=True)
        # convert expiry date to datetime and also set it to last day of month
        card_df['expiry_date'] = pd.to_datetime(card_df['expiry_date'], format="%m/%y")
        card_df['expiry_date'] = card_df['expiry_date'].apply(lambda x : datetime(x.year, x.month, (calendar.monthrange(x.year, x.month)[1])))
        # convert card number to numberic by first correcting values with typos
        card_df['card_number'] = card_df['card_number'].replace({'\?' : ''}, regex=True)
        card_df['card_number'] = pd.to_numeric(card_df['card_number'])
        # optimize column dtypes
        card_df['card_provider'] = card_df['card_provider'].astype('category')
        return card_df

    def clean_store_data(stores_df):
        # remove N/A and NULL values
        stores_df.replace(['NULL', 'N/A'], None, inplace=True)
        # convert date columns
        stores_df['opening_date'] = pd.to_datetime(stores_df['opening_date'], errors='coerce')
        # drop rows with all incorrect values and reset index
        stores_df = stores_df.loc[stores_df['opening_date'].notna()]
        stores_df = stores_df.reset_index(drop=True)
        # drop duplicate column
        stores_df.drop(columns='lat', inplace=True)
        # clean errorneous data
        stores_df['staff_numbers'] = stores_df['staff_numbers'].str.replace('[A-Z_a-z\W]', '', regex=True)
        stores_df['continent'] = stores_df['continent'].str.replace('eeEurope' , 'Europe').replace('eeAmerica' , 'America')
        # convert numeric columns
        stores_df['staff_numbers'] = pd.to_numeric(stores_df['staff_numbers'])
        stores_df['longitude'] = pd.to_numeric(stores_df['longitude'])
        stores_df['latitude'] = pd.to_numeric(stores_df['latitude'])
        # optimize column dtypes
        stores_df['locality'] = stores_df['locality'].astype('category')
        stores_df['store_type'] = stores_df['store_type'].astype('category')
        stores_df['country_code'] = stores_df['country_code'].astype('category')
        stores_df['continent'] = stores_df['continent'].astype('category')
        stores_df['store_code'] = stores_df['store_code'].astype('string')
        return stores_df

