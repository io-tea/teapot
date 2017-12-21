from graphene_sqlalchemy import SQLAlchemyConnectionField
import graphene

from schema.cup import Cup
from schema.greyscale import Greyscale
from schema.humidity import Humidity
from schema.liquid import Liquid
from schema.temperature import Temperature

__all__ = ['schema', ]


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_cups = SQLAlchemyConnectionField(Cup)


schema = graphene.Schema(query=Query, types=[Greyscale, Humidity, Liquid, Temperature])
