import sys
import os
import requests
import base64
from lxml import etree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QRadioButton, QFileDialog, QLabel, QMainWindow, QApplication, QPushButton, QTextBrowser, QLineEdit, QAction, QMessageBox, QMenuBar
from PyQt5.QtCore import QThread, pyqtSignal
from bg_jpg import img as bg
from ico_jpg import img as ico

tmp = open('bg.jpg', 'wb')
tmp.write(base64.b64decode(bg))
tmp.close()
tmp = open('ico.jpg', 'wb')
tmp.write(base64.b64decode(ico))
tmp.close()


class Downthread(QtCore.QThread):
    signal = pyqtSignal(str)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    def __init__(self, url, path, platform):
        super(Downthread, self).__init__()
        self.url = url
        self.path = path
        self.platform = platform
        self.status = True

    def __del__(self):
        self.wait()

    def get_FileSize(self, filePath):
        #获取文件大小
        fsize = os.path.getsize(filePath)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 2)

    def run(self):
        def downloadfunction(url, path):
            #下载
            music = requests.get(url, headers=self.headers).content
            if (self.status == True):
                try:
                    with open(path, 'wb') as file:
                        file.write(music)
                except:
                    self.signal.emit('下载失败\n')
                else:
                    size = self.get_FileSize(path)
                    if (size > 0.1):
                        self.signal.emit('下载成功\n')
                    else:
                        self.signal.emit('无法下载\n')
                        os.remove(path)

        def downloadpath(path, file_name):
            #文件路径
            file_name=file_name.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                                        .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
            path = path.replace('/', '\\')
            if path == '':
                path = "D:\\MusicDownload"
            if (os.path.exists(path)):
                pass
            else:
                os.makedirs(path)
            path = path + '\\' + file_name + '.mp3'
            return path

        def kuwo(url):
            #kuwo
            def down(url):
                position = url.find('detail/')
                id = url[position + 7:]
                result = requests.get(url, headers=self.headers).text
                dom = etree.HTML(result)
                song_name = dom.xpath('//input[@id="songinfo-name"]/@value')
                if song_name:
                    song_name = song_name[0]
                else:
                    song_name = 'Error'
                song_artist = dom.xpath('//span[@class="name"]/text()')
                if song_artist:
                    song_artist = song_artist[1]
                else:
                    song_artist = '未知'
                song_album = dom.xpath(
                    '//span[@class="tip album_name"]/text()')
                if song_album:
                    song_album = song_album[0]
                else:
                    song_album = '未知'
                # self.signal.emit('Clear now')
                self.signal.emit("歌名:" + song_name)
                self.signal.emit("歌手:" + song_artist)
                self.signal.emit("专辑:" + song_album)
                file_name = song_name + '-' + song_artist
                path = downloadpath(self.path, file_name)
                # print(path)
                down_url = 'http://antiserver.kuwo.cn/anti.s?useless=' + '/resource' + '&format=mp3&rid=MUSIC_' + id + '&response=res&type=convert_url&'
                downloadfunction(down_url, path)
                # self.signal.emit('finished')            
            if 'playlist' in url:
                pass
            else:
                self.signal.emit('Clear now')
                down(url)
                self.signal.emit('finished')
                
            

        def wangyi(url):
            def down(url):
                if "?userid=" in url:
                    position1 = url.find("song/")
                    position2 = url.find("/?userid=")
                    id = self.url[position1 + 5:position2]
                elif '&' in self.url:
                    position1 = url.find("?id=")
                    position2 = url.find("&")
                    id = url[position1 + 4:position2]
                else:
                    position = url.find("id=")
                    id = url[position + 3:]
                print(id)
                url = "https://music.163.com/song?id=" + id
                down_url = "http://music.163.com/song/media/outer/url?id=" + id + ".mp3"
                result = requests.get(url, headers=self.headers).text
                dom = etree.HTML(result)
                name = dom.xpath('//meta[@property="og:title"]/@content')
                if name:
                    name = name[0]
                else:
                    name = 'Error'
                album = dom.xpath(
                    '//meta[@property="og:music:album"]/@content')
                if album:
                    album = album[0]
                else:
                    album = 'Error'
                artist = dom.xpath(
                    '//meta[@property="og:music:artist"]/@content')
                if artist:
                    artist = artist[0]
                else:
                    artist = 'Error'
                if (name == 'Error' and artist == 'Error'):
                    self.signal.emit("解析失败\n")
                else:
                    self.signal.emit("歌名:" + name)
                    self.signal.emit("歌手:" + artist)
                    self.signal.emit("专辑:" + album)
                    # song_name=song_name.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                    #                 .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                    # song_artist=song_artist.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                    #                 .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                    # file_name = song_name + '-' + song_artist + ".mp3"
                    # while ('/' in file_name):
                    #     position = file_name.find('/')
                    #     file_name = file_name[:position] + ' ' + file_name[
                    #         position + 1:]
                    # if (self.path == ''):
                    #     self.path = "D:\\MusicDownload\\"
                    # else:
                    #     while ('/' in self.path):
                    #         position = self.path.find('/')
                    #         self.path = self.path[:position] + '\\' + self.path[
                    #             position + 1:]
                    file_name=name+'-'+artist
                    path = downloadpath(self.path,file_name)
                    downloadfunction(down_url,path)
                    # if (os.path.exists(path)):
                    #     pass
                    # else:
                    #     os.makedirs(path)
                    # music = requests.get(down_url,
                    #                      headers=self.headers).content
                    # true_path = self.path + '\\' + file_name
                    # try:
                    #     with open(true_path, 'wb') as file:
                    #         file.write(music)
                    # except:
                    #     self.signal.emit('下载失败\n\n')
                    # else:
                    #     size = self.get_FileSize(true_path)
                    #     if (size > 0.1):
                    #         self.signal.emit('下载成功\n\n')
                    #     else:
                    #         self.signal.emit('无法下载\n\n')
                    #         os.remove(true_path)
                # self.signal.emit('have finished')


            if "playlist" in self.url:
                if "?userid=" in self.url:
                    position1 = self.url.find("playlist/")
                    position2 = self.url.find("/?userid=")
                    id = self.url[position1 + 9:position2]
                elif '&' in self.url:
                    position1 = self.url.find("?id=")
                    position2 = self.url.find("&")
                    id = self.url[position1 + 4:position2]
                else:
                    position = self.url.find("id=")
                    id = self.url[position + 3:]
                playlist_url = "https://music.163.com/playlist?id=" + id
                result = requests.get(playlist_url, headers=self.headers).text
                dom = etree.HTML(result)
                ids = dom.xpath('//a[contains(@href,"song?")]/@href')
                cot=dom.xpath('//span[@id="playlist-track-count"]/text()')
                cot=int(cot[0])
                title = dom.xpath('//meta[@property="og:title"]/@content')
                if title:
                    title = title[0]
                else:
                    title = 'Error'
                self.signal.emit("Clear now")
                self.signal.emit(title)
                title=title.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                                    .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                if (self.path == ''):
                    self.path = "D:\\MusicDownload\\" + title
                else:
                    self.path = self.path + '\\' + title
                self.signal.emit('当前歌单共计%d首\n' % (cot))
                for id in ids:
                    if (self.status == True):
                        if '$' not in id:
                            id = id[9:]
                            url = "https://music.163.com/song?id=" + id
                            print(url) 
                            down(url)     
                            cot = cot - 1
                            self.signal.emit('剩余%d首\n' % (cot))
                            if (cot == 0):
                                self.signal.emit("have finished")
                    else:
                        self.signal.emit('下载已停止\n')
                        break          
            else:
                self.signal.emit('Clear now')
                down(url)
                self.signal.emit('finished')
        if self.platform == 'kuwo':
            kuwo(self.url)
        if self.platform == 'wangyi':
            wangyi(self.url)
            # if "playlist" in self.url:
            #     if "?userid=" in self.url:
            #         position1 = self.url.find("playlist/")
            #         position2 = self.url.find("/?userid=")
            #         id = self.url[position1 + 9:position2]
            #     elif '&' in self.url:
            #         position1 = self.url.find("?id=")
            #         position2 = self.url.find("&")
            #         id = self.url[position1 + 4:position2]
            #     else:
            #         position = self.url.find("id=")
            #         id = self.url[position + 3:]
            #     playlist_url = "https://music.163.com/playlist?id=" + id
            #     result = requests.get(playlist_url, headers=self.headers).text
            #     dom = etree.HTML(result)
            #     ids = dom.xpath('//a[contains(@href,"song?")]/@href')
            #     title = dom.xpath('//meta[@property="og:title"]/@content')
            #     if title:
            #         true_title = title[0]
            #     else:
            #         true_title = 'Error'
                # self.signal.emit("Clear now")
                # self.signal.emit(true_title)
                # true_title=true_title.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                #                     .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                # if (self.path == ''):
                #     self.path = "D:\\MusicDownload\\" + true_title
                # else:
                #     self.path = self.path + '\\' + true_title
                #     while ('/' in self.path):
                #         position = self.path.find('/')
                #         self.path = self.path[:position] + '\\' + self.path[
                #             position + 1:]
                # path = self.path
                # if (os.path.exists(path)):
                #     pass
                # else:
                #     os.makedirs(path)
                # cot = len(ids)
                # self.signal.emit('当前歌单共计%d首\n' % (cot))
                # for id in ids:
                #     if (self.status == True):
                #         if '$' not in id:
                #             id = id[9:]
                #             true_url = "https://music.163.com/song?id=" + id
                            # down_url = "http://music.163.com/song/media/outer/url?id=" + id + ".mp3"
                            # result = requests.get(true_url,
                            #                       headers=self.headers).text
                            # dom = etree.HTML(result)
                            # name = dom.xpath(
                            #     '//meta[@property="og:title"]/@content')
                            # if name:
                            #     song_name = name[0]
                            # else:
                            #     song_name = 'Error'
                            # album = dom.xpath(
                            #     '//meta[@property="og:music:album"]/@content')
                            # if album:
                            #     song_album = album[0]
                            # else:
                            #     song_album = 'Error'
                            # artist = dom.xpath(
                            #     '//meta[@property="og:music:artist"]/@content')
                            # if artist:
                            #     song_artist = artist[0]
                            # else:
                            #     song_artist = 'Error'
                            # if (song_name == 'Error'
                            #         and song_artist == 'Error'):
                            #     self.signal.emit("解析失败\n")
                            # else:
                            #     self.signal.emit("歌名:" + song_name)
                            #     self.signal.emit("歌手:" + song_artist)
                            #     self.signal.emit("专辑:" + song_album)
                                # music = requests.get(
                                #     down_url, headers=self.headers).content
                                # song_name=song_name.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                                #                 .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                                # song_artist=song_artist.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                                #                 .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                                # file_name = song_name + '-' + song_artist + ".mp3"
                                # true_path = self.path + '\\' + file_name
                                # downloadfunction(down_url, true_path)
                                # if (self.status == True):
                                #     try:
                                #         with open(true_path, 'wb') as file:
                                #             file.write(music)
                                #     except:
                                #         self.signal.emit('下载失败\n')
                                #     else:
                                #         size = self.get_FileSize(true_path)
                                #         if (size > 0.1):
                                #             self.signal.emit('下载成功\n')
                                #         else:
                                #             self.signal.emit('无法下载\n')
                                #             os.remove(true_path)
                    #             cot = cot - 1
                    #             self.signal.emit('剩余%d首\n' % (cot))
                    #             if (cot == 0):
                    #                 self.signal.emit("have finished")
                    # else:
                    #     self.signal.emit('下载已停止\n')
                    #     break
            # else:
                # if "?userid=" in self.url:
                #     position1 = self.url.find("song/")
                #     position2 = self.url.find("/?userid=")
                #     id = self.url[position1 + 5:position2]
                # elif '&' in self.url:
                #     position1 = self.url.find("?id=")
                #     position2 = self.url.find("&")
                #     id = self.url[position1 + 4:position2]
                # else:
                #     position = self.url.find("id=")
                #     id = self.url[position + 3:]
                # true_url = "https://music.163.com/song?id=" + id
                # down_url = "http://music.163.com/song/media/outer/url?id=" + id + ".mp3"
                # result = requests.get(true_url, headers=self.headers).text
                # dom = etree.HTML(result)
                # name = dom.xpath('//meta[@property="og:title"]/@content')
                # if name:
                #     song_name = name[0]
                # else:
                #     song_name = 'Error'
                # album = dom.xpath(
                #     '//meta[@property="og:music:album"]/@content')
                # if album:
                #     song_album = album[0]
                # else:
                #     song_album = 'Error'
                # artist = dom.xpath(
                #     '//meta[@property="og:music:artist"]/@content')
                # if artist:
                #     song_artist = artist[0]
                # else:
                #     song_artist = 'Error'
                # if (song_name == 'Error' and song_artist == 'Error'):
                #     self.signal.emit("解析失败\n")
                # else:
                #     self.signal.emit('Clear now')
                #     self.signal.emit("歌名:" + song_name + '\n')
                #     self.signal.emit("歌手:" + song_artist + '\n')
                #     self.signal.emit("专辑:" + song_album + '\n')
                #     song_name=song_name.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                #                     .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                #     song_artist=song_artist.replace('\\',' ').replace('|',' ').replace('/',' ').replace(':',' ')\
                #                     .replace('?',' ').replace('*',' ').replace('\"',' ').replace('<',' ').replace('>',' ')
                #     file_name = song_name + '-' + song_artist + ".mp3"
                #     while ('/' in file_name):
                #         position = file_name.find('/')
                #         file_name = file_name[:position] + ' ' + file_name[
                #             position + 1:]
                #     if (self.path == ''):
                #         self.path = "D:\\MusicDownload\\"
                #     else:
                #         while ('/' in self.path):
                #             position = self.path.find('/')
                #             self.path = self.path[:position] + '\\' + self.path[
                #                 position + 1:]
                #     path = self.path
                #     if (os.path.exists(path)):
                #         pass
                #     else:
                #         os.makedirs(path)
                #     music = requests.get(down_url,
                #                          headers=self.headers).content
                #     true_path = self.path + '\\' + file_name
                #     try:
                #         with open(true_path, 'wb') as file:
                #             file.write(music)
                #     except:
                #         self.signal.emit('下载失败\n\n')
                #     else:
                #         size = self.get_FileSize(true_path)
                #         if (size > 0.1):
                #             self.signal.emit('下载成功\n\n')
                #         else:
                #             self.signal.emit('无法下载\n\n')
                #             os.remove(true_path)
                # self.signal.emit('have finished')


