# -*- coding: utf-8 -*-

__all__ = ['WeiboLogin', 'WeiboDownloader', 'WeiboCrawler', 'SearchParser']

__author__ = 'Cheng Chen'
__email__ = 'cchen224@uic.edu'
__date__ = '20160214'



if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = raw_input('请输入微博账号 >')
    pwd = raw_input('请输入微博密码 >')
    keywords = raw_input('请输入查询关键词 >')

    WeiboLogin(username, pwd).login()
    WeiboCrawler(isConnectMySQL=True, htmlOutputDir='/Users/cchen224/Downloads/weibo').search(keywords, pages=[1, 2])
    print 'Finally!!'
