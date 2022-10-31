from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# destination DataBase
username = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
dbname = 'mecabapp'

DB = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'

# create engine
Engine = create_engine(
    DB,
    encoding = 'utf-8',
    echo = False
)
Base = declarative_base()

# create session
session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = Engine
    )
)

# use model
Base = declarative_base()
Base.query = session.query_property()