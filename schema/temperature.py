from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import TemperatureModel


class Temperature(SQLAlchemyObjectType):
    class Meta:
        model = TemperatureModel
        interfaces = (relay.Node,)
