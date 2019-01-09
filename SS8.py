import requests
import re
import base64
import zxing
import json
import time
import subprocess

class SS8(object):
    def __init__(self, ssPath, ssConfigPath):
        self.ssConfigPath = ssConfigPath
        self.ssPath = ssPath
        self.headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                        }
        self.ss8_url = 'https://abc.ss8.fun/index.html'


    def get_html(self):
        try:
            res = requests.get(url = self.ss8_url, headers = self.headers)
        except:
            return False, 'Get SS8 Html Error.'

        pattern = re.compile('<a href="images(.+?)" class="image ">', re.S)
        item = re.findall(pattern, res.text)
        self.Singapore_url = 'https://abc.ss8.fun/images' + item[0]
        self.United_States_url = 'https://abc.ss8.fun/images' + item[1]
        self.Russia_url = 'https://abc.ss8.fun/images' + item[2]
        return True, 'Success'

    def get_code(self):

        for i in range(3):
            try:
                self.Singapore_code = requests.get(url = self.Singapore_url ,headers = self.headers)
            except:
                continue
            break
        # download code image
        with open('Singapore_code.jpg','wb') as f:
                f.write(self.Singapore_code.content)


        for i in range(3):
            try:
                self.United_States_code = requests.get(url = self.United_States_url ,headers = self.headers)
            except:
                continue
            break
        # download code image
        with open('United_States_code.jpg','wb') as f:
            f.write(self.United_States_code.content)


        for i in range(3):
            try:
                self.Russia_code = requests.get(url = self.Russia_url ,headers = self.headers)
            except:
                continue
            break
        # download code image
        with open('Russia_code.jpg','wb') as f:
            f.write(self.Russia_code.content) 


    # SS8 二维码解码
    def decode(self, mode):
        mode += '_code'
        reader = zxing.BarCodeReader()
        try:
            barcode = reader.decode("{}.jpg".format(mode))
        except:
            pass
        try:
            img_code = str(barcode)
            pattern = re.compile('\'ss(.+?)\'')
            ss_code = pattern.search(img_code).group(0)[1:-1]

            decode = str(base64.b64decode(ss_code))
            pattern = re.compile(r'aes-256-cfb:(.+?)@(.+?):(.+?)\\n')
            ss_code = re.findall(pattern, decode)

            self.password = ss_code[0][0].strip() # password
            self.address = ss_code[0][1].strip() # address
            self.port = ss_code[0][2].strip()  # port

        except:
            self.password = 'Error'
            self.address = 'Error'
            self.port = 'Error'

            #return self.password, self.address, self.port


    def write_decode(self):

        data = None
        with open(self.ssConfigPath, "r+") as f:
            data = json.load(f)
        data['configs'][0]['server'] = self.address
        data['configs'][0]['server_port'] = self.port
        data['configs'][0]['password'] = self.password
        data['configs'][0]['method'] = 'aes-256-cfb'
        data['configs'][0]['remarks'] = ('SS8-' + time.strftime('%m-%d %H:%M'))
        with open(self.ssConfigPath, "w") as f:
            json.dump(data, f, indent=4)

        subprocess.call('taskkill /f /im shadowsocks.exe', stdout=subprocess.PIPE)
        subprocess.Popen(self.ssPath)





if __name__ == '__main__':

    # SS程序路径
    ssPath = "H:\Shadowsocks\Shadowsocks.exe"
    # SS配置文件路径
    ssConfigPath = "H:\Shadowsocks\gui-config.json"

    ss8 = SS8(ssPath=ssPath, ssConfigPath=ssConfigPath)
    ss8.get_html()
    ss8.get_code()
    ss8.decode('United_States')
    print(ss8.password)
    ss8.write_decode()

