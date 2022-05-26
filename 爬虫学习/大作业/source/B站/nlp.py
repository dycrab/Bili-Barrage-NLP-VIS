# -*- coding: utf-8 -*-
# @Time : 2022/5/23 21:32
# @Author : Leviathan_Sei
# @File : nlp.py
# @Python : 3.7
import csv
from threading import Thread

from snownlp import SnowNLP

from matplotlib import pyplot as plt


plt.rcParams['font.sans-serif'] = ['KaiTi']


class DanmuNLP(Thread):
    '''
    初始化NLP列表
    '''
    def __init__(self, keyword=True):
        super(DanmuNLP, self).__init__()
        self.keyword = keyword
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

    def get_time(self):
        with open('../data/NLP_score/'+self.keyword+'.csv', 'r', encoding='utf-8-sig') as f:
            file = csv.reader(f)
            for row in file:
                if row[-1] == '一般':
                    self.neutral_time += 1
                elif row[-1] == '积极':
                    self.good_time += 1
                else:
                    self.bad_time += 1

    def get_pic(self):


        labels = ['积极', '一般', '消极']
        sizes = [self.good_time, self.neutral_time, self.bad_time]
        explode = (0, 0, 0.2)
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', shadow=True, startangle=100)
        # 设置 标题
        title = "Bili "+self.keyword+" Pie"
        plt.title(title)
        plt.savefig('../data/pic_pie/'+title+'.png')

def get_key_words_list():
    with open('../data/keys', 'r', encoding='utf-8') as f:
        key_list = f.read().split('\n')

    return key_list


if __name__ == '__main__':
    keys = get_key_words_list()
    for key in keys:
        nlp = DanmuNLP(key)
        nlp.get_time()
        nlp.get_pic()



