#!/usr/bin/env python3

import click

import logging
import asyncio

import aiocoap.resource as resource
import aiocoap

from database import db_session
import database
from sqlalchemy import desc

from utils import PeriodicTask

#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)


class Resource(resource.Resource):
    __model__ = None
    _values = None
    _values_ids = None
    _last_value = 0

    def __init__(self):
        super().__init__()
        self._values = []
        self._values_ids = set()
        self._last_value = 0

    async def render_put(self, request):
        try:
            value = self.process_message(request.payload)
            if value is not None:
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

        cup = db_session.query(database.CupModel).order_by(desc(database.CupModel.id)).first()
        if self._values:
            self._last_value = sum(self._values) / len(self._values)
        self._values = []
        self._values_ids = set()
        db_session.add(self.__model__(value=self._last_value, cup_id=cup.id))
        db_session.commit()

    def process_message(self, payload):
        """
        Parses message payload.
        :param payload: message payload
        :return: decoded value
        :raises ValueError: if the message is invalid
        """
        payload = str(payload.rstrip(b'\x00').decode('utf-8'))
        value, message_id = None, None

        try:
            value, message_id = payload.split(',')
            value = float(value)
        except ValueError:
            ValueError('Invalid message {}'.format(payload))

        if message_id in self._values_ids:
            return None
        self._values_ids.add(message_id)
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
    db_session.add(database.CupModel())
    db_session.commit()

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
