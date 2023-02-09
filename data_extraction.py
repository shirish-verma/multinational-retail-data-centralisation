from database_utils import DatabaseConnector
import pandas as pd
import tabula

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

