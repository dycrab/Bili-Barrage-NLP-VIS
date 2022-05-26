# -*- coding: utf-8 -*-
# @Time : 2022/5/6 10:54
# @Author : Leviathan_Sei
# @File : keywordSearch-Tencent.py
# @Python : 3.7
import re
import csv
import requests
import time


class BvidGet(object):
    def __init__(self, keyword=True):
        self.keyword = keyword
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }

    def get_html(self, url):
        ret = requests.get(url, headers=self.headers)
        ret.encoding = 'utf-8'
        return ret.json()['data']['result'][-1]['data']

    def get_save_data(self):
        '''

        通过 对链接进行请求获得视频数据 并对数据进行提取保存
        '''
        url = 'https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&' \
              '_extra=&context=&page=1&page_size=42&order=&duration=&from_source=&from_spmid=333.337&' \
              'platform=pc&highlight=1&single_column=0&keyword=' + self.keyword + '&preload=true&com2co=true'
        source_data_list = self.get_html(url)
        save_list = []
        for vd in source_data_list:
            tmp_list = [vd['aid'], vd['bvid'], vd['mid'], vd['title'], vd['arcurl'], vd['play']]
            save_list.append(tmp_list)
        with open('../data/video_infos/' + self.keyword + '.csv', 'w', encoding='utf-8', newline='') as f:
            f = csv.writer(f)
            f.writerows(save_list)
        time.sleep(5)

# if __name__ == '__main__':
#
#
#     get_save_data()
