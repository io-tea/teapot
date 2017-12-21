from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import GreyscaleModel


class Greyscale(SQLAlchemyObjectType):
    class Meta:
        model = GreyscaleModel
        interfaces = (relay.Node,)
