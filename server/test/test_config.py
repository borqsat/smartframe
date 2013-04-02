import unittest
import sys
import os

DIRNAME = os.path.abspath(os.path.dirname(__file__))


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
        from smartserver import config
        self.config = reload(config)

    def tearDown(self):
        del os.environ["MONGODB_URI"]
        del os.environ["MONGODB_REPLICASET"]
        del os.environ["REDIS_URI"]
        del os.environ["MEMCACHED_URI"]
        del os.environ["WEB_HOST"]
        del os.environ["WEB_PORT"]
        sys.argv = self.orig_argv

    def testLoadConfigFromEnv(self):
        self.assertEqual(self.config.MONGODB_URI, "mongo://192.168.0.1:6666")
        self.assertEqual(self.config.MONGODB_REPLICASET, "replicaset")
        self.assertEqual(self.config.REDIS_URI, "redis://192.168.0.1:12345")
        self.assertEqual(self.config.REDIS_HOST, "192.168.0.1")
        self.assertEqual(self.config.REDIS_PORT, 12345)
        self.assertEqual(self.config.MEMCACHED_URI, "192.168.0.1:6667")
        self.assertEqual(self.config.WEB_HOST, "www.google.com")
        self.assertEqual(self.config.WEB_PORT, 8080)


class TestConfigDefaultEnv(unittest.TestCase):
    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1]
        from smartserver import config
        self.config = reload(config)

    def tearDown(self):
        sys.argv = self.orig_argv

    def testLoadConfigFromEnv(self):
        self.assertEqual(self.config.MONGODB_URI, "mongodb://localhost:27017")
        self.assertEqual(self.config.MONGODB_REPLICASET, None)
        self.assertEqual(self.config.REDIS_URI, "redis://localhost:6379")
        self.assertEqual(self.config.REDIS_HOST, "localhost")
        self.assertEqual(self.config.REDIS_PORT, 6379)
        self.assertEqual(self.config.MEMCACHED_URI, "localhost:11211")
        self.assertEqual(self.config.WEB_HOST, "")
        self.assertEqual(self.config.WEB_PORT, 80)
