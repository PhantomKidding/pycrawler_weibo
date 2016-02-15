# -*- coding: utf-8 -*-

import json
import re
import sys

import bs4
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


class TopicParser:

    PATTERN = re.compile('<script>STK && STK.pageletM && STK.pageletM.view\((.*)\)</script>', re.MULTILINE)

    def __init__(self, website):
        self.hasResult = not isNoResult(website)
        self._weibosSoup = self.getWeibosSoup(website)
        self.weibos = []

    def retrieve(self):
        if self.hasResult:
            for weiboSoup in self._weibosSoup:
                weibo = getInfo(weiboSoup)
                if weibo is not None:
                    self.weibos.append(weibo)
        return self

    def getWeibosSoup(self, website):
        if self.hasResult:
            for block in self.PATTERN.findall(website):
                block_json = json.loads(block)
                if 'pid' in block_json.keys() and block_json['pid'] == 'pl_weibo_direct':
                    return BeautifulSoup(block_json['html'], 'html.parser') \
                        .find_all('div', class_='WB_cardwrap S_bg2 clearfix')


def getInfo(weibo):
    out = dict()
    out['raw'] = weibo
    out['mid'] = weibo.find(has_mid).attrs['mid']
    try:
        out['isforward'] = weibo.find(has_isforward)['isforward']
        forward = weibo.find('div', class_='comment')
        out['forwarduid'] = forward.find('div', class_='comment_info').div.a.attrs['usercard'].split('=')[1]
        out['forwardmid'] = forward.find('div', class_='feed_action clearfix W_fr').find_all('li')[2].a.attrs['action-data'].split('=')[1]
    except TypeError:
        out['isforward'] = u'0'
        out['forwarduid'] = ''
        out['forwardmid'] = ''

    # content
    weiboDetails = weibo.find('div', class_='feed_content wbcon')
    userInfo = weiboDetails.a.attrs
    out['nick'] = userInfo['nick-name']
    out['uid'] = userInfo['usercard'].split('&')[0].split('=')[1]
    out['weibo'] = parseWeibo(weiboDetails.p)
    # date time via
    weiboFroms = weibo.find_all('div', class_='feed_from W_textb')[-1]
    out['datetime'] = weiboFroms.a.attrs['title']
    out['via'] = re.sub(u'.+? (来自|via) | +$|\n', '', weiboFroms.text)

    # number of forwards comments and likes
    try:
        weiboActions = weibo.find_all('div', 'feed_action clearfix')[-1].find_all('span', class_='line S_line1')
        forwards = re.sub(u'转发| |"', '', weiboActions[1].text)
        comments = re.sub(u'评论| |"', '', weiboActions[2].text)
        likes = weiboActions[3].text
        out['forwards'] = u'0' if forwards == u'' else forwards
        out['comments'] = u'0' if comments == u'' else comments
        out['likes'] = u'0' if likes == u'' else likes
    except IndexError:
        out['forwards'] = u'0'
        out['comments'] = u'0'
        out['likes'] = u'0'
        print '\t微博 ' + out['mid'] + ' feed_action部分缺失,请检查是否均为0.'
    return out


def parseWeibo(weibo):
    content = ''
    for child in weibo.children:
        if type(child) == bs4.element.NavigableString:
            line = child.string.encode('unicode-escape')
            line = re.sub('\\\\[a-zA-Z0-9]{9}', '', line).decode('unicode-escape')  # remove emoji
            line = re.sub('"', '\\"', line)
            content += line
        elif type(child) == bs4.element.Tag:
            if 'http' not in child.text:
                content += child.text
            # add face into content
            if child.text == '' and child.has_attr('type') and child['type'] == 'face':
                content += ' ' + child.attrs['title'] + ' '
        else:
            print 'Unexpected Beautifulsoup type in \n' + weibo.text
    content = re.sub(' +', ' ', content)
    return re.sub('\n|\t', '', content)


def isNoResult(website):
    p = re.compile('<div class=\\\\"(.+?)\\\\">')
    return 'search_noresult' in p.findall(website)


def has_mid(tag):
    return tag.has_attr('mid')


def has_isforward(tag):
    return tag.has_attr('isforward')