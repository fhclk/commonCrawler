#!/usr/bin/env python
#-*-coding:utf-8-*-

def getDomain(url):
    '''
    根据url获取域名
    :param url: url地址
    :return: 返回域名
    '''
    try:
        urlList = url.split('://')
        newUrl = urlList[-1] if len(urlList) > 0 else ''
        urlList = newUrl.split('/')
        newUrl = urlList[0] if len(urlList) > 0 else ''
        return newUrl
    except Exception,e:
        return ''


import pymongo
def getConfigFromDB(crawler, taskNo):
    def get_config_from_db(db_url, db_port, db_name, task_no):
        '''
        从数据库中获取配置文件
        :param db_url: 数据库url
        :param db_port: 数据库端口
        :param db_name: 数据库名
        :param task_no: 配置文件对应的任务编号
        :return: 
        '''
        client = pymongo.MongoClient(db_url, db_port)
        db = client[db_name]
        task = db.task
        return task.find_one({"task_no": task_no})

    db_url = crawler.settings.get('MONGO_URI', '')
    db_port = crawler.settings.get('MONGO_PORT', 27017)
    db_name = crawler.settings.get('MONGO_DATABASE', 'test')
    return get_config_from_db(db_url, db_port, db_name, taskNo)





import re
def cleanHtmlTag(htmlText):
    '''
    清除文本中的html标签
    :param htmlText: 
    :return: 
    '''
    dr = re.compile(r'<[^>]+>', re.S)
    return dr.sub('', htmlText)


import logging
logger = logging.getLogger(__name__)

