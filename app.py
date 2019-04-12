# -*- coding: utf-8 -*-
# author: Luke

from flask import Flask
from flask_redis import FlaskRedis
from celery import Celery

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379',
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'



def make_celery(app):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)
redis_store = FlaskRedis(app, decode_responses=True)


@app.route('/')
def index():
    # redis_store.lpush("proxy", 1, 2, 3, 4)
    # redis_store.lpush("proxy", *(1,2,3,4))
    # data = redis_store.lrange("proxy",0, 3)
    # redis_store.lpop("proxy")
    # redis_store.rpop("proxy")
    # print(data)
    return "<h1>hello</h1>"



if __name__ == '__main__':
    app.run(debug=True)