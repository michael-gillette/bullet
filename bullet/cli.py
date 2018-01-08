# python imports
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# module imports
from . import core, types


logging.basicConfig(level=logging.INFO)


parser = ArgumentParser(prog='bullet',
                        formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('--seed', type=int,
                    default=564, help='A seed for the random data generated')

parser.add_argument('--influx', type=types.influxdb_dsn,
                    default='influxdb://root:root@localhost:8086/bullet',
                    help='InfluxDB connection string')

def main():
    options = parser.parse_args()
    try:
        core.run(options)
    except KeyboardInterrupt:
        raise SystemExit
