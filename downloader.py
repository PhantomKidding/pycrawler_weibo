# -*- coding: utf-8 -*-

import os
import random
import socket
import time
import urllib2

from url import *
from webparser import SearchParser


class WeiboDownloader:

    MAX_SEARCH_RETRY = 2
    MAX_LOAD_RETRY = 5

    def __init__(self,
                 keyword,
                 page=1,
                 sqlConnector=None,
                 htmlOutputDir=''):

        self._keyword = keyword
        self._page = page
        self._html = ''
        self._htmlOutputDir = htmlOutputDir
        self._url = get_search_url(self._keyword, self._page)

        self._conn = sqlConnector
        self._cursor = None
        self._table = ''

        self._searchRetry = 0
        self._loadRetry = 0

        self.weibos = []
        self.hasResult = True

    def load(self):
        print '正在载入 ' + self._keyword + ' 第' + str(self._page) + '页...',
        try:
            self._html = urllib2.urlopen(self._url, timeout=60).read()
        except socket.timeout:
            if self._loadRetry <= self.MAX_LOAD_RETRY:
                print '\t第' + str(self._loadRetry) + '次重连'
                self._loadRetry += 1
                self.load()
            else:
                print '\t尝试连接' + str(self.MAX_LOAD_RETRY) + '次均超时.'
                print '\t休息一小时后重连'
                self._loadRetry = 0
                time.sleep(3600 + random.uniform(-10, 10))
                self.load()
        print u'\t成功'
        if self._htmlOutputDir != '':
            self._htmlOutputDir = re.sub('//', '/', self._htmlOutputDir + '/')
            self.saveHtml()
        return self

    def retrieve(self):
        parser = SearchParser(self._html).parse()
        self.hasResult = parser.hasResult
        if self.hasResult:
            self.weibos = parser.weibos
            if self._conn is not None:
                parser.toMySQL(self._conn)
            print self._keyword + ' 第' + str(self._page) + '页获取完毕'
            return self
        elif self._searchRetry <= self.MAX_SEARCH_RETRY:
            self._searchRetry += 1
            print self._keyword + ' 第' + str(self._page) + '页没有结果,',
            print '休息60秒后第' + str(self._searchRetry) + '次重载'
            time.sleep(random.uniform(50, 70))
            return self.retrieve()
        else:
            print self._keyword + ' 第' + str(self._page) + \
                  '没有结果,第' + str(self._page - 1) + '页是最后一页'
            return self

    # save html
    def saveHtml(self):
        if not os.path.exists(self._htmlOutputDir):
            os.mkdir(self._htmlOutputDir)
        fp_raw = open(self._htmlOutputDir + self._keyword + 'page' + str(self._page) + '.html', 'w+')
        fp_raw.write(self._html)
        fp_raw.close()

    def set_max_search_retry(self, n):
        self.MAX_SEARCH_RETRY = n
        return self

    def set_max_load_retry(self, n):
        self.MAX_LOAD_RETRY = n
        return self
