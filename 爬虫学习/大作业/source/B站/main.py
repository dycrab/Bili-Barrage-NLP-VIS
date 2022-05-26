# -*- coding: utf-8 -*-
# @Time : 2022/5/7 12:45
# @Author : Leviathan_Sei
# @File : main.py
# @Python : 3.7
import csv
import os

from PyQt5 import QtWidgets
import sys

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from snownlp import SnowNLP

from BarrageGet import BarrageGet
from keywordSearch import BvidGet
from cloud import CLoud


class Bvid(QThread):
    _signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    # 设置keywords参数 用来接受 keywords列表 用于爬取
    def __init__(self, keywords=True):
        super().__init__()
        self.do_keywords = keywords

    def run(self):
        """
        进行爬虫的工作, 并返回结果
        """
        for word in self.do_keywords:
            # 发射信号
            self._signal.emit("爬取BVIDing...\n关键词为：" + word)
            bvidGet = BvidGet(word)
            bvidGet.get_save_data()


class WordCloud(QThread):
    _signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, keywords=True):
        super().__init__()
        self.do_keywords = keywords

    def run(self):
        """
        进行任务操作，主要的逻辑操作,返回结果
        """
        # 发射信号
        for word in self.do_keywords:
            self._signal.emit("生成词云ing...\n关键词为：" + word)
            cloudGet = CLoud(word)
            cloudGet.get_pic()


class nlpThread(QThread):
    _signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, keywords=True):
        super().__init__()
        self.do_keywords = keywords
        self.keyword = None
        self.barrage_list = []
        self.len = 0
        self.good_time = 0
        self.neutral_time = 0
        self.bad_time = 0
        self.good_score = 0.75
        self.neutral_score = 0.45
        self.score_list = []
        self.type_list = []
        self.max_score = -1.0
        self.min_score = -1.0
        self.mean_score = 0.0
        self.range = -1
        self.save_list = []

    def get_barrage_type(self):
        for barrage in self.barrage_list:
            tmp = []
            try:
                score = SnowNLP(barrage).sentiments
            except ZeroDivisionError:
                score = 0.5
            self.score_list.append(score)
            if score > self.good_score:
                self.type_list.append("积极")
                self.good_time += 1
                tmp = [barrage, score, "积极"]
            elif score > self.neutral_score:
                self.type_list.append("一般")
                self.neutral_time += 1
                tmp = [barrage, score, "一般"]
            else:
                self.type_list.append("消极")
                self.bad_time += 1
                tmp = [barrage, score, "消极"]
            self.save_list.append(tmp)

    def get_barrage(self):
        with open('../data/danmuku/dm' + self.keyword + '.csv', 'r', encoding='utf-8') as f:
            self.barrage_list = f.read().split('\n')
        self.len = len(self.barrage_list)

    def run(self):
        """
        进行任务操作，主要的逻辑操作,返回结果
        """
        # 发射信号
        for word in self.do_keywords:
            self.keyword = word
            self.save_list = []
            self._signal.emit("NLP分析ing...\n关键词为：" + word)
            self.get_barrage()
            self.get_barrage_type()
            with open('../data/NLP_score/' + self.keyword + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
                wt = csv.writer(f)
                wt.writerows(self.save_list)


class Barrage(QThread):
    _signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, keywords=True):
        super().__init__()
        self.do_keywords = keywords

    def run(self):
        """
        进行任务操作，主要的逻辑操作,返回结果
        """
        # 发射信号
        for word in self.do_keywords:
            self._signal.emit("爬取弹幕ing...\n关键词为：" + word)
            barrageGet = BarrageGet(word)
            barrageGet.get_barrge()


class MainWindow(QtWidgets.QMainWindow):  # 组合继承
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('main.ui', self)
        self.setWindowIcon(QIcon("../data/favicon.ico"))
        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.plt = static_canvas.figure.subplots()
        self.setWindowTitle("基于关键词的B站弹幕分析系统")
        # self.setObjectName("基于关键词的B站弹幕分析系统")
        self.setStyleSheet('''QWidget{background-color:#66ccff;}''')
        self.pushButton.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.pushButton_2.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.textEdit.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.textBrowser.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        self.checkBox.stateChanged.connect(self.changeReady)
        self.checkBox_2.stateChanged.connect(self.changeReady)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        # self.ui_page.setupUi(self)
        self.keywords = None
        self.pushButton.clicked.connect(self.work)
        self.pushButton_2.clicked.connect(self.close)
        self.thread = None
        self.thread1 = None
        self.thread0 = None
        self.jobID = 0
        self.readyCloud = 1
        self.readyNLP = 1
        self.keyword = None
        self.barrage_list = []
        self.len = 0
        self.good_time = 0
        self.neutral_time = 0
        self.bad_time = 0
        self.good_score = 0.75
        self.neutral_score = 0.45
        self.score_list = []
        self.type_list = []
        self.max_score = -1.0
        self.min_score = -1.0
        self.mean_score = 0.0
        self.range = -1
        self.show()

    def changeReady(self):
        if self.checkBox.isChecked():
            self.readyCloud = 1
        else:
            self.readyCloud = 0
        if self.checkBox_2.isChecked():
            self.readyNLP = 1
        else:
            self.readyNLP = 0
        # print(self.readyCloud, self.readyNLP)

    def get_keywords(self):
        if len(str(self.textEdit.toPlainText())) == 0:
            self.keywords = []
        else:
            self.keywords = str(self.textEdit.toPlainText()).strip().split('\n')

    def get_bvid(self, msg):
        self.textBrowser.append(msg)
        self.pushButton.setEnabled(True)

    def get_barrage(self, msg):
        self.textBrowser.append(msg)
        self.pushButton.setEnabled(True)

    def get_word_cloud(self, msg):
        self.textBrowser.append(msg)
        self.pushButton.setEnabled(True)

    def get_NLP_pie(self, msg):
        self.textBrowser.append(msg)
        self.pushButton.setEnabled(True)

    def NLP_done(self):
        self.textBrowser.append("NLP分析完毕！")

    def cloud_done(self):
        self.textBrowser.append("词云生成完毕！")

    def word1(self):
        self.pushButton.setEnabled(False)
        self.thread = Bvid(self.keywords)
        self.thread._signal.connect(self.get_bvid)  # 连接回调函数，接收结果
        self.thread.start()  # 启动线程
        self.thread.finished.connect(self.word2)

    def word2(self):
        self.pushButton.setEnabled(False)
        self.thread0 = Barrage(self.keywords)
        self.thread0._signal.connect(self.get_barrage)  # 连接回调函数，接收结果
        self.thread0.start()  # 启动线程
        self.thread0.finished.connect(self.word3)

    def word3(self):
        self.textBrowser.append("弹幕爬取完毕！！！")
        if self.readyCloud == 1:
            self.pushButton.setEnabled(False)
            self.thread1 = WordCloud(self.keywords)
            self.thread1._signal.connect(self.get_word_cloud)  # 连接回调函数，接收结果
            self.thread1.start()  # 启动线程
            self.thread1.finished.connect(self.cloud_done)
        if self.readyNLP == 1:
            self.pushButton.setEnabled(False)
            self.thread2 = nlpThread(self.keywords)
            self.thread2._signal.connect(self.get_NLP_pie)  # 连接回调函数，接收结果
            self.thread2.start()  # 启动线程
            self.thread2.finished.connect(self.NLP_done)

    def work(self):
        self.get_keywords()
        if len(self.keywords) == 0:
            self.textBrowser.append("请输入关键词！")
        else:
            self.word1()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
