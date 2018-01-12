import random
import datetime

from database import (
    db_session,
    CupModel,
    GreyscaleModel,
    HumidityModel,
    LiquidModel,
    TemperatureModel,
)


def generate_fake_data(cups, samples):
    db_session.add_all([CupModel(id=cup) for cup in range(cups)])
    db_session.commit()

    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=10)
    for cup in range(cups):
        generate_fake_cup(cup, timestamp, samples)


def generate_fake_cup(cup, timestamp, samples):
    values = (0, 0, 0, 0)

    for _ in range(samples):
        delta = [random.randint(0, 20) for _ in range(4)]
        values = [sum(x) for x in zip(values, delta)]
        timestamp += datetime.timedelta(seconds=5)

        db_session.add_all([
            GreyscaleModel(
                value=values[0],
                timestamp=timestamp,
                cup_id=cup,
            ),
            HumidityModel(
                value=values[1],
                timestamp=timestamp,
                cup_id=cup,
            ),
            LiquidModel(
                value=values[2],
                timestamp=timestamp,
                cup_id=cup,
            ),
            TemperatureModel(
                value=values[3],
                timestamp=timestamp,
                cup_id=cup,
            )
        ])
        db_session.commit()
