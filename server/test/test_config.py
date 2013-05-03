import unittest
import sys
import os

DIRNAME = os.path.abspath(os.path.dirname(__file__))


class TestConfigEnv_v0(unittest.TestCase):

    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1]
        os.environ["MONGODB_URI"] = "mongodb://192.168.0.1:6666"
        os.environ["MONGODB_REPLICASET"] = "replicaset"
        os.environ["REDIS_URI"] = "redis://192.168.0.1:12345/1"
        os.environ["MEMCACHED_URI"] = "192.168.0.1:6667"
        os.environ["WEB_HOST"] = "www.google.com"
        os.environ["WEB_PORT"] = "8080"
        from smartserver.v0 import config
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
        self.assertEqual(self.config.MONGODB_URI, os.environ["MONGODB_URI"])
        self.assertEqual(self.config.MONGODB_REPLICASET, os.environ["MONGODB_REPLICASET"])
        self.assertEqual(self.config.REDIS_URI, os.environ["REDIS_URI"])
        self.assertEqual(self.config.REDIS_HOST, "192.168.0.1")
        self.assertEqual(self.config.REDIS_PORT, 12345)
        self.assertEqual(self.config.REDIS_DB, 1)
        self.assertEqual(self.config.MEMCACHED_URI, os.environ["MEMCACHED_URI"])
        self.assertEqual(self.config.WEB_HOST, os.environ["WEB_HOST"])
        self.assertEqual(self.config.WEB_PORT, int(os.environ["WEB_PORT"]))


class TestConfigDefaultEnv_v0(unittest.TestCase):

    def setUp(self):
        self.orig_argv = sys.argv
        sys.argv = self.orig_argv[0:1]
        from smartserver.v0 import config
        self.config = reload(config)

    def tearDown(self):
        sys.argv = self.orig_argv

    def testLoadConfigFromEnv(self):
        self.assertEqual(self.config.MONGODB_URI, "mongodb://localhost:27017")
        self.assertEqual(self.config.MONGODB_REPLICASET, None)
        self.assertEqual(self.config.REDIS_URI, "redis://localhost:6379")
        self.assertEqual(self.config.REDIS_HOST, "localhost")
        self.assertEqual(self.config.REDIS_PORT, 6379)
        self.assertEqual(self.config.REDIS_DB, 0)
        self.assertEqual(self.config.MEMCACHED_URI, "localhost:11211")
        self.assertEqual(self.config.WEB_HOST, "")
        self.assertEqual(self.config.WEB_PORT, 80)


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.envs = ["MONGODB_URI", "MONGODB_REPLICASET", "REDIS_URI",
                     "REDIS_HOST", "REDIS_PORT", "REDIS_DB", "MEMCACHED_URI",
                     "WEB_HOST", "WEB_PORT"]

    def tearDown(self):
        pass

    def testLoadConfigFromEnv(self):
        from smartserver import config
        for env in self.envs:
            self.assertTrue(env in config.__dict__)
