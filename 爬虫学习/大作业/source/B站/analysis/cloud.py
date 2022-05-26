# -*- coding: utf-8 -*-
# @Time : 2022/5/6 15:53
# @Author : Leviathan_Sei
# @File : cloud.py
# @Python : 3.7

import jieba
import random
import stylecloud




class CLoud(object):
    def __init__(self, keyword=True):
        self.keyword=keyword
        self.text = ''

    def get_cut_words(self,content_series):
        # 读入停用词表
        stop_words = []

        with open("analysis/cn_stopwords.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())

        # 添加关键词
        my_words = ['a', 'b']
        for i in my_words:
            jieba.add_word(i)

            # 自定义停用词
        my_stop_words = []
        stop_words.extend(my_stop_words)

        # 分词
        word_num = jieba.lcut(content_series, cut_all=False)

        # 条件筛选
        word_num_selected = [i for i in word_num if i not in stop_words and len(i) >= 2]

        return word_num_selected


    def get_random_shape(self):

        shapes = open('analysis/wordcloud_shapes', 'r', encoding='utf-8').read().split('\n')

        return random.choice(shapes)


    def get_word_cloud(self, text1):
        print(self.get_random_shape())
        stop_words = []
        with open("analysis/cn_stopwords.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                stop_words.append(line.strip())
        stylecloud.gen_stylecloud(text=' '.join(text1), collocations=False,
                                  palette='cartocolors.qualitative.Pastel_5',
                                  font_path=r'‪C:\Windows\Fonts\msyh.ttc',
                                  icon_name='fas '+self.get_random_shape(),
                                  size=400,
                                  output_name='pic_wordcloud/'+self.keyword+'词云图.png')


    def get_dm(self):
        with open('../../data/bilibili/dm'+self.keyword+'.csv', 'r', encoding='utf-8') as f:
            dm = f.read().split('\n')
        return ''.join(dm)

    def get_pic(self):
        self.get_word_cloud(self.get_cut_words(self.get_dm()))

# if __name__ == '__main__':
#     for word in keywords:
#         keyword=word
#         dm = get_dm(keyword)
#         text = get_cut_words(dm)
#         get_word_cloud(text)

