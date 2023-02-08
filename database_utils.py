import yaml
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector():
    def read_db_creds(self):
        with open('db_creds.yaml', mode='r') as stream:
            return yaml.safe_load(stream)

    def init_db_engine(self):
        db_creds = self.read_db_creds()
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = db_creds.get('RDS_HOST')
        USER = db_creds.get('RDS_USER')
        PASSWORD = db_creds.get('RDS_PASSWORD')
        DATABASE = db_creds.get('RDS_DATABASE')
        PORT = db_creds.get('RDS_PORT')
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        engine.connect()
        return engine

    def list_db_tables(self):
        inspector = inspect(self.init_db_engine())
        return inspector.get_table_names()

    def upload_to_db(dataframe, table_name):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'aicore2023'
        DATABASE = 'Sales_Data'
        PORT = 5432
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        engine.connect()
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
