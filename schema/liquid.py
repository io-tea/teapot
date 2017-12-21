from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import LiquidModel


class Liquid(SQLAlchemyObjectType):
    class Meta:
        model = LiquidModel
        interfaces = (relay.Node,)
