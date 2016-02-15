# -*- coding: utf-8 -*-

import cookielib
import json
import re
import urllib2, time

import login_encode
from bs4 import BeautifulSoup


class WeiboLogin:

    def __init__(self, username, password, proxy=''):
        self._username = username
        self._password = password
        # self._nick = nick
        self._proxy = proxy

        self._serverUrl = 'http://login.sina.com.cn/sso/prelogin.php?' \
                          'entry=weibo&callback=sinaSSOController.preloginCallBack&su=&' \
                          'rsakt=mod&client=ssologin.js(v1.4.18)&_=1407721000736'
        self._loginUrl = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self._postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

        self._servertime = ''
        self._nonce = ''
        self._pubkey = ''
        self._rsakv = ''
        self._redirectLoginUrl = ''

    # create a cookie
    def enableCookie(self, proxy):
        cookieJar = cookielib.LWPCookieJar()  # build cookie
        cookieSupport = urllib2.HTTPCookieProcessor(cookieJar)
        if proxy == '':
            opener = urllib2.build_opener(cookieSupport, urllib2.HTTPHandler)
        else:
            proxySupport = urllib2.ProxyHandler({'http': proxy})  # 使用代理
            opener = urllib2.build_opener(proxySupport, cookieSupport, urllib2.HTTPHandler)
            print 'Proxy ', proxy,  ' enabled.'
        urllib2.install_opener(opener)

    # get server time and nonce
    def getServerData(self):
        print u'正在登录微博...',
        serverData = urllib2.urlopen(self._serverUrl).read()   # 获取网页内容
        try:
            # 在JSON中提取serverTime, nonce, pubkey, rsakv字段
            p = re.compile('\((.*)\)')
            jsonRaw = p.search(serverData).group(1)
            jsonData = json.loads(jsonRaw)
            servertime = str(jsonData['servertime'])   # 获取data中的相应字段，Json对象为一个字典
            nonce = jsonData['nonce']
            pubkey = jsonData['pubkey']
            rsakv = jsonData['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print u"\t失败."
            return None

    # Login中解析重定位结果部分函数
    def getRedirectLoginUrl(self, text):
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        loginUrl = p.search(text).group(1)
        return loginUrl

    def tryLogin(self):
        if self.isLoggedIn():
            print u'\t已登录!'
        else:
            self.enableCookie(self._proxy)
            self._servertime, self._nonce, self._pubkey, self._rsakv = self.getServerData()
            postData = login_encode.postEncode(self._username,
                                               self._password,
                                               self._servertime,
                                               self._nonce,
                                               self._pubkey,
                                               self._rsakv)
            # print "Getting postData success"
            req = urllib2.Request(self._loginUrl, postData, self._postHeader)   # 封装请求信息
            result = urllib2.urlopen(req)  # 登录第二步向self.loginUrl发送用户和密码
            text = result.read()  # 读取内容

            try:
                self._redirectLoginUrl = self.getRedirectLoginUrl(text)  # 得到重定位信息后，解析得到最终跳转到的URL
                urllib2.urlopen(self._redirectLoginUrl)  # 打开该URL后，服务器自动将用户登陆信息写入cookie，登陆成功
                return True if self.isRedirectLoginUrl(self._redirectLoginUrl) else False
            except:
                return False

    def login(self):
        print '\t登陆成功!\n' if self.tryLogin() else '\t登陆失败. T T'
        print '3秒后开始搜索...',
        time.sleep(1)
        print '1',
        time.sleep(1)
        print '2',
        time.sleep(1)
        print '3'

    def isRedirectLoginUrl(self, redirectLoginUrl):
        p = re.compile('retcode=[0-9]+')
        m = p.findall(redirectLoginUrl)
        if 'retcode=0' in m:
            return True
        else:
            print m
            return False

    def isLoggedIn(self):
        mainPage = 'http://s.weibo.com/'
        html = urllib2.urlopen(mainPage).read()

        # if self._nick == '':
        p = re.compile('\$CONFIG\[\'islogin\'\] = \'([0-9])\'')
        return p.search(html).group(1) == '1'
        # else:
        #     try:
        #         p = re.compile('\$CONFIG\[\'nick\'\] = \'(.+?)\'')
        #         return p.search(html).group(1) == self._nick
        #     except:
        #         return False