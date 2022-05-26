# -*- coding: utf-8 -*-
# @Time : 2022/5/6 14:24
# @Author : Leviathan_Sei
# @File : BarrageGet.py
# @Python : 3.7
import time
import csv
import re
import json
import requests
from dm_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson, Parse


class BarrageGet(object):
    def __init__(self, keyword=True):

        self.b_web_cookie = ''
        self.headers = {
            'cookie': self.b_web_cookie
        }
        self.keyword = keyword
        self.id_list = []
        self.get_id_list()
        self.get_cookie()

    def get_cookie(self):
        with open('../data/cookies', 'r', encoding='utf-8') as f:
            self.b_web_cookie = f.read()

    def get_date_list(self, oid):
        url = "https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=" + oid + "&month=2022-05"
        response = requests.get(url, headers=self.headers)
        list_date = json.dumps(response.json(), ensure_ascii=False, indent=4)

        return list_date

    def get_cid(self, bvid):

        url = 'https://www.bilibili.com/video/' + bvid
        ret = requests.get(url, headers=self.headers)
        ret.encoding = 'utf-8'
        html = ret.text

        cid = re.findall('"cid":(.*?),', html)[0]
        return cid

    def dm_history(self, url_history):

        headers = {
            'cookie': self.b_web_cookie
        }
        resp = requests.get(url_history, headers=headers)
        DM = DmSegMobileReply()
        DM.ParseFromString(resp.content)
        data_dict = json.loads(MessageToJson(DM))
        # print(data_dict)
        dm_list = []
        list(map(lambda x=None: dm_list.append(x['content']), data_dict.get('elems', [])))
        return dm_list

    def dm_real_time(self, url_real_time):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'cookie': self.b_web_cookie
        }
        resp = requests.get(url_real_time, headers=headers)

        DM = DmSegMobileReply()
        DM.ParseFromString(resp.content)
        data_dict = json.loads(MessageToJson(DM))
        # print(data_dict)
        dm_list = []
        list(map(lambda x=None: dm_list.append(x['content']), data_dict.get('elems', [])))
        return dm_list

    def get_barrge(self):
        for id_tuple in self.id_list:

            oid = self.get_cid(id_tuple[1])
            try:
                date_list = json.loads(self.get_date_list(oid))['data']
                for date in date_list:
                    dm_url_history = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=' + oid + '&date=' + date
                    dm_list = self.dm_history(dm_url_history)

                    self.save_dm(dm_list)
                    if self.quit():
                        return
                    if date != date_list[-1]:
                        time.sleep(10)
            except Exception as e:
                print(e)
            url_real_time = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=' + oid + '&pid=' + id_tuple[
                0] + '&segment_index=1'
            dm_list = self.dm_real_time(url_real_time)

            self.save_dm(dm_list)
            if self.quit():
                return
            if id_tuple != self.id_list[-1]:
                time.sleep(10)

    def quit(self):
        count = 0
        with open('../data/danmuku/dm' + self.keyword + '.csv', 'r', encoding='utf-8-sig') as f:
            for index, _ in enumerate(f):
                count += 1
                if count > 10000:
                    return True

    def save_dm(self, dm_list):
        # print("saving")
        # print(dm_list)
        with open('../data/danmuku/dm' + self.keyword + '.csv', 'a', encoding='utf-8-sig', newline='') as f:
            for dm in dm_list:
                f.write(dm + '\n')

    def get_id_list(self):

        with open('../data/video_infos/' + self.keyword + '.csv', 'r', encoding='utf-8-sig') as f:
            file = csv.reader(f)
            for line in file:

                self.id_list.append((line[0], line[1]))

# if __name__ == '__main__':
#     get_barrge()
