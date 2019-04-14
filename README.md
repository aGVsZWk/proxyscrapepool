# proxyscrapepool

## 项目说明
该项目是从某些网站上免费获取代理，打造属于自己的代理池。
目前代理的主要来源是 **https://proxyscrape.com/**

## 实现方式
flask提供接口，目录管理采用包管理结构；代理池的存储用的是redis；定时抓取用的是celery。

## 环境搭建
### 采用pipenv控制项目虚拟环境，用python-dotenv实现激活项目虚拟环境加载.env中的环境变量
### 先安装pipenv第三包扩展包
### 安装项目虚拟环境：`pipenv install`
### 激活项目虚拟环境: `pipenv shell`


## 项目启动
### 需要自己配置项目的.env文件，里面是需要加载的环境变量
### celery启动方式: `celery worker -A proxyscrapepool.celery --loglevel=info`
### celery定时任务方式: `celery -A proxyscrapepool.celery beat`
### 运行manager.py


## 未完成事件
### 1. 增加代理来源
### 2. 对代理定期校验
