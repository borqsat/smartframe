#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import ConfigParser
import os


__all__ = ["config"]


def _read_config():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--config", dest="config", type="string",
                      default="development.ini", help="the configuration FILE.", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.error("Invalid arguments.")

    if not os.path.exists(options.config):
        parser.error("Config file doesn't exists.")

    config = ConfigParser.ConfigParser()
    config.read(options.config)

    return config


config = _read_config()
