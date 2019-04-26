# -*- coding: utf-8 -*-
# author: Luke
import os
from celery.schedules import crontab


SECRET_KEY = os.environ.get('SECRET_KEY', 'secret string')

# Flask-Redis configuration
# REDIS_URL = "redis://localhost:6379/0"
REDIS_PORT = 6379
REDIS_HOST = 'localhost'
REDIS_DB = 0

# flask-mongoengine configuration
MONGODB_DB = 'proxyscrapepool'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
# MONGODB_USERNAME = 'luke'
# MONGODB_PASSWORD =
# MONGODB_CONNECT = False
# or
# MONGODB_SETTINGS = {
#     'db': 'project1',
#     'host': '192.168.1.35',
#     'port': 12345,
#     'username':'webapp',
#     'password':'pwd123',
#     # 'connect': False
# }




# getProxy Redis configuration
PROXY_QUEUE = "proxy_queue"
PROXY_COLLECTOR = "proxy_collector"
INTERVAL_TIME = 1
RETRY_TIMES = 3
# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/2'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERYBEAT_SCHEDULE = {
    'getData':{
        'task':'proxyscrapepool.tasks.get_proxy_task',
        "schedule": crontab(minute='*/5'),
    }
}
CELERYD_CONCURRENCY = 2      # celery worker concurrent quantity
CELERYD_MAX_TASKS_PER_CHILD = 2   # worker finished tasks number before died


# Flask-Mail configuration
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = 'flask@example.com'