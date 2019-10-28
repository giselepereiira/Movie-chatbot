from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()

db_config = {'drivername': 'postgres',
             'username': 'tdx',
             'password': 'challenge_nlp',
             'host': 'localhost',
             'database': 'chatbot',
             'port': 5432}
db_string = URL(**db_config)
# Create all tables defined before.
engine = create_engine(db_string)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()


def connection_from():
    if hasattr(engine, 'cursor'):
        return engine, False
    if hasattr(engine, 'connection'):
        return engine.connection, False
    return engine.raw_connection(), True