class DownMusic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.StartGui()
        self.bt3.setEnabled(False)

    def update(self, result):
        #更新文字内容
        if result == 'Clear now':
            self.text.clear()
        elif result == 'have finished':
            self.text.append('歌单下载完成')
            self.bt1.setEnabled(True)
        elif result == 'finished':
            self.bt1.setEnabled(True)
        else:
            self.text.append(result)

    def StartDown(self):
        #开始下载
        if self.platform == '':
            self.text.clear()
            self.text.append('请选择平台')
        else:
            if (self.input1.text() == ''):
                pass
            else:
                url = self.input1.text()
                path = self.input2.text()
                platform = self.platform
                self.result = Downthread(url, path, platform)
                self.result.signal.connect(self.update)
                self.result.start()
                self.bt1.setEnabled(False)
                self.bt3.setEnabled(True)

    def Stop(self):
        #停止下载
        self.result.status = False
        self.bt1.setEnabled(True)

    def SelectPath(self):
        #选择路径
        path = QFileDialog.getExistingDirectory(self, '选取文件夹', './')
        self.input2.setText(path)

    def select_platform(self):
        #选择平台
        if self.qr1.isChecked():
            self.platform = 'wangyi'
        elif self.qr2.isChecked():
            self.platform = 'kuwo'

    def StartGui(self):
        #启动界面
        def screencenter():
            # 屏幕居中
            desktop = QApplication.desktop()
            screenrect = desktop.screenGeometry()
            scr_w = screenrect.width()
            scr_h = screenrect.height()
            cen_w = (scr_w - 974) / 2
            cen_h = (scr_h - 730) / 2
            return cen_w, cen_h

        def AboutUs():
            # 关于
            MsgBox = QMessageBox(
                QMessageBox.NoIcon, '关于我们',
                '这只是一个用来方便下载的工具\n感谢 Charles提供的酷我音乐入口（github)\n\npowered by Nobilta \nVersion:1.4\n更新内容:\n新增酷我平台解析,修复bug'
            )
            MsgBox.exec()

        def Help():
            #帮助
            Msgbox = QMessageBox(
                QMessageBox.NoIcon, '帮助',
                '复制一个网易云或酷我的单曲(歌单)，粘贴到工具中，选择平台，点击下载，默认路径为D:\\MusicDownload(-歌单名)\n如遇网易云平台下载失败，建议尝试酷我平台 '
            )
            Msgbox.exec()

        self.platform = ''
        w, h = screencenter()
        # 背景图片
        palette = QtGui.QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))

        # 文字标签
        self.lb1 = QLabel("请输入网易云音乐(歌单)链接:", self)
        self.lb1.resize(350, 25)
        self.lb1.move(18, 32)
        self.lb1.setStyleSheet('color:#696969')
        self.lb1.setFont(QFont("微软雅黑", 15))

        # 输入框
        self.input1 = QLineEdit(self)
        self.input1.resize(700, 20)
        self.input1.move(18, 85)
        self.input1.setPlaceholderText("请输入链接")
        self.input1.setFont(QFont("Arial", 14))
        self.input1.setStyleSheet(
            "background:transparent;border-width:0;border-style:outset;color:#696969;font-style:italic"
        )

        self.lb2 = QLabel(
            "————————————————————————————————————————————————————————————————————",
            self)
        self.lb2.resize(700, 15)
        self.lb2.move(18, 108)
        self.lb2.setFont(QFont("微软雅黑", 11))
        self.lb2.setStyleSheet("color:#696969")

        # 下载按钮
        self.bt1 = QPushButton("下载", self)
        self.bt1.resize(60, 30)
        self.bt1.move(740, 90)
        self.bt1.setFont(QFont("微软雅黑", 9))
        self.bt1.setStyleSheet(
            "background:#7ccee3;color:white;border-radius:15px")
        self.bt1.clicked.connect(self.StartDown)

        # 停止按钮
        self.bt3 = QPushButton("停止", self)
        self.bt3.resize(60, 30)
        self.bt3.move(820, 90)
        self.bt3.setFont(QFont("微软雅黑", 9))
        self.bt3.setStyleSheet(
            "background:#FD9892;color:white;border-radius:15px")
        self.bt3.clicked.connect(self.Stop)

        # 选择按钮
        self.qr1 = QRadioButton('网易云音乐', self)
        self.qr1.resize(120, 30)
        self.qr1.move(20, 125)
        self.qr1.setFont(QFont('微软雅黑', 11))
        self.qr1.setStyleSheet('color:blue')
        self.qr1.clicked.connect(self.select_platform)
        self.qr2 = QRadioButton('酷我音乐', self)
        self.qr2.resize(120, 30)
        self.qr2.move(150, 125)
        self.qr2.setFont(QFont('微软雅黑', 11))
        self.qr2.setStyleSheet('color:blue')
        self.qr2.clicked.connect(self.select_platform)

        # 显示框
        self.text = QTextBrowser(self)
        self.text.resize(800, 430)
        self.text.move(87, 170)
        self.text.setFont(QFont("微软雅黑", 13))
        self.text.setStyleSheet(
            "background:transparent;color:#696969;border-color:#696969")

        # 设置路径
        self.input2 = QLineEdit(self)
        self.input2.resize(615, 25)
        self.input2.move(185, 623)
        self.input2.setFont(QFont("Arial", 12))
        self.input2.setStyleSheet(
            "background:transparent;color:#696969;border-width:0;border-style:outset"
        )
        self.lb3 = QLabel("选择路径：", self)
        self.lb3.resize(100, 30)
        self.lb3.move(80, 620)
        self.lb3.setFont(QFont("微软雅黑", 14))
        self.lb3.setStyleSheet("color:#696969")
        self.lb4 = QLabel(
            "————————————————————————————————————————————————————————————————————",
            self)
        self.lb4.resize(615, 35)
        self.lb4.move(185, 630)
        self.lb4.setStyleSheet("color:#696969")
        self.lb4.setFont(QFont("微软雅黑", 13))

        # 选择路径按钮
        self.bt2 = QPushButton("选择", self)
        self.bt2.resize(60, 30)
        self.bt2.move(830, 623)
        self.bt2.setFont(QFont("微软雅黑", 9))
        self.bt2.setStyleSheet(
            "background:#7ccee3;color:white;border-radius:15px")
        self.bt2.clicked.connect(self.SelectPath)

        # 关于/帮助按钮
        self.bt4 = QPushButton('关于', self)
        self.bt4.resize(50, 20)
        self.bt4.move(430, 680)
        self.bt4.setFont(QFont('微软雅黑', 9))
        self.bt4.setStyleSheet(
            'background:transparent;color:blue;border-width:0')
        self.bt4.clicked.connect(AboutUs)
        self.bt5 = QPushButton('帮助', self)
        self.bt5.resize(50, 20)
        self.bt5.move(480, 680)
        self.bt5.setFont(QFont('微软雅黑', 9))
        self.bt5.setStyleSheet(
            'background:transparent;color:blue;border-width:0')
        self.bt5.clicked.connect(Help)

        # 初始化
        self.setPalette(palette)
        self.setGeometry(w, h, 974, 730)
        self.setFixedSize(974, 730)
        self.setWindowTitle('MusicDownloader V1.4')
        self.setWindowIcon(QIcon('ico.jpg'))
        self.setAutoFillBackground(True)
        self.text.setText("准备就绪")
        self.show()
        os.remove('bg.jpg')
        os.remove('ico.jpg')
        self.result = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = DownMusic()
    s.show()
    sys.exit(app.exec_())
