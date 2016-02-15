# -*- coding: utf-8 -*-

import random
import time

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
                 keyword,
                 pages=None,
                 isConnectMySQL=False,
                 htmlOutputDir=''):

        self._keyword = keyword
        self._pages = pages
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

    def crawl(self):
        if self._pages is None:
            self._crawl_unlimited()
        else:
            self._crawl_pages()

    def _crawl_unlimited(self):
        page = 1
        while self.hasResult:
            downloader = WeiboDownloader(self._keyword, page, self._conn).load().retrieve()
            self.hasResult = downloader.hasResult
            page += 1
            if self.hasResult:
                sleep()

    def _crawl_pages(self):
        for page in self._pages:
            downloader = WeiboDownloader(self._keyword, page, self._conn).load().retrieve()
            self.hasResult = downloader.hasResult
            if self.hasResult:
                sleep()
            else:
                break


def sleep():
    sec = random.uniform(5, 15)
    print '随机睡眠' + str(sec) + '秒\n'
    time.sleep(sec)
