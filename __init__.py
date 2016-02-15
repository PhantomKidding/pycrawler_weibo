# -*- coding: utf-8 -*-

__all__ = ['WeiboLogin', 'WeiboDownloader', 'WeiboCrawler', 'TopicParser']

__author__ = 'Cheng Chen'
__email__ = 'cchen224@uic.edu'
__date__ = '20160214'



if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = 'cchenapp@gmail.com'  # '虫洞探索者'
    pwd = raw_input('请输入微博密码 >')
    keyword = '#谷歌#'

    WeiboLogin(username, pwd).login()
    WeiboCrawler(keyword, pages=range(29,52), isConnectMySQL=True, htmlOutputDir='/Users/cchen224/Downloads/weibo').crawl()
    print 'Finally!!'
