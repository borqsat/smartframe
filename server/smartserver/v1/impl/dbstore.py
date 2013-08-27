#!/usr/bin/env python
# -*- coding: utf-8 -*-

import memcache
from pymongo import MongoClient, MongoReplicaSetClient
from pymongo import ReadPreference

from ..config import MEMCACHED_URI, MONGODB_URI, MONGODB_REPLICASET
# TODO need refactoring

class DataStore(object):

    """
    Class DbStore provides the access to MongoDB DataBase
    """

    def doFind(self, collection, spec, fields):
        return list(self._db[collection].find(spec, fields))
        
    def doFindOne(self, collection, spec, fields):
        return self._db[collection].find_one(spec, fields)
    
    def doUpdate(self, collection, spec, fields):
        return self._db[collection].update(spec, fields)
    
    def doInsert(self, collection, spec):
        return self._db[collection].insert(spec)
    

def __getStore():
    mongo_uri = MONGODB_URI
    replicaset = MONGODB_REPLICASET
    mongo_client = MONGODB_REPLICASET and MongoReplicaSetClient(
        mongo_uri, replicaSet=replicaset, read_preference=ReadPreference.PRIMARY) or MongoClient(mongo_uri)
    mem = memcache.Client(MEMCACHED_URI.split(','))
    return DataStore(mongo_client, mem)

store = __getStore()
