# python imports
from argparse import ArgumentTypeError

# vendor imports
from influxdb.client import _parse_dsn


def influxdb_dsn(dsn: str) -> str:
    # validates the provided input string is indeed a valid dsn
    # by using the actual method defined in the library
    try:
        _parse_dsn(dsn)
    except ValueError as ex:
        raise ArgumentTypeError(str(ex))
    return dsn
