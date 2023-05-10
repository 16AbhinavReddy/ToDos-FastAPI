from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database_url = 'sqlite:///./todos_apk.db'
database_url = 'postgresql://postgres:string@localhost/TodoApplicationdatabase'

engine = create_engine(database_url)

sessionlocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

base = declarative_base()