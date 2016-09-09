# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = raw_input('Input Weibo account >') 
    pwd = raw_input('Input password >')
    keywords = raw_input('Input what you want to search >')

    WeiboLogin(username, pwd).login()
    WeiboCrawler(isConnectMySQL=True, htmlOutputDir='/Users/cchen224/Downloads/weibo').search(keywords)
    print 'Finally!!'
