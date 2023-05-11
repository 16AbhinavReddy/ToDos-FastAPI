from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database_url = 'sqlite:///./todos_apk.db'
# database_url = 'postgresql://postgres:string@localhost/TodoApplicationdatabase'
database_url = 'mysql+pymysql://root:1234567890@127.0.0.1:3306/TodoApplicationDatabase'

# engine = create_engine(database_url, connect_args={'check_same_thread': False})   // For sqlite only not for postgresql and mysql
engine = create_engine(database_url)

sessionlocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

base = declarative_base()