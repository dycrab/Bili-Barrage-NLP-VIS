# -*- coding: utf-8 -*-
# @Time : 2022/5/6 15:53
# @Author : Leviathan_Sei
# @File : 情感分析.py
# @Python : 3.7

from snownlp import SnowNLP

class DanmuNLP(object):
    '''
    初始化NLP列表
    '''
    def __init__(self, barrage_list):
        self.barrage_list = barrage_list
        self.snow = SnowNLP
        self.len = len(self.barrage_list)
        self.good_score = 0.75
        self.neutral_score = 0.45
        self.score_list = []
        self.type_list = []

    def get_barrage_type(self):
        for barrage in self.barrage_list:
            self.score_list.append(SnowNLP(barrage).sentiments)
            if self.score_list[-1] > self.good_score:
                self.type_list.append("积极")
            elif self.score_list[-1] > self.neutral_score:
                self.type_list.append("一般")
            else:
                self.type_list.append("消极")







