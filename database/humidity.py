from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import relationship, backref

from database import Base
from database.cup import CupModel


class HumidityModel(Base):
    __tablename__ = 'humidity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    value = Column(Float)

    cup_id = Column(Integer, ForeignKey('cup.id'))
    cup = relationship(CupModel, uselist=False, backref=backref('humidity_levels', uselist=True, cascade='delete,all'))
