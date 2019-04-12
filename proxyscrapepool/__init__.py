# -*- coding: utf-8 -*-
# author: Luke

from flask import Flask
from flask_redis import FlaskRedis
from flask_mail import Mail
from celery import Celery

def make_celery(app):
    celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"], backend=app.config["CELERY_RESULT_BACKEND"])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask('proxyscrapepool')
app.config.from_pyfile('settings.py')
mail = Mail(app)
# redis_store = FlaskRedis(app, decode_responses=True)
redis_store = FlaskRedis.ConnectionPool(app)
redis_store = FlaskRedis.StrictRedis(connection_pool=redis_store)
celery = make_celery(app)

from proxyscrapepool import errors, commands
from proxyscrapepool.views import *

if __name__ == '__main__':
    app.run(debug=True)