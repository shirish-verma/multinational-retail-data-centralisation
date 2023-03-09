from data_cleaning import DataCleaning
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

host_db_instance = DatabaseConnector("db_creds.yaml")
local_db_instance = DatabaseConnector("local_db_creds.yaml")

raw_user_df = DataExtractor.read_rds_table(host_db_instance.engine, 'legacy_users')
clean_user_df = DataCleaning.clean_user_data(raw_user_df)
local_db_instance.upload_to_db(clean_user_df, 'dim_users')

raw_card_df = DataExtractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
clean_card_df = DataCleaning.clean_card_data(raw_card_df)
local_db_instance.upload_to_db(clean_card_df, 'dim_card_details')

number_of_stores = DataExtractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores')
raw_stores_df = DataExtractor.retrieve_stores_data(number_of_stores, 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}')
clean_stores_df = DataCleaning.clean_store_data(raw_stores_df)
local_db_instance.upload_to_db(clean_stores_df, 'dim_store_details')

raw_products_df = DataExtractor.extract_from_s3('s3://data-handling-public/products.csv')
interim_products_df = DataCleaning.clean_products_data(raw_products_df)
clean_products_df = DataCleaning.convert_product_weights(interim_products_df)
local_db_instance.upload_to_db(clean_products_df, 'dim_products')

raw_orders_df = DataExtractor.read_rds_table(host_db_instance.engine, 'orders_table')
clean_orders_df = DataCleaning.clean_orders_data(raw_orders_df)
local_db_instance.upload_to_db(clean_orders_df, 'orders_table')

raw_events_df = DataExtractor.retrieve_events_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
clean_events_df = DataCleaning.clean_events_data(raw_events_df)
local_db_instance.upload_to_db(clean_events_df, 'dim_date_times')

