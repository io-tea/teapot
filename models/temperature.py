from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import relationship

from .database import Base
from .cup import CupModel


class TemperatureModel(Base):
    __tablename__ = 'temperature'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    value = Column(Integer)

    cup = relationship(CupModel, uselist=False, backref='temperatures')
