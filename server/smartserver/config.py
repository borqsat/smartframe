#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import os
from urlparse import urlparse

__all__ = ["MONGODB_URI", "MONGODB_REPLICASET", "REDIS_URI", "REDIS_HOST", "REDIS_PORT",
           "MEMCACHED_URI", "WEB_HOST", "WEB_PORT"]


parser = argparse.ArgumentParser(description="Running the stability testing web application.")
parser.add_argument("-c", "--config", dest="config", type=file,
                    help="the configuration FILE.", metavar="CONFIG_FILE")
parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                    help="Turn on debug options.")

args = parser.parse_args()
if args.config:
    print("Reading configuration from %s." % args.config.name)
    config = ConfigParser.ConfigParser()
    config.readfp(args.config)
else:
    config = None

if config:
    try:
        MONGODB_URI = config.get("mongodb", "uri")
    except ConfigParser.Error:
        MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    try:
        MONGODB_REPLICASET = config.get("mongodb", "replicaSet")
    except ConfigParser.Error:
        MONGODB_REPLICASET = os.getenv("MONGODB_REPLICASET")
    try:
        REDIS_URI = config.get("redis", "uri")
    except ConfigParser.Error:
        REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
    try:
        MEMCACHED_URI = config.get("memcached", "uri")
    except ConfigParser.Error:
        MEMCACHED_URI = os.getenv("MEMCACHED_URI", "localhost:11211")
    try:
        WEB_HOST = config.get("server:web", "host")
    except ConfigParser.Error:
        WEB_HOST = os.getenv("WEB_HOST", "localhost")
    try:
        WEB_PORT = int(config.get("server:web", "port"))
    except ConfigParser.Error:
        WEB_PORT = int(os.getenv("WEB_PORT", "80"))
else:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_REPLICASET = os.getenv("MONGODB_REPLICASET")
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
    MEMCACHED_URI = os.getenv("MEMCACHED_URI", "localhost:11211")
    WEB_HOST = os.getenv("WEB_HOST", "localhost")
    WEB_PORT = int(os.getenv("WEB_PORT", "80"))

ru = urlparse(REDIS_URI)
REDIS_HOST = ru.hostname
REDIS_PORT = ru.port
