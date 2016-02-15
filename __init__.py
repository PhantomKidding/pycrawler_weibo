# -*- coding: utf-8 -*-

__all__ = ['WeiboLogin', 'WeiboDownloader', 'WeiboCrawler']

__author__ = 'Cheng Chen'
__email__ = 'cchen224@uic.edu'
__date__ = '20160214'



if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = 'cchenapp@gmail.com'  # '虫洞探索者'
    pwd = raw_input('请输入微博密码 >')
    keyword = '#百度#'

    WeiboLogin(username, pwd).login()
    WeiboCrawler(keyword, isConnectMySQL=True).crawl()
    print 'Finally!!'
