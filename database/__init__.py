from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3', convert_unicode=True)
Base = declarative_base()

from database.cup import CupModel  # noqa: F401
from database.greyscale import GreyscaleModel  # noqa: F401
from database.humidity import HumidityModel  # noqa: F401
from database.liquid import LiquidModel  # noqa: F401
from database.temperature import TemperatureModel  # noqa: F401

__all__ = [
    'Base',
    'CupModel',
    'GreyscaleModel',
    'HumidityModel',
    'LiquidModel',
    'TemperatureModel',
    'db_init',
    'db_session'
]


def db_init():
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
db_session = Session()
