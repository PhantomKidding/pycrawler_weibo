# -*- coding: utf-8 -*-

import MySQLdb

from crawler import WeiboCrawler
from login import WeiboLogin

if __name__ == '__main__':
    # username = 'ericchen2436@gmail.com'
    # pwd = 'Cc19900201'
    # nick = '叉叉个叉叉'
    # keyword = '#工商银行#'
    # WeiboLogin.WeiboLogin(username, pwd, nick).login()


    username = 'cchenapp@gmail.com' #'虫洞探索者'
    pwd = 'Cc19900201'
    keyword = '#工商银行#'

    WeiboLogin(username, pwd).login()

    WeiboCrawler(keyword, pages=[37,38,39,40], isConnectMySQL=True).crawl()

    # downloader = WeiboCrawler(
    #     keyword,
    #     toMySQL=True,
    #     outputDir='/Users/cchen224/Downloads/tt',
    #     sleepTime=[10,30])
    # website = downloader.getSinglePage(1)
    # print 'downloaded'


    # conn = MySQLdb.connect(host='127.0.0.1',
    #                        user='root',
    #                        passwd='',
    #                        db='weibo',
    #                        port=3306,
    #                        charset='utf8mb4',
    #                        use_unicode=False)
    # print u'连入数据库'
    # weibos = WeiboDownloader('#百度#', 4, conn).load()
    # a = weibos.retrieve()
    # a[3]['raw']
    # analyzer = TopicAnalyzer(website).retrieve()
    # for a in analyzer._weibos:
    #     print a['mid']

    print 'Finally!!'

