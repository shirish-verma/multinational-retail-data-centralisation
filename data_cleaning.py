import calendar
import numpy as np
import pandas as pd
from datetime import datetime

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
        # optimize column dtypes
        card_df['card_provider'] = card_df['card_provider'].astype('category')
        return card_df