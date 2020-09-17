import sys
import os
import requests
from lxml import etree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# class Newthread(QtCore.QThread):
#     def __init__(self):
#         super(Runthread,self).__init__()
#     def __del__(self):
#         self.wait()
#     def run(self):


class DownMusic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.StartGui()

    def StartDown(self):
        if (self.input1.text() == ''):
            pass
        else:
            url = self.input1.text()
            headers = {'user-agent': 'my-app/0.0.1'}
            if "playlist" in url:
                if "?userid=" in url:
                    position1 = url.find("playlist/")
                    position2 = url.find("/?userid=")
                    id = url[position1 + 9:position2]
                elif '&' in url:
                    position1 = url.find("?id=")
                    position2 = url.find("&")
                    id = url[position1 + 4:position2]
                else:
                    position = url.find("id=")
                    id = url[position + 3:]
                playlist_url = "https://music.163.com/playlist?id=" + id
                result = requests.get(playlist_url, headers=headers).text
                dom = etree.HTML(result)
                ids = dom.xpath('//a[contains(@href,"song?")]/@href')
                title = dom.xpath('//meta[@property="og:title"]/@content')
                if title:
                    true_title = title[0]
                else:
                    true_title = 'Error'
                print(true_title)
                self.text.setText(true_title)
                if (self.input2.text() == ''):
                    path = "D:\\MusicDownload\\" + true_title
                else:
                    path = self.input2.text() + '\\' + true_title
                    while ('/' in path):
                        position = path.find('/')
                        path = path[:position] + '\\' + path[position + 1:]
                print(path)
                if (os.path.exists(path)):
                    pass
                else:
                    os.makedirs(path)
                for id in ids:
                    if '$' not in id:
                        id = id[9:]
                        true_url = "https://music.163.com/song?id=" + id
                        down_url = "http://music.163.com/song/media/outer/url?id=" + id + ".mp3"
                        result = requests.get(true_url, headers=headers).text
                        dom = etree.HTML(result)
                        name = dom.xpath(
                            '//meta[@property="og:title"]/@content')
                        if name:
                            song_name = name[0]
                        else:
                            song_name = 'Error'
                        album = dom.xpath(
                            '//meta[@property="og:music:album"]/@content')
                        if album:
                            song_album = album[0]
                        else:
                            song_album = 'Error'
                        artist = dom.xpath(
                            '//meta[@property="og:music:artist"]/@content')
                        if artist:
                            song_artist = artist[0]
                        else:
                            song_artist = 'Error'
                        self.text.insertPlainText("歌名:" + song_name)
                        self.text.insertPlainText('\n')
                        self.text.insertPlainText("歌手:" + song_artist)
                        self.text.insertPlainText('\n')
                        self.text.insertPlainText("专辑:" + song_album)
                        self.text.insertPlainText('\n')

                        music = requests.get(down_url, headers=headers).content
                        file_name = song_name + '-' + song_artist + ".mp3"
                        true_path = path + '\\' + file_name
                        try:
                            with open(true_path, 'wb') as file:
                                file.write(music)
                        except:
                            self.text.insertPlainText("下载失败")
                            self.text.insertPlainText('\n')
                        else:
                            self.text.insertPlainText("下载成功")
                            self.text.insertPlainText('\n')
            else:
                if "?userid=" in url:
                    position1 = url.find("song/")
                    position2 = url.find("/?userid=")
                    id = url[position1 + 5:position2]
                elif '&' in url:
                    position1 = url.find("?id=")
                    position2 = url.find("&")
                    id = url[position1 + 4:position2]
                else:
                    position = url.find("id=")
                    id = url[position + 3:]
                    true_url = "https://music.163.com/song?id=" + id
                    print(true_url)
                    down_url = "http://music.163.com/song/media/outer/url?id=" + id + ".mp3"
                    print(down_url)
                    result = requests.get(true_url, headers=headers).text
                    dom = etree.HTML(result)
                    name = dom.xpath('//meta[@property="og:title"]/@content')
                    print(name)
                    if name:
                        song_name = name[0]
                    else:
                        song_name = 'Error'

                    album = dom.xpath(
                        '//meta[@property="og:music:album"]/@content')
                    if album:
                        song_album = album[0]
                    else:
                        song_album = 'Error'
                    artist = dom.xpath(
                        '//meta[@property="og:music:artist"]/@content')
                    if artist:
                        song_artist = artist[0]
                    else:
                        song_artist = 'Error'
                    self.text.insertPlainText("歌名:" + song_name)
                    self.text.insertPlainText('\n')
                    self.text.insertPlainText("歌手:" + song_artist)
                    self.text.insertPlainText('\n')
                    self.text.insertPlainText("专辑:" + song_album)
                    self.text.insertPlainText('\n')
                    music = requests.get(down_url, headers=headers).content
                    file_name = song_name + '-' + song_artist + ".mp3"
                    if (self.input2.text() == ''):
                        path = "D:\\MusicDownload\\"
                    else:
                        path = self.input2.text()
                        while ('/' in path):
                            position = path.find('/')
                            path = path[:position] + '\\' + path[position + 1:]
                    print(path)
                    if (os.path.exists(path)):
                        pass
                    else:
                        os.makedirs(path)
                    true_path = path + '\\' + file_name
                    try:
                        with open(true_path, 'wb') as file:
                            file.write(music)
                    except:
                        self.text.insertPlainText("下载失败")
                        self.text.insertPlainText('\n')
                    else:
                        self.text.insertPlainText("下载成功")
                        self.text.insertPlainText('\n')

    def SelectPath(self):
        path = QFileDialog.getExistingDirectory(self, '选取文件夹', './')
        self.input2.setText(path)

    def StartGui(self):
        #启动界面
        def screencenter():
            # 屏幕居中
            desktop = QApplication.desktop()
            screenrect = desktop.screenGeometry()
            scr_w = screenrect.width()
            scr_h = screenrect.height()
            cen_w = (scr_w - 1024) / 2
            cen_h = (scr_h - 768) / 2
            return cen_w, cen_h

        def AboutUs():
            # 关于
            MsgBox = QMessageBox(
                QMessageBox.NoIcon, '关于我们',
                '这只是一个用来方便下载的工具\n\npowered by Nobilta \nVersion:1.0')
            MsgBox.exec()

        def Help():
            Msgbox = QMessageBox(
                QMessageBox.NoIcon, '帮助',
                '复制一个网易云的单曲或者歌单，粘贴到工具中，直接下载，默认路径为D:\\MusicDownload(-歌单名) ')
            Msgbox.exec()

        w, h = screencenter()
        # 背景图片
        palette = QtGui.QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))
        # 菜单栏
        aboutAct = QAction('关于我们', self)
        aboutAct.triggered.connect(AboutUs)
        helpAct = QAction('使用帮助', self)
        helpAct.triggered.connect(Help)
        menuBar = self.menuBar()
        aboutMenu = menuBar.addMenu('关于')
        aboutMenu.addAction(aboutAct)
        aboutMenu.addAction(helpAct)
        # 文字标签
        self.lb1 = QLabel("请输入网易云音乐(歌单)链接:", self)
        self.lb1.setStyleSheet('color:#696969')
        self.lb1.setFont(QFont("微软雅黑", 16))
        self.lb1.resize(350, 35)
        self.lb1.move(18, 32)
        # 输入框
        self.input1 = QLineEdit(self)
        self.input1.resize(700, 30)
        self.input1.move(18, 85)
        self.input1.setPlaceholderText("请输入链接")
        self.input1.setStyleSheet(
            "background:transparent;border-width:0;border-style:outset;color:#696969;font-style:italic"
        )
        self.input1.setFont(QFont("Arial", 14))
        self.lb2 = QLabel(
            "___________________________________________________________________________________________________________________________",
            self)
        self.lb2.setStyleSheet("color:#696969")
        self.lb2.resize(700, 12)
        self.lb2.move(18, 104)
        # 按钮
        self.bt1 = QPushButton("下载", self)
        self.bt1.move(740, 90)
        self.bt1.resize(60, 30)
        self.bt1.setFont(QFont("微软雅黑", 10))
        self.bt1.setStyleSheet(
            "background:#7ccee3;color:white;border-radius:15px")
        self.bt1.clicked.connect(self.StartDown)
        # 显示框
        self.text = QTextBrowser(self)
        self.text.resize(800, 450)
        self.text.move(112, 170)
        self.text.setFont(QFont("微软雅黑", 14))
        self.text.setStyleSheet(
            "background:transparent;color:#696969;border-color:#696969")
        # 设置路径
        self.input2 = QLineEdit(self)
        self.input2.resize(630, 30)
        self.input2.move(200, 665)
        self.input2.setFont(QFont("Arial", 14))
        self.input2.setStyleSheet(
            "background:transparent;color:#696969;border-width:0;border-style:outset"
        )
        self.lb3 = QLabel("选择路径：", self)
        self.lb3.resize(85, 30)
        self.lb3.move(105, 665)
        self.lb3.setFont(QFont("微软雅黑", 15))
        self.lb3.setStyleSheet("color:#696969")
        self.lb4 = QLabel(
            "___________________________________________________________________________________________________________",
            self)
        self.lb4.resize(630, 12)
        self.lb4.move(200, 682)
        self.lb4.setStyleSheet("color:#696969")
        self.bt2 = QPushButton("选择", self)
        self.bt2.resize(60, 30)
        self.bt2.move(843, 670)
        self.bt2.setFont(QFont("微软雅黑", 10))
        self.bt2.setStyleSheet(
            "background:#7ccee3;color:white;border-radius:15px")
        self.bt2.clicked.connect(self.SelectPath)
        # 初始化
        self.setPalette(palette)
        self.setGeometry(w, h, 1024, 768)
        self.setFixedSize(1024, 768)
        self.setWindowTitle('网易云下载工具V1.0')
        self.setWindowIcon(QIcon('ico.png'))
        self.setAutoFillBackground(True)
        self.text.setText("准备就绪")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = DownMusic()
    sys.exit(app.exec_())
