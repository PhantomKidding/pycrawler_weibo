# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from crawler import WeiboCrawler
    from login import WeiboLogin

    username = raw_input('请输入微博账号 >')
    pwd = raw_input('请输入微博密码 >')
    keywords = raw_input('请输入查询关键词 >')

    WeiboLogin(username, pwd).login()
    WeiboCrawler(isConnectMySQL=True, htmlOutputDir='/Users/cchen224/Downloads/weibo').search(keywords)
    print 'Finally!!'
