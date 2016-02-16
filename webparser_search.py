# -*- coding: utf-8 -*-

import bs4
import re
from bs4 import BeautifulSoup
from webparser_general import *


def parse_search_cardwrap(weibo):
    """
    :param weibo: a block of a weibo
    :type weibo: BeautifulSoup

    :return out: weibo info
    :return err: caught errors when parsing
    :rtype out: dictionary
    :rtype err: dictionary
    """
    out = dict()
    out['raw'] = weibo
    out['mid'], out['isforward'], out['forwarduid'], out['forwardmid'] = parse_feed_info(weibo)
    out['nick'], out['uid'], out['weibo'] = parse_feed_content(weibo)  # user info and content of weibo
    out['datetime'], out['via'] = parse_feed_from(weibo)  # date time via
    out['forwards'], out['comments'], out['likes'] = parse_feed_action(weibo)  # number of forwards comments and likes
    return out


def parse_feed_info(soup):
    mid = soup.find(has_mid).attrs['mid']
    try:
        isforward = soup.find(has_isforward)['isforward']
        forward_content = soup.find('div', class_='comment')
        try:
            fr_uid = forward_content.find('div', class_='comment_info').div.a.attrs['usercard'].split('=')[1]
            fr_mid = forward_content.find('div', class_='feed_action clearfix W_fr') \
                .find_all('li')[2].a.attrs['action-data'].split('=')[1]
        except KeyError:
            isforward = u'9'
            fr_uid = ''
            fr_mid = ''
    except TypeError:
        isforward = u'0'
        fr_uid = ''
        fr_mid = ''
    return mid, isforward, fr_uid, fr_mid


def parse_feed_content(soup):
    feed_content = soup.find('div', class_='feed_content wbcon')
    user_info = feed_content.a.attrs
    nick = user_info['nick-name']
    uid = user_info['usercard'].split('&')[0].split('=')[1]
    weibo = parse_feed_content_weibo(feed_content.p)
    return nick, uid, weibo


def parse_feed_from(soup):
    try:
        feed_from = soup.find_all('div', class_='feed_from W_textb')[-1]
        datetime = feed_from.a.attrs['title']
        via = re.sub(u'.+? (来自|via) | +$|\n', '', feed_from.text)
    except IndexError:
        datetime = ''
        via = ''
    return datetime, via


def parse_feed_action(soup):
    try:
        feed_action = soup.find_all('div', 'feed_action clearfix')[-1].find_all('span', class_='line S_line1')
        forwards = re.sub(u'转发| |"', '', feed_action[1].text)
        comments = re.sub(u'评论| |"', '', feed_action[2].text)
        likes = feed_action[3].text
        n_forwards = u'0' if forwards == u'' else forwards
        n_comments = u'0' if comments == u'' else comments
        n_likes = u'0' if likes == u'' else likes
    except IndexError:
        n_forwards = u'0'
        n_comments = u'0'
        n_likes = u'0'
    return n_forwards, n_comments, n_likes


def parse_feed_content_weibo(weibo):
    """
    :type weibo: BeautifulSoup
    :rtype: str
    """
    content = ''
    for child in weibo.children:
        if type(child) == bs4.element.NavigableString:
            line = child.string.encode('unicode-escape')
            line = re.sub('\\\\[a-zA-Z0-9]{9}', '', line).decode('unicode-escape')  # remove emoji
            line = re.sub('"', '\\"', line)
            line = re.sub('\\\\', '', line)
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


def search_noresult(website):
    """
    :type website: str
    :rtype: bool
    """
    p = re.compile('<div class=\\\\"(.+?)\\\\">')
    return 'search_noresult' in p.findall(website)
