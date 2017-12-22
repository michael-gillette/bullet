# python imports
from setuptools import setup, find_packages

# module imports
from bullet import __version__

setup(
    name='bullet',
    description='Bullet is an InfluxDB data generator',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'arrow>=0.12.0',
        'influxdb>=5.0.0',
    ]
)

