from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import CupModel


class Cup(SQLAlchemyObjectType):
    class Meta:
        model = CupModel
        interfaces = (relay.Node,)
