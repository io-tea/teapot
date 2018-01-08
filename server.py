import logging
import asyncio

import aiocoap.resource as resource
import aiocoap

import database

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


class Resource(resource.Resource):
    __model__ = None

    async def render_put(self, request):
        logging.debug('{} PUT {}'.format(self.__model__.__name__, request.payload))


class GreyscaleResource(Resource):
    __model__ = database.GreyscaleModel


class HumidityResource(resource.Resource):
    __model__ = database.HumidityModel


class LiquidResource(resource.Resource):
    __model__ = database.LiquidModel


class TemperatureResource(resource.Resource):
    __model__ = database.TemperatureModel


def main():
    root = resource.Site()
    root.add_resource(('greyscale',), GreyscaleResource())
    root.add_resource(('humidity',), HumidityResource())
    root.add_resource(('liquid',), LiquidResource())
    root.add_resource(('temperature',), TemperatureResource())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
