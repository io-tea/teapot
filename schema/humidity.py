from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import HumidityModel


class Humidity(SQLAlchemyObjectType):
    class Meta:
        model = HumidityModel
        interfaces = (relay.Node,)
