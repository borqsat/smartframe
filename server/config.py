#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser

__all__ = ["config", "args"]


def _read_config():
    parser = argparse.ArgumentParser(description="Running the stability testing web application.")
    parser.add_argument("-c", "--config", dest="config", type=file,
                        default="development.ini", help="the configuration FILE.",
                        metavar="CONFIG_FILE")
    parser.add_argument("-d", "--development", dest="development", action="store_true",
                        help="Using development options.")

    args = parser.parse_args()

    print("Using configuration file: %s." % args.config.name)
    config = ConfigParser.ConfigParser()
    config.readfp(args.config)

    return config, args

config, args = _read_config()
