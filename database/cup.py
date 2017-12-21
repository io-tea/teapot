from sqlalchemy import Column, Integer

from database import Base


class CupModel(Base):
    __tablename__ = 'cup'
    id = Column(Integer, primary_key=True, autoincrement=True)
