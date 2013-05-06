#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from urlparse import urlparse

__all__ = ["MONGODB_URI", "MONGODB_REPLICASET", "REDIS_URI", "REDIS_HOST",
           "REDIS_PORT", "REDIS_DB", "MEMCACHED_URI", "WEB_HOST", "WEB_PORT"]


MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_REPLICASET = os.getenv("MONGODB_REPLICASET")
REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")
MEMCACHED_URI = os.getenv("MEMCACHED_URI", "localhost:11211")
WEB_HOST = os.getenv("WEB_HOST", "")
WEB_PORT = int(os.getenv("WEB_PORT", "80"))

ru = urlparse(REDIS_URI)
REDIS_HOST = ru.hostname
REDIS_PORT = ru.port
if ru.path.find("/") == 0:
    REDIS_DB = int(ru.path[1:])
else:
    REDIS_DB = 0
