from sqlalchemy import create_engine
from sqlalchemy import inspect
import pandas as pd
import yaml

class DatabaseConnector:
    def __init__(self, creds_filepath):
        self.creds_filepath = creds_filepath
        self.db_creds = self.read_db_creds()
        self.engine = self.init_db_engine()

    def read_db_creds(self):
        with open(self.creds_filepath, mode='r') as stream:
            return yaml.safe_load(stream)

    def init_db_engine(self):
        engine = create_engine(f"{'postgresql'}+{'psycopg2'}://{self.db_creds.get('RDS_USER')}:{self.db_creds.get('RDS_PASSWORD')}@{self.db_creds.get('RDS_HOST')}:{self.db_creds.get('RDS_PORT')}/{self.db_creds.get('RDS_DATABASE')}")
        engine.connect()
        return engine

    def list_db_tables(self):
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def upload_to_db(self, dataframe, table_name):
        dataframe.to_sql(table_name, self.engine, if_exists='replace', index=False)

