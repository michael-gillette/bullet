# python imports
import time
import json
import random
import logging
from typing import List, Dict, NamedTuple
from argparse import Namespace

# vendor imports
import arrow
from influxdb import InfluxDBClient


logger = logging.getLogger('bullet')


class Tag(NamedTuple):
    node: str
    layer: str
    genre: str


Metric = Dict[Tag, int]


def run(options: Namespace):
    """ Configures and instantiates all dependencies required for the
    application to execute successfully.

    :param options: parsed arguments defined in cli.py
    :type options: Namespace
    """
    # log arguments
    logger.info(f'arguments {vars(options)}')
    # configure the InfluxDB connection
    client = InfluxDBClient.from_dsn(
        options.influx,
        # hold program until a connection is acquired
        retries=0
    )
    logger.info('influx connection established')
    # the configured database needs to exist
    client.create_database(client._database)
    logger.info(f'influx database "{client._database}" created')
    # configure the random number generator
    random.seed(options.seed)
    logger.info(f'random number generator prepared')
    # create the requisite state
    state = new_state()
    # generate the data
    while True:
        generate(client, state)
        time.sleep(1)


def new_state() -> Metric:
    m = dict()
    for node_id in range(1, 5):
        for layer_id in range(1, 3):
            for record_id in range(1, 7):
                t = Tag(
                    f'node-{node_id}',
                    f'layer-{layer_id}',
                    f'record-{record_id}'
                )
                m[t] = 0
    return m


def generate(client: InfluxDBClient, state: Metric):
    # all nodes run on synchronized clocks and submit metrics in parallel
    now = arrow.utcnow().floor('second')
    # queue all metrics to send in batch
    points: List[dict] = []

    # iterate over all tags
    for tag in state.keys():
        # nodes store metrics as counters, so increment randomly
        state[tag] += random.randint(1, 500)

        # prepare the metric for publish
        points.append({
            'measurement': 'bullet_metric',
            'tags': tag._asdict(),
            'time': now.isoformat(),
            'fields': {
                'value': state[tag]
            }
        })

    # write all points to InfluxDB
    client.write_points(points)

    # log success
    logger.info(f'points submitted for time @ {now.isoformat()}')
