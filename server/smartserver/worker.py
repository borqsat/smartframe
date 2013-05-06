from __future__ import absolute_import

from celery import Celery
from . import celeryconfig


worker = Celery('smartserver.worker')

# Optional configuration, see the application user guide.
worker.config_from_object(celeryconfig)


if __name__ == '__main__':
    worker.start()
