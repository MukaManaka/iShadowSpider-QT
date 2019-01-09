# -*- coding: utf-8 -*-
import re
import subprocess
import json
import time
import requests



headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}



class ShadowSocks(object):
    def __init__(self, ssPath, ssConfigPath, url):
        self.url = url
        self.ssPath = ssPath
        self.headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                        }
        self.ssConfigPath = ssConfigPath
        #self.getHtml()

    # 获取页面内容
    def getHtml(self):

        try:
            res = requests.get(url=self.url, headers=headers, verify=False)
            if res.status_code == 200:
                res.encoding = 'utf-8'
                self.content = res.text
                return (True, 'Success')
            else:
                return (False, 'iShadow网页拒绝访问 T_T ' + res)
        except:
            return (False, 'iShadow网页Get方法失败 O_O')

    # 获取服务器内容
    def printItem(self, pattern):

        if pattern == 'Japan A': pattern = JapanA_pattern
        if pattern == 'Japan B': pattern = JapanB_pattern
        if pattern == 'Japan C': pattern = JapanC_pattern
        if pattern == 'Singapore A': pattern = SingaporeA_pattern
        if pattern == 'Singapore B': pattern = SingaporeB_pattern
        if pattern == 'Singapore C': pattern = SingaporeC_pattern
        if pattern == 'Usa A': pattern = UsaA_pattern
        if pattern == 'Usa B': pattern = UsaB_pattern
        if pattern == 'Usa C': pattern = UsaC_pattern

        try:
            item = re.findall(pattern, self.content)[0]
            #print(item)
            print('服务器  :', item[0].strip())
            print('端口    :', item[1].strip())
            print('密码    :', item[2].strip())
            print('加密方式:', item[3].strip())
            print('===================================')
        except:
            item = 'iShadow网页正则表达式抓取失败'
        return item

    # 设置服务器
    def setShadowSocks(self, pattern):

        if pattern == 'Japan A': pattern = JapanA_pattern
        if pattern == 'Japan B': pattern = JapanB_pattern
        if pattern == 'Japan C': pattern = JapanC_pattern
        if pattern == 'Singapore A': pattern = SingaporeA_pattern
        if pattern == 'Singapore B': pattern = SingaporeB_pattern
        if pattern == 'Singapore C': pattern = SingaporeC_pattern
        if pattern == 'Usa A': pattern = UsaA_pattern
        if pattern == 'Usa B': pattern = UsaB_pattern
        if pattern == 'Usa C': pattern = UsaC_pattern

        
        item = re.findall(pattern, self.content)[0]
        server = item[0].strip()
        server_port = item[1].strip()
        password = item[2].strip()
        method = item[3].strip()


        data = None
        with open(self.ssConfigPath, "r+") as f:
            data = json.load(f)
        data['configs'][0]['server'] = server
        data['configs'][0]['server_port'] = server_port
        data['configs'][0]['password'] = password
        data['configs'][0]['method'] = method
        data['configs'][0]['remarks'] = ('ishadow-' + time.strftime('%m-%d %H:%M'))
        with open(self.ssConfigPath, "w") as f:
            json.dump(data, f, indent=4)

        subprocess.call('taskkill /f /im shadowsocks.exe', stdout=subprocess.PIPE)
        subprocess.Popen(self.ssPath)
            


##################################################
##    基本变量
##################################################



# 匹配日本服务器的模式
JapanA_pattern = re.compile(
    r'<span id="ipjpa">(.+?)</span>.+<h4>Port:<span id="portjpa">(.+?)</span>.+<span id="pwjpa">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
JapanB_pattern = re.compile(
    r'<span id="ipjpb">(.+?)</span>.+<h4>Port:<span id="portjpb">(.+?)</span>.+<span id="pwjpb">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
JapanC_pattern = re.compile(
    r'<span id="ipjpc">(.+?)</span>.+<h4>Port:<span id="portjpc">(.+?)</span>.+<span id="pwjpc">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)

# 匹配新加坡服务器的模式
SingaporeA_pattern = re.compile(
    r'<span id="ipsga">(.+?)</span>.+<h4>Port:<span id="portsga">(.+?)</span>.+<span id="pwsga">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
SingaporeB_pattern = re.compile(
    r'<span id="ipsgb">(.+?)</span>.+<h4>Port:<span id="portsgb">(.+?)</span>.+<span id="pwsgb">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
SingaporeC_pattern = re.compile(
    r'<span id="ipsgc">(.+?)</span>.+<h4>Port:<span id="portsgc">(.+?)</span>.+<span id="pwsgc">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)

# 匹配美国服务器的模式
UsaA_pattern = re.compile(
    r'<span id="ipusa">(.+?)</span>.+<h4>Port:<span id="portusa">(.+?)</span>.+<span id="pwusa">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
UsaB_pattern = re.compile(
    r'<span id="ipusb">(.+?)</span>.+<h4>Port:<span id="portusb">(.+?)</span>.+<span id="pwusb">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)
UsaC_pattern = re.compile(
    r'<span id="ipusc">(.+?)</span>.+<h4>Port:<span id="portusc">(.+?)</span>.+<span id="pwusc">(.+?)</span>.+<h4>Method:(.+?)</h4>', re.S)

if __name__ == '__main__':

    # SS程序路径
    ssPath = "H:\Shadowsocks\Shadowsocks.exe"
    # SS配置文件路径
    ssConfigPath = "H:\Shadowsocks\gui-config.json"
    url = 'https://a.ishadowx.net/'


    a = ShadowSocks(ssPath, ssConfigPath ,url)
    
    # print(a.getHtml())

    a.printItem(pattern=JapanA_pattern)
    a.printItem(pattern=JapanB_pattern)
    a.printItem(pattern=JapanC_pattern)
    a.printItem(pattern=SingaporeA_pattern)
    a.printItem(pattern=SingaporeB_pattern)
    a.printItem(pattern=SingaporeC_pattern)
    a.printItem(pattern=UsaA_pattern)
    a.printItem(pattern=UsaB_pattern)
    a.printItem(pattern=UsaC_pattern)
