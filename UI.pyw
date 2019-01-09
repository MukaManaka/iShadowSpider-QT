# -*- coding: utf-8 -*-
from iShadow import *
from SS8 import *
import threading
import re
import sys
import os
import PyQt5.sip
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit,
                            QHBoxLayout, QVBoxLayout, QLabel, QComboBox, 
                            QDesktopWidget,QMainWindow,QInputDialog)






class Windows(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_para()
        self.config()
        self.initUI()

    def init_para(self):
        self.Ready = False
        self.spider_status = False  
        self.mode = 'iShadow'  # 系统初始状态

    # 参数配置
    def config(self):
        self.ssPath = r"H:\Shadowsocks\Shadowsocks.exe"
        self.ssConfigPath = r"H:\Shadowsocks\gui-config.json"

        

    def initUI(self):
        #设置中心控件QWidegt
        self.QWidegt = QWidget()
        self.setCentralWidget(self.QWidegt)
        #状态栏
        #self.statusBar().showMessage('Reday')
        
        #按钮
        searchButton = QPushButton('Search')
        settingButton = QPushButton('Setting')
        okButton = QPushButton("Write", self)
        cancelButton = QPushButton("Clear", self)
        loadButton = QPushButton('Load Web')
        # pathButton = QPushButton('Path')
        self.modeButton = QPushButton('iShadow')
        #文本框    
        self.label = QLabel('', self)
        #self.lbl.setText(text)
        
        #下拉列表
        self.combo = QComboBox(self)
        self.combo_set()

        #创建一个垂直布局
        hbox_up_left = QVBoxLayout()
        hbox_up_left.addWidget(self.label)
        
        #创建一个垂直布局
        hbox_up_right = QVBoxLayout()
        hbox_up_right.addWidget(settingButton)
        hbox_up_right.addWidget(loadButton)
        #hbox_up_right.addWidget(pathButton)
        hbox_up_right.addWidget(self.modeButton)        
        hbox_up_right.addStretch(1)

        #创建一个水平布局
        vbox_up = QHBoxLayout()
        vbox_up.addLayout(hbox_up_left)
        vbox_up.addStretch(1)
        vbox_up.addLayout(hbox_up_right)
        
        #创建一个水平布局
        vbox_down = QHBoxLayout()
        vbox_down.addWidget(self.combo)
        vbox_down.addStretch(1)
        vbox_down.addWidget(searchButton)
        vbox_down.addWidget(okButton)
        vbox_down.addWidget(cancelButton)
        #创建一个垂直布局
        mainbox = QVBoxLayout()
        mainbox.addLayout(vbox_up)
        mainbox.addLayout(vbox_down)
        #设置窗口的布局界面
        self.QWidegt.setLayout(mainbox)

        #信号
        searchButton.clicked.connect(self.search)
        okButton.clicked.connect(self.write)
        cancelButton.clicked.connect(self.clean)
        settingButton.clicked.connect(self.setting)
        loadButton.clicked.connect(self.load_web)
        # pathButton.clicked.connect(self.path)
        self.modeButton.clicked.connect(self.mode_press)
        #self.combo.activated[str].connect(self.onActivated)

        
        #窗口设置
        self.resize(300, 150)
        self.center() 
        self.setWindowTitle('Shadow v0.5')    
        self.setWindowIcon(QIcon('icon.png'))        
        self.show()
        
    def center(self):  
        # 得到主窗体的框架信息  
        qr = self.frameGeometry()  
        # 得到桌面的中心  
        cp = QDesktopWidget().availableGeometry().center()  
        # 框架的中心与桌面中心对齐  
        qr.moveCenter(cp)  
        # 自身窗体的左上角与框架的左上角对齐  
        self.move(qr.topLeft())  

        
    def search(self):
        if self.Ready :
            if self.mode == 'iShadow':
                item = shadowsocks.printItem(pattern=self.combo.currentText())
                if type(item) != str:
                    self.label.setText('服务器  :{} \n端口    :{}\n密码    :{}\n加密方式:{}'.format(item[0].strip(),item[1].strip(),item[2].strip(),item[3].strip()))
                else:
                    self.label.setText(item)

            elif self.mode == 'SS8':
                self.label.setText('服务器  :{} \n端口    :{}\n密码    :{}\n加密方式:aes-256-cfb'.format(ss8.address, ss8.port, ss8.password))

        else:
            self.label.setText('Not Ready To Search.')

    def clean(self):
        self.label.setText('')
        if(os.path.exists('Singapore_code.jpg')): os.remove("Singapore_code.jpg")
        if(os.path.exists('United_States_code.jpg')): os.remove("United_States_code.jpg")
        if(os.path.exists('Russia_code.jpg')): os.remove("Russia_code.jpg")

    def write(self):
        if self.Ready :
            if self.mode == 'iShadow':
                shadowsocks.setShadowSocks(pattern=self.combo.currentText())
                #self.statusBar().showMessage('Success')

            if self.mode == 'SS8':
                if ss8.password != 'Error':
                    ss8.write_decode()
                else:
                    print('SS8 write Error')  
        else:
            self.label.setText('Not Ready To Write.')

    '''
    def path(self):
        text = 'H:\\Shadowsocks\\'
        path,ok = QInputDialog.getText(self, "Path Setting","Shadowsocks Path:",text=text)
        if ok:
            if path[-1] != '\\': path += '\\' 
            self.ssPath = path + 'Shadowsocks.exe'
            self.ssConfigPath + 'gui-config.json'
            self.label.setText('成功修改了路径: \n' + path)
            
        else:
            self.label.setText('木有修改路径...')
    '''

    def setting(self):
        url_1 = 'http://my.ishadowx.net/'
        url_2 = 'http://ss.ishadowx.net/'
        url_3 = 'https://us.ishadowx.net/'
        url_4 = 'https://a.ishadowx.net/'
        items = [url_1, url_2, url_3, url_4]
        url_item,ok = QInputDialog.getItem(self, "Url Setting","iShadow Url:", items)
        if ok:
            shadowsocks.url = url_item
            self.label.setText('成功修改了一次设定 >_<')
            self.change = True
        else:
            self.label.setText('成功取消了一次设定...')

    def load_web(self):
        if self.mode == 'iShadow':
            self.label.setText('正在初始化iShadow')
            self.spider_thread = SpiderThread(self)
            self.spider_thread.mode = 'iShadow'
            self.spider_thread.start()
            self.spider_thread.trigger.connect(self.spider_launched)

        elif self.mode == 'SS8':
            self.label.setText('正在初始化SS8')
            self.spider_thread = SpiderThread()
            self.spider_thread.mode = 'SS8'
            self.spider_thread.start()
            self.spider_thread.trigger.connect(self.spider_launched)


    def mode_press(self):
        if self.mode == 'iShadow':
            self.label.setText('Mode Changed:  SS8')
            self.modeButton.setText('SS8')
            self.mode = 'SS8'
        elif self.mode == 'SS8':
            self.label.setText('Mode Changed:  iShadow')
            self.modeButton.setText('iShadow')
            self.mode = 'iShadow'
        self.combo_set()


    def spider_launched(self):
        self.spider_status = self.spider_thread.result
        self.label.setText(str(self.spider_status[0]) + '\n' + self.spider_status[1])
        if self.spider_status[0]:
            self.Ready = True

        if self.mode == 'iShadow':
            pass

        if self.mode == 'SS8':
            ss8.get_code()
            ss8.decode(self.combo.currentText())

    def combo_set(self):
        if self.mode == 'SS8':
            self.combo.clear()
            self.combo.addItem("Singapore")
            self.combo.addItem("United_States")
            self.combo.addItem("Russia")
        elif self.mode == 'iShadow':
            self.combo.clear()
            self.combo.addItem("Singapore A")
            self.combo.addItem("Singapore B")
            self.combo.addItem("Singapore C")
            self.combo.addItem("Usa A")
            self.combo.addItem("Usa B")
            self.combo.addItem("Usa C")

class SpiderThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super().__init__()

 
    def run(self):
        if  self.mode == 'iShadow':
            self.result = shadowsocks.getHtml()
        elif self.mode == 'SS8':
            self.result = ss8.get_html()
        self.trigger.emit()         #完毕后发出信号




# SS程序路径
ssPath = "H:\Shadowsocks\Shadowsocks.exe"
# SS配置文件路径
ssConfigPath = "H:\Shadowsocks\gui-config.json"


if __name__ == '__main__':
    url = 'https://b.ishadowx.net/'
    shadowsocks = ShadowSocks(ssPath=ssPath, ssConfigPath=ssConfigPath, url=url)
    ss8 = SS8(ssPath=ssPath, ssConfigPath=ssConfigPath)   

    import cgitb 
    cgitb.enable(format = 'text')

    app = QApplication(sys.argv)
    ex = Windows()
    sys.exit(app.exec_())  






    
