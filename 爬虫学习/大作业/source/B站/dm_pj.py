# -*- coding: utf-8 -*-
# @Time : 2022/5/6 10:34
# @Author : Leviathan_Sei
# @File : dm_pj.py.py
# @Python : 3.7

# -*- coding: utf-8 -*-
# @Author  :
# @Date    :
# @File    : dm_pj.py
# @description : XXX


import json
import requests
from dm_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson, Parse

b_web_cookie = "buvid3=24D5D9DF-8E89-4174-B76F-79AE6FB4769D58474infoc; blackside_state=1; rpdid=|(Ylm|mu|km0J'uY|~Ym)|)); LIVE_BUVID=AUTO9616250513411298; i-wanna-go-back=-1; _uuid=3FF29B55-861F-32A5-B416-623A1010F3B5E440590infoc; buvid4=385C1C65-A159-6AFC-B8FB-5499B6B078CA42412-022031011-uk4/G28K78xQotvtGK73yheCq4UnLoHUCLHWw2AHuVVvmw9R4aGxvQ%3D%3D; sid=j0m7a14n; buvid_fp_plain=undefined; DedeUserID=148898352; DedeUserID__ckMd5=ebcdf2a1964a68e5; SESSDATA=e4375e22%2C1662435567%2Cecfb1*31; bili_jct=2970fc7631b97da49c2dd68df34e9961; b_ut=5; CURRENT_BLACKGAP=0; nostalgia_conf=-1; hit-dyn-v2=1; is-2022-channel=1; PVID=1; fingerprint3=922a782fd92b77cdda9817a8f405f791; CURRENT_QUALITY=116; fingerprint=413d4e682bb7b0bb7234ac014dc37b29; buvid_fp=413d4e682bb7b0bb7234ac014dc37b29; bp_video_offset_148898352=656777379740385400; b_lsid=716C1055C_180973854C8; innersign=1; CURRENT_FNVAL=4048"


def get_date_list():
    url = "https://api.bilibili.com/x/v2/dm/history/index?type=1&oid=168855206&month=2022-02"
    headers = {
        'cookie': b_web_cookie
    }
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), ensure_ascii=False, indent=4))


def dm_real_time():
    url_real_time = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=11742550&pid=935826118&segment_index=1'
    resp = requests.get(url_real_time)

    DM = DmSegMobileReply()
    DM.ParseFromString(resp.content)
    data_dict = json.loads(MessageToJson(DM))
    # print(data_dict)
    list(map(lambda x=None: print(x['content']), data_dict.get('elems', [])))


def dm_history(url_history):
    url_history = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=168855206&date=2022-02-23'
    headers = {
        'cookie': b_web_cookie
    }
    resp = requests.get(url_history, headers=headers)
    DM = DmSegMobileReply()
    DM.ParseFromString(resp.content)
    data_dict = json.loads(MessageToJson(DM))
    # print(data_dict)
    list(map(lambda x=None: print(x['content']), data_dict.get('elems', [])))


if __name__ == '__main__':
    dm_real_time()
    # get_date_list()
    # dm_history()
    pass