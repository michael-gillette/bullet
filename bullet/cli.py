# python imports
from argparse import ArgumentParser


parser = ArgumentParser(prog='bullet')

parser.add_argument('--seed', type=int, default=564, help='')

parser.add_argument('-s', '--server-host', type=str)

parser.add_argument('-p', '--server-port', type=int, choices=range(1, 65536))


def main():
    options = parser.parse_args()
