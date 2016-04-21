# -*- coding: utf-8 -*-

import json
import re
import sys

import _mysql_exceptions
from bs4 import BeautifulSoup

from webparser_search import parse_search_cardwrap, search_noresult

reload(sys)
sys.setdefaultencoding('utf8')


class SearchParser:
    """
    Parse html of Sina weibo search result
    :param website: (str) html

    :return weibos: list of BeautifulSoup of parsed weibo
    :return errors: list of caught errors during parsing html
    """

    PATTERN = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*)\)</script>', re.MULTILINE)
    PATTERN_KEYWORD_IN_TITLE = re.compile(' - (.+?) - ')

    def __init__(self, website):
        self._website = website
        self._title = BeautifulSoup(website, 'html.parser').head.title.string
        self._keyword = self.PATTERN_KEYWORD_IN_TITLE.search(self._title).group(1)
        self.hasResult = not search_noresult(website)
        self.weibos = []

        if '#' in self._keyword:
            self._table = 'topic_' + re.sub('#', '', self._keyword)
        elif '@' in self._keyword:
            self._table = 'topic_' + re.sub('@', '', self._keyword)
        else:
            print u'Wrong search keyword'

    def parse(self):
        if self.hasResult:
            for weibo in self.get_cardwrap(self._website):
                self.weibos.append(parse_search_cardwrap(weibo))
        return self

    def get_cardwrap(self, website):
        if self.hasResult:
            for block in self.PATTERN.findall(website):
                block_json = json.loads(block)
                if 'pid' in block_json.keys() and block_json['pid'] == 'pl_weibo_direct':
                    return BeautifulSoup(block_json['html'], 'html.parser') \
                        .find_all('div', class_='WB_cardwrap S_bg2 clearfix')

    def toMySQL(self, conn):
        print u'\t表格录入中...'
        cursor = conn.cursor()
        cursor._defer_warnings = True
        command_create = 'CREATE TABLE IF NOT EXISTS ' + self._table + \
                         '(mid CHAR(16), ' \
                         'weibo VARCHAR(255), ' \
                         'uid CHAR(10), ' \
                         'nick VARCHAR(40), ' \
                         'forwards INT UNSIGNED DEFAULT 0, ' \
                         'comments INT UNSIGNED DEFAULT 0, ' \
                         'likes INT UNSIGNED DEFAULT 0, ' \
                         'time DATETIME DEFAULT NULL, ' \
                         'via VARCHAR(140), ' \
                         'isforward INT(1) DEFAULT 0, ' \
                         'forwarduid VARCHAR(10) DEFAULT NULL, ' \
                         'forwardmid VARCHAR(16) DEFAULT NULL, ' \
                         'UNIQUE (mid))'  # keep mid unique
        cursor.execute(command_create)

        for weibo in self.weibos:
            command_insert = \
                'INSERT INTO ' + self._table + \
                '(mid, weibo, uid, nick, forwards, comments, likes, time, via, isforward, forwarduid, forwardmid)' \
                ' VALUES("%s", "%s", "%s", "%s", %s, %s, %s, "%s", "%s", %s, "%s", "%s");' % \
                (weibo['mid'], weibo['weibo'], weibo['uid'],
                 weibo['nick'], weibo['forwards'], weibo['comments'],
                 weibo['likes'], weibo['datetime'], weibo['via'],
                 weibo['isforward'], weibo['forwarduid'], weibo['forwardmid'])
            try:
                cursor.execute(command_insert)
                print '\t微博' + weibo['mid'] + '已录入.'
            except _mysql_exceptions.OperationalError, e:
                print e[1]
            except _mysql_exceptions.IntegrityError:
                print '\t微博' + weibo['mid'] + '已存在.'
            except _mysql_exceptions.ProgrammingError:
                print 'SQL command error: '
                print command_insert
        conn.commit()
        return self
