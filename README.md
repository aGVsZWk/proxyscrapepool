# proxyscrapepool

## 项目说明
该项目是从某些网站上免费获取代理，打造属于自己的代理池。
目前代理的主要来源是 **https://proxyscrape.com/**

## 实现方式
采用flask提供接口，可选用redis进行存储，也可直接采用记事本文档的方式进行存储。

## 项目启动
### celery启动方式: `celery worker -A proxyscrapepool.celery --loglevel=info`
### flask项目目录采用包管理方式，直接启动就好


## 未完成事件
### 1. 增加代理来源
### 2. 对代理定期校验
