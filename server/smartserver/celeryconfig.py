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
        'schedule': crontab(minute=0, hour=0, day_of_week='saturday')
        #'schedule': crontab(minute='*/1')
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
