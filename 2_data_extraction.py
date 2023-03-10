from awscli.customizations.s3.utils import split_s3_bucket_key
from database_utils import DatabaseConnector
import boto3
import pandas as pd
import requests
import tabula

api_creds = {'x-api-key' : 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

class DataExtractor():
    def read_rds_table(engine, table_name):
        users_df = pd.read_sql_table(table_name, engine).set_index('index')
        return users_df 
      
    def retrieve_pdf_data(pdf_link):
        list_of_dfs = tabula.read_pdf(pdf_link, pages='all')
        dataframe = pd.concat(list_of_dfs)
        return dataframe

    def list_number_of_stores(url):
        response = requests.get(url, headers=api_creds)
        number_of_stores = response.json().get('number_stores')
        return number_of_stores

    def retrieve_stores_data(number_of_stores, url):
        mod_url = url.split('{')[0]
        stores_dict = [requests.get(f'{mod_url}{x}', headers=api_creds).json() for x in range(0,number_of_stores)]
        stores_df = pd.DataFrame(stores_dict)
        stores_df.set_index('index', inplace=True)
        return stores_df

    def extract_from_s3(s3_uri):
        bucket_name, key_name = split_s3_bucket_key(s3_uri)
        s3_client = boto3.client('s3')
        s3_client.download_file(Bucket=bucket_name, Key=key_name, Filename='products.csv')
        products_df = pd.read_csv('products.csv', index_col=0)
        return products_df

    def retrieve_events_data(url):
        response = requests.get(url)
        events_df = pd.DataFrame(response.json())
        return events_df

