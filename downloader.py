# -*- coding: utf-8 -*-

import os
import random
import re
import socket
import time
import urllib
import urllib2

import _mysql_exceptions

from webparser import TopicParser


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
        self._url = 'http://s.weibo.com/weibo/' \
                    + re.sub('_(%[^%]{2})%([^%]{2})_', r'\1\2',
                             urllib.quote(re.sub('(#|@)', r'_%\1_', keyword))) \
                    + '&nodup=1&page=' + str(self._page)

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
        parser = TopicParser(self._html).retrieve()
        self.hasResult = parser.hasResult
        if self.hasResult:
            self.weibos = parser.weibos
            if self._conn is not None:
                self.connectSQL()
                self.toMySQL()
            print self._keyword + ' 第' + str(self._page) + '页获取完毕'
            return self
        elif self._searchRetry <= self.MAX_SEARCH_RETRY:
            self._searchRetry += 1
            print self._keyword + ' 第' + str(self._page) + \
                  '没有结果,休息60秒后第' + str(self._searchRetry) + '次重新载入'
            time.sleep(random.uniform(50, 70))
            return self.retrieve()
        else:
            print self._keyword + ' 第' + str(self._page) + \
                  '没有结果,第' + str(self._page - 1) + '页是最后一页'
            return self

    def connectSQL(self):
        self._cursor = self._conn.cursor()
        self._cursor._defer_warnings = True
        if '#' in self._keyword:
            self._table = 'topic_' + re.sub('#', '', self._keyword)
        elif '@' in self._keyword:
            self._table = 'mention_' + re.sub('@', '', self._keyword)
        else:
            print 'Keyword does NOT have @|#'

        # create a table in database if not exists
        # with warnings.filterwarnings('ignore', 'Table \'(.+?)\' already exists'):
        self._cursor.execute('CREATE TABLE IF NOT EXISTS ' + self._table +
                             '('
                             'mid CHAR(16),'
                             'weibo VARCHAR(255),'
                             'uid CHAR(10),'
                             'nick VARCHAR(40),'
                             'forwards INT UNSIGNED DEFAULT 0,'
                             'comments INT UNSIGNED DEFAULT 0,'
                             'likes INT UNSIGNED DEFAULT 0,'
                             'time DATETIME DEFAULT NULL,'
                             'via VARCHAR(140),'
                             'isforward INT(1) DEFAULT 0,'
                             'forwarduid VARCHAR(10) DEFAULT NULL,'
                             'forwardmid VARCHAR(16) DEFAULT NULL,'
                             'UNIQUE (mid)'  # keep mid unique
                             ')')

    # save html
    def saveHtml(self):
        if not os.path.exists(self._htmlOutputDir):
            os.mkdir(self._htmlOutputDir)
        fp_raw = open(self._htmlOutputDir + 'page' + str(self._page) + '.html', 'w+')
        fp_raw.write(self._html)
        fp_raw.close()

    # save to MySQL database
    def toMySQL(self):
        print u'\t表格录入中...'
        for weibo in self.weibos:
            try:
                command = 'INSERT INTO ' + self._table + \
                          '(mid, weibo, uid, nick, forwards, comments, likes, time, via, isforward, forwarduid, forwardmid)' \
                          ' VALUES("%s", "%s", "%s", "%s", %s, %s, %s, "%s", "%s", %s, "%s", "%s");' % \
                          (weibo['mid'], weibo['weibo'], weibo['uid'],
                           weibo['nick'], weibo['forwards'], weibo['comments'],
                           weibo['likes'], weibo['datetime'], weibo['via'],
                           weibo['isforward'], weibo['forwarduid'], weibo['forwardmid'])
                self._cursor.execute(command)
                print '\t微博' + weibo['mid'] + '已录入.'
            except _mysql_exceptions.OperationalError, e:
                print e[0], e[1]
                print weibo['weibo']
            except _mysql_exceptions.IntegrityError:
                print '\t微博' + weibo['mid'] + '已存在.'
            except _mysql_exceptions.ProgrammingError, e:
                print e
                print command
                print weibo['raw']
        self._conn.commit()
        return self
