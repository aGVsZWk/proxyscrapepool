# -*- coding: utf-8 -*-
# author: Luke
from app import celery


@celery.task
def add_together(a, b):
    return a + b

@celery.task
def pool_start():
    from getData import ProxyPool
    pp = ProxyPool()
    pp.process_run()
    print('celery调用成功')