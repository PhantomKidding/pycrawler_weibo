# -*- coding: utf-8 -*-

import re
# import sys
import urllib
import urllib2

import _mysql_exceptions

# reload(sys)
# sys.setdefaultencoding('utf8')

from webparser import TopicParser


class WeiboDownloader:

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
                    + '&b=1&page=' + str(self._page)

        self._conn = sqlConnector
        self._cursor = None
        self._table = ''

        self.weibos = []
        self.hasResult = True

    def load(self):
        print '正在载入 ' + self._keyword + ' 第' + str(self._page) + '页...',
        self._html = urllib2.urlopen(self._url).read()
        print u'\t成功'
        if self._htmlOutputDir != '':
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
                             'UNIQUE (mid)'  # keep mid unique
                             ')')

    # save html
    def saveHtml(self):
        fp_raw = open(self._htmlOutputDir + 'page' + str(self._page) + '.html', 'w+')
        fp_raw.write(self._html)
        fp_raw.close()

    # save to MySQL database
    def toMySQL(self):
        print u'\t表格录入中...'
        for weibo in self.weibos:
            try:
                self._cursor.execute('INSERT INTO ' + self._table +
                                     '(mid, weibo, uid, nick, forwards, comments, likes, time, via) '
                                     'VALUES("%s", "%s", "%s", "%s", %s, %s, %s, "%s", "%s");' %
                                     (weibo['mid'], weibo['weibo'], weibo['uid'],
                                      weibo['nick'], weibo['forwards'], weibo['comments'],
                                      weibo['likes'], weibo['datetime'], weibo['via']))
                print '\t微博' + weibo['mid'] + '已录入.'
            except _mysql_exceptions.OperationalError, e:
                print e[0], e[1]
                print weibo['weibo']
            except _mysql_exceptions.IntegrityError:
                print '\t微博' + weibo['mid'] + '已存在.'
        self._conn.commit()
        return self
