from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base




SQLALCHEMY_DATABASE_URL = 'postgresql://cosmetics_db_4lo5_user:8zGoFX5vJIipKkBpAbQZHO9BIJXLVkqL@dpg-d0ipaph5pdvs739o4ntg-a.oregon-postgres.render.com/cosmetics_db_4lo5'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session_local = sessionmaker(autocommit = False, autoflush= False, bind=engine)

Base = declarative_base()