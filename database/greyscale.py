from sqlalchemy import Column, DateTime, Integer, func, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base
from database.cup import CupModel


class GreyscaleModel(Base):
    __tablename__ = 'greyscale'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    value = Column(Integer)

    cup_id = Column(Integer, ForeignKey('cup.id'))
    cup = relationship(CupModel, uselist=False, backref=backref('greyscale_levels', uselist=True, cascade='delete,all'))
