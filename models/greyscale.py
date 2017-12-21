from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import relationship

from .database import Base
from .cup import CupModel


class GreyscaleModel(Base):
    __tablename__ = 'greyscale'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    value = Column(Integer)

    cup = relationship(CupModel, uselist=False, backref='greyscales')
