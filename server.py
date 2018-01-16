#!/usr/bin/env python3

import click

import logging
import asyncio

import aiocoap.resource as resource
import aiocoap

from database import db_session
import database

from utils import PeriodicTask

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)


class Resource(resource.Resource):
    __model__ = None
    _values = None

    def __init__(self):
        super().__init__()
        self._values = []

    async def render_put(self, request):
        try:
            value = self.process_message(request.payload)
            self._values.append(value)
        except ValueError:
            logging.debug(str(ValueError))

        return aiocoap.Message()

    def update(self):
        """
        Pushes gathered results to database.
        This should be ran periodically.
        :return: None
        """
        if len(self._values) == 0:
            logging.debug('Nothing to update in {}'.format(self.__model__.__name__))
            return

        cup = db_session.query(database.CupModel).order_by('-id').first()
        value = sum(self._values) / len(self._values)
        self._values = []
        db_session.add(self.__model__(value=value, cup_id=cup.id))

    def process_message(self, payload):
        """
        Parses message payload.
        :param payload: message payload
        :return: decoded value
        :raises ValueError: if the message is invalid
        """
        payload = str(payload)
        value, message_id = None, None

        try:
            value, message_id = payload.split(',')
        except ValueError:
            ValueError('Invalid message {}'.format(payload))

        return value


class GreyscaleResource(Resource):
    __model__ = database.GreyscaleModel


class HumidityResource(Resource):
    __model__ = database.HumidityModel


class LiquidResource(Resource):
    __model__ = database.LiquidModel


class TemperatureResource(Resource):
    __model__ = database.TemperatureModel


@click.command()
@click.option('--port', default=1234)
def main(port):
    greyscale = GreyscaleResource()
    humidity = HumidityResource()
    liquid = LiquidResource()
    temperature = TemperatureResource()

    PeriodicTask(greyscale.update, 5)
    PeriodicTask(humidity.update, 5)
    PeriodicTask(liquid.update, 5)
    PeriodicTask(temperature.update, 5)

    root = resource.Site()
    root.add_resource(('g',), greyscale)
    root.add_resource(('h',), humidity)
    root.add_resource(('l',), liquid)
    root.add_resource(('t',), temperature)

    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('::', port)))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
