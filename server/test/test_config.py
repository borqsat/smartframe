import unittest
import sys
import os
from smartserver import config


class TestConfigEnv(unittest.TestCase):
    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1]
        os.environ["MONGODB_URI"] = "mongo://192.168.0.1:6666"
        os.environ["MONGODB_REPLICASET"] = "replicaset"
        os.environ["REDIS_URI"] = "redis://192.168.0.1:12345"
        os.environ["MEMCACHED_URI"] = "192.168.0.1:6667"
        os.environ["WEB_HOST"] = "www.google.com"
        os.environ["WEB_PORT"] = "8080"
        reload(config)

    def tearDown(self):
        del os.environ["MONGODB_URI"]
        del os.environ["MONGODB_REPLICASET"]
        del os.environ["REDIS_URI"]
        del os.environ["MEMCACHED_URI"]
        del os.environ["WEB_HOST"]
        del os.environ["WEB_PORT"]
        sys.argv = self.orig_argv

    def testLoadConfigFromEnv(self):
        self.assertEqual(config.MONGODB_URI, "mongo://192.168.0.1:6666")
        self.assertEqual(config.MONGODB_REPLICASET, "replicaset")
        self.assertEqual(config.REDIS_URI, "redis://192.168.0.1:12345")
        self.assertEqual(config.REDIS_HOST, "192.168.0.1")
        self.assertEqual(config.REDIS_PORT, 12345)
        self.assertEqual(config.MEMCACHED_URI, "192.168.0.1:6667")
        self.assertEqual(config.WEB_HOST, "www.google.com")
        self.assertEqual(config.WEB_PORT, 8080)


class TestConfigDefaultEnv(unittest.TestCase):
    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1]
        reload(config)

    def tearDown(self):
        sys.argv = self.orig_argv

    def testLoadConfigFromEnv(self):
        self.assertEqual(config.MONGODB_URI, "mongodb://localhost:27017")
        self.assertEqual(config.MONGODB_REPLICASET, None)
        self.assertEqual(config.REDIS_URI, "redis://localhost:6379")
        self.assertEqual(config.REDIS_HOST, "localhost")
        self.assertEqual(config.REDIS_PORT, 6379)
        self.assertEqual(config.MEMCACHED_URI, "localhost:11211")
        self.assertEqual(config.WEB_HOST, "localhost")
        self.assertEqual(config.WEB_PORT, 80)


class TestConfigFile(unittest.TestCase):
    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1] + ["-c", "test/test.cfg"]
        reload(config)

    def tearDown(self):
        sys.argv = self.orig_argv

    def testLoadConfigFile(self):
        self.assertEqual(config.MONGODB_URI, "mongodb://test:27017")
        self.assertEqual(config.MONGODB_REPLICASET, "ats_rs")
        self.assertEqual(config.REDIS_URI, "redis://test:6379")
        self.assertEqual(config.REDIS_HOST, "test")
        self.assertEqual(config.REDIS_PORT, 6379)
        self.assertEqual(config.MEMCACHED_URI, "test:11211")
        self.assertEqual(config.WEB_HOST, "test")
        self.assertEqual(config.WEB_PORT, 8081)


class TestConfigFileDefault(unittest.TestCase):
    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1] + ["-c", "test/test_lack.cfg"]
        reload(config)

    def tearDown(self):
        sys.argv = self.orig_argv

    def testLoadConfigFile(self):
        self.assertEqual(config.MONGODB_URI, "mongodb://localhost:27017")
        self.assertEqual(config.MONGODB_REPLICASET, None)
        self.assertEqual(config.REDIS_URI, "redis://localhost:6379")
        self.assertEqual(config.REDIS_HOST, "localhost")
        self.assertEqual(config.REDIS_PORT, 6379)
        self.assertEqual(config.MEMCACHED_URI, "localhost:11211")
        self.assertEqual(config.WEB_HOST, "test")
        self.assertEqual(config.WEB_PORT, 8081)
