#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""YSTAFDB CLI

Usage:
  ystafdb-cli regenerate <dirpath>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from ystafdb import generate_ystafdb
import sys


def main():
    try:
        args = docopt(__doc__, version='0.1')
        generate_ystafdb(args["<dirpath>"])
    except KeyboardInterrupt:
        print("Terminating CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
