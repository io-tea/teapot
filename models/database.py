from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3', convert_unicode=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def init_database():
    Base.metadata.create_all(engine)

def get_session():
    return Session()