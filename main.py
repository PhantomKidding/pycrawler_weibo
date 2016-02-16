# -*- coding: utf-8 -*-


from crawler import WeiboCrawler
from login import WeiboLogin

if __name__ == '__main__':

    username = 'cchenapp@gmail.com'
    pwd = 'Cc19900201'
    keywords = ['#中国人寿#', '#中国人寿保险#', '#中国人寿保险公司#']

    WeiboLogin(username, pwd).login()
    WeiboCrawler(isConnectMySQL=True, htmlOutputDir='/Users/cchen224/Downloads/China Life').search(keywords)
    print 'Finally!!'
