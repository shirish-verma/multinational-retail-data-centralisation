from data_extraction import DataExtractor
from database_utils import DatabaseConnector
from data_cleaning import DataCleaning


user_df = DataExtractor.read_rds_table()
clean_df = DataCleaning.clean_user_data(user_df)
DatabaseConnector.upload_to_db(clean_df, 'dim_users')
