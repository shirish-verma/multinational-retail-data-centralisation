import tabula
import requests
import pandas as pd
from database_utils import DatabaseConnector

api_creds = {'x-api-key' : 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}

class DataExtractor():    
    def read_rds_table():
        rds_instance = DatabaseConnector()
        rds_tables = rds_instance.list_db_tables()    
        users_df = pd.read_sql_table(rds_tables[rds_tables.index('legacy_users')], rds_instance.init_db_engine()).set_index('index')
        return users_df
    
    def retrieve_pdf_data(pdf_link):
        list_of_dfs = tabula.read_pdf(pdf_link, pages='all')
        dataframe = pd.concat(list_of_dfs)
        return dataframe

    def list_number_of_stores():
        response = requests.get('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', headers=api_creds)
        number_of_stores = response.json().get('number_stores')
        return number_of_stores

    def retrieve_stores_data(number_of_stores):
        stores_dict = [requests.get(f'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{x}', headers=api_creds).json() for x in range(0,number_of_stores)]
        stores_df = pd.DataFrame(stores_dict)
        stores_df.set_index('index', inplace=True)
        return stores_df

