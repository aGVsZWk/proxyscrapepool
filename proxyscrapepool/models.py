# -*- coding: utf-8 -*-
# author: Luke
from datetime import datetime

from proxyscrapepool import db



class Proxy(db.Document):
    figer = db.StringField(required=True, unique=True)  # 指纹，用于获取
    ip = db.StringField(required=True)      # ip
    port = db.IntField(required=True)   # 端口
    type = db.StringField(required=True, max_length=10)     # 协议类型
    is_outwall = db.BooleanField(default=False)      # 是否能翻墙
    delay_time = db.IntField(default=0)     # 延迟
    loss_packet_percent = db.IntField(default=0)    # 丢包百分比
    source = db.StringField()    # 来源

    is_ok = db.BooleanField(default=False)  # 是否还能使用
    create_time = db.DateTimeField()    # 获取时间
    update_time = db.DateTimeField()    # 更新时间


    def save(self, *args, **kwargs):
        now = datetime.now()
        if not self.create_time:
            self.create_time = now
        self.update_time = now
        return super(Proxy, self).save(*args, **kwargs)


    def to_dict(self):
        ret_dict = {}
        ret_dict['figer'] = self.figer
        ret_dict['ip'] = self.ip
        ret_dict['port'] = self.port
        ret_dict['type'] = self.type
        ret_dict['is_outwall'] = self.is_outwall
        ret_dict['delay_time'] = self.delay_time
        ret_dict['loss_packet_percent'] = self.loss_packet_percent
        ret_dict['source'] = self.source
        ret_dict['create_time'] = self.create_time
        ret_dict['update_time'] = self.update_time
        ret_dict['is_ok'] = self.is_ok
        return ret_dict

    def __unicode__(self):
        type_ip_port = self.type + "://" + self.ip + ":" + self.port
        return type_ip_port

    def __str__(self):
        type_ip_port = self.type + "://" + self.ip + ":" + self.port
        return type_ip_port

    meta = {
        "allow_inheritance": True,  # 不加此行会报错
        "indexes": ['figer'],
        "ordering": ['-update_time']
    }