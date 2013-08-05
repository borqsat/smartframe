#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import config
from celery.schedules import crontab

# Included Taskes
CELERY_INCLUDE = ['smartserver.tasks']
# Task Broker
BROKER_URL = config.REDIS_URI
# Task Result backend
CELERY_RESULT_BACKEND = config.REDIS_URI
CELERY_TASK_RESULT_EXPIRES = 3600

# pool and threads
#CELERYD_POOL = "gevent"
#CELERYD_CONCURRENCY = 1000
#CELERYD_PREFETCH_MULTIPLIER = 1

# Scheduled tasks
CELERYBEAT_SCHEDULE = {
    'cleardirty-every-week': {
        'task': 'smartserver.tasks.ws_del_dirty',
        'schedule': crontab(minute=0, hour=0, day_of_month=1)
    },
    'validate-session-endtime-every-30-minutes': {
        'task': 'smartserver.tasks.ws_validate_session_endtime',
        'schedule': crontab(minute='*/30')
    },
    'validate-testcase-endtime-every-30-minutes': {
        'task': 'smartserver.tasks.ws_validate_testcase_endtime',
        'schedule': crontab(minute='*/30')
    },
    'validate-token-expiretime-every-30-minutes': {
        'task': 'smartserver.tasks.ws_validate_token_expiretime',
        'schedule': crontab(minute='*/30')
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
