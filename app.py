# -*- coding: utf-8 -*-
# author: Luke

from flask import Flask
from flask_redis import FlaskRedis
app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
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