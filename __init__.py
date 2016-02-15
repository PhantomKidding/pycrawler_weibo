# -*- coding: utf-8 -*-


__all__ = ['WeiboLogin', 'WeiboDownloader', 'WeiboCrawler']


if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = 'cchenapp@gmail.com'  # '虫洞探索者'
    pwd = raw_input('请输入微博密码 >')
    keyword = '#百度#'

    WeiboLogin(username, pwd).login()
    WeiboCrawler(keyword, isConnectMySQL=True).crawl()
    print 'Finally!!'
