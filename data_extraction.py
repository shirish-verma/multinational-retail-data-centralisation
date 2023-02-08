import pandas as pd
from database_utils import DatabaseConnector

class DataExtractor():
    def read_rds_table():
        rds_instance = DatabaseConnector()
        rds_tables = rds_instance.list_db_tables()    
        users_df = pd.read_sql_table(rds_tables[rds_tables.index('legacy_users')], rds_instance.init_db_engine()).set_index('index')
        return users_df

