# -*- coding: utf-8 -*-

import random
import time
import logging

import MySQLdb

from downloader import WeiboDownloader


class WeiboCrawler:

    MYSQL_HOST = 'local'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DATABASE = 'weibo'
    MYSQL_PORT = 3306
    MYSQL_CHARSET = 'utf8mb4'

    def __init__(self,
                 isConnectMySQL=False,
                 htmlOutputDir=''):
        self._keywords = None
        self._pages = None
        self._htmlOutputDir = htmlOutputDir
        self._isConnectMySQL = isConnectMySQL
        self._conn = None

        self.hasResult = True

        if self._isConnectMySQL:
            self._conn = MySQLdb.connect(
                host='127.0.0.1' if self.MYSQL_HOST == 'local' else self.MYSQL_HOST,
                user=self.MYSQL_USERNAME,
                passwd=self.MYSQL_PASSWORD,
                db=self.MYSQL_DATABASE,
                port=self.MYSQL_PORT,
                charset=self.MYSQL_CHARSET,
                use_unicode=False)
            print u'连入数据库'

    # def search(self, keywords, pages):
    #     if type(keywords) is str:
    #         self._search_keyword(keywords)
    #     elif type(keywords) is list:
    #         for keyword in keywords:
    #             self._search_keyword(keyword)
    #     else:
    #         print 'Keywords TypeError'

    def search(self, keywords, pages=range(1,51)):
        if type(keywords) is str:
            for page in pages:
                downloader = WeiboDownloader(keywords, page, self._conn, self._htmlOutputDir).load().retrieve()
                self.hasResult = downloader.hasResult
                if self.hasResult:
                    sec = random.uniform(5, 15)
                    print '随机睡眠' + str(sec) + '秒\n'
                    time.sleep(sec)
                else:
                    break
        elif type(keywords) is list:
            for keyword in keywords:
                self.search(keyword, pages)
        else:
            print 'Keywords TypeError, please enter str or list.'
