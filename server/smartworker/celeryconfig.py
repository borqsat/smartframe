from smartserver import config
from celery.schedules import crontab

# Included Taskes
CELERY_INCLUDE = ['smartworker.tasks']
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
    'add-every-30-seconds': {
        'task': 'smarkworker.tasks.add',
        'schedule': crontab(minute="*/1"),
        'args': (100, 2)
    },
}

CELERY_TIMEZONE = 'Asia/Shanghai'
