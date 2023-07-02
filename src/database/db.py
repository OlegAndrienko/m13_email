import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from fastapi import HTTPException, status

from src.conf.config import settings

# engine = create_engine('postgresql+pycopg2://user:password\
# @hostname/database_name')

# file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
# config = configparser.ConfigParser()
# config.read(file_config)

# username = config.get('DEV_DB', 'USER')
# password = config.get('DEV_DB', 'PASSWORD')
# host = config.get('DEV_DB', 'HOST')
# port = config.get('DEV_DB', 'PORT')
# database = config.get('DEV_DB', 'DB_NAME')
# domain = config.get('DEV_DB', 'DOMAIN')

# SQLALCHEMY_DATABASE_URL = f'{domain}://{username}:{password}@{host}:{port}/{database}'  #postgresql+pycopg2://user:password@hostname/database_name

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
DBSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)

#Dependency

def get_db():
    db = DBSession()
    try:
        yield db    #yield keyword is used instead of return. It allows to return a generator instead of a list.
    except SQLAlchemyError as err:
          db.rollback() 
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()  #close the database connection when the request is finished.  