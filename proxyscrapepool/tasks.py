# -*- coding: utf-8 -*-
# author: Luke
from proxyscrapepool import celery, mail, app


@celery.task
def add_task(a, b):
    return a + b

@celery.task
def get_proxy_task():
    from .getProxy import ProxyPool
    pp = ProxyPool()
    pp.process_run()


@celery.task
def send_async_email_task(msg):
    with app.app_context():
        mail.send(msg)