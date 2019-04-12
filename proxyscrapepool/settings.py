# -*- coding: utf-8 -*-
# author: Luke
import os

SECRET_KEY = 'abcdefg'

# Flask-Redis configuration
REDIS_URL = "redis://localhost:6379/0"

# getProxy Redis configuration
PROXY_QUEUE = "proxy_queue"
FILTER_COLLECTOR = "proxy_filter_collector"
PROXY_HASH_MAP = "proxy_hash_map"


# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/2'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'


# Flask-Mail configuration
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = "johnfash86@gmail.com"
MAIL_PASSWORD = "shabidaohao2018!"
MAIL_DEFAULT_SENDER = 'flask@example.com'