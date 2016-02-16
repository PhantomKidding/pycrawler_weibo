# -*- coding: utf-8 -*-
import urllib
import base64
import rsa
import binascii


# 获取用户名和密码加密后的形式，封装成发送数据的数据包返回
def post_encode(username, password, serverTime, nonce, pubkey, rsakv):
    encodedUsername = get_username(username)  # 用户名使用base64加密
    encodedPassword = get_password(password, serverTime, nonce, pubkey)  # 目前密码采用rsa加密
    postPara = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'ssosimplelogin': '1',
            'vsnf': '1',
            'vsnval': '',
            'su': encodedUsername,
            'service': 'miniblog',
            'servertime': serverTime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'sp': encodedPassword,
            'encoding': 'UTF-8',
            'prelt': '115',
            'rsakv': rsakv,
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
            }
    postData = urllib.urlencode(postPara)  # 封装postData信息并返回
    return postData


# 根据明文的用户名信息获取加密后的用户名
def get_username(username):
    return base64.encodestring(urllib.quote(username))[:-1]


# 根据明文的密码信息加入nonce和pubkey后根据rsa加密算法的规则生成密码的密文
def get_password(password, servertime, nonce, pubkey):
    rsa_pubkey = int(pubkey, 16)
    key = rsa.PublicKey(rsa_pubkey, 65537)  # 创建公钥
    msg = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文加密文件中得到
    pwd = rsa.encrypt(msg, key)  # 加密
    pwd = binascii.b2a_hex(pwd)  # 将加密信息转换为16进制。
    return pwd
