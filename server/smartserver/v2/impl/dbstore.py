#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gridfs
import memcache
import hashlib
import uuid
import base64
from bson.objectid import ObjectId
from datetime import datetime
from datetime import timedelta
import time
from collections import defaultdict
from random import choice
import string
import pymongo
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo import ReadPreference

from ..config import MEMCACHED_URI, MONGODB_URI, MONGODB_REPLICASET
# TODO need refactoring
import beaker.cache
from beaker.util import parse_cache_config_options

mc_url = MEMCACHED_URI
cache = beaker.cache.Cache("memcached", type="ext:memcached",
                           lock_dir="/tmp/cache/lock",
                           url=mc_url, expire=600)
cache_opts = {
    'cache.lock_dir': '/tmp/cache/lock_memcached',
    'cache.type': 'ext:memcached',
    'cache.url': mc_url,
    'cache.expire': 600,
    'cache.regions': 'local, local_short',
    'cache.local_short.lock_dir': '/tmp/cache/lock_local_short',
    'cache.local_short.type': 'memory',
    'cache.local_short.expire': '10',
    'cache.local.lock_dir': '/tmp/cache/lock_local',
    'cache.local.type': 'memory',
    'cache.local.expire': '300'
}
cm = beaker.cache.CacheManager(**parse_cache_config_options(cache_opts))

DATE_FORMAT_STR = "%Y.%m.%d-%H.%M.%S"
DATE_FORMAT_STR1 = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_STR2 = "%Y/%m/%d %H:%M"
IDLE_TIME_OUT = 1800

class DataStore(object):

    """
    Class DbStore provides the access to MongoDB DataBase
    """

    def __init__(self, mongo_client, mem):
        """
        do the database instance init works
        """
        print 'init db store class!!!'

        self._db = mongo_client.smartServer
        self._fsdb = mongo_client.smartFiles
        self._fs = gridfs.GridFS(self._fsdb, collection="fs")
        self._mc = mem

    def doFind(self, collection, spec, fields={}):
        return list(self._db[collection].find(spec, fields))
        
    def doInsert(self, collection, doc):
        self._db[collection].insert(doc)

    def doFind_and_Modify(self, collection, query, update):
        return self._db[collection].find_and_modify(query, update, new=True, upsert=True)

def __getStore():
    mongo_uri = MONGODB_URI
    replicaset = MONGODB_REPLICASET
    mongo_client = MONGODB_REPLICASET and MongoReplicaSetClient(
        mongo_uri, replicaSet=replicaset, read_preference=ReadPreference.PRIMARY) or MongoClient(mongo_uri)
    mem = memcache.Client(MEMCACHED_URI.split(','))
    return DataStore(mongo_client, mem)

store = __getStore()
