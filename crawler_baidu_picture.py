#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/5 0005 22:20
# @Author  : LKM

import re
import os
import warnings
import requests
from urllib import request
from requests.exceptions import SSLError, ConnectionError, ConnectTimeout

warnings.filterwarnings("ignore")


class CrawlerBaiduPicture:
    def __init__(self, _keywords: list):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
        }
        for item, keyword in enumerate(_keywords):
            self.get_picture_set(keyword=keyword, item=item)

    def get_picture_set(self, keyword: str, item: int):
        all_picture_list: list = []
        pageNum: int = 20
        if "金融" in keyword:
            pageNum = 40
        for page in range(pageNum):
            page = page * 30
            url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&pn={}'.format(keyword, page)
            session = requests.session()
            session.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
            try:
                html = session.request("GET", url=url, headers=self.header, verify=False, timeout=30)
                html_content = html.content.decode("utf-8")
                picture_list = re.findall('{"thumbURL":"(.*?)",', html_content)
                all_picture_list.extend(picture_list)
            except (SSLError, ConnectionError, ConnectTimeout):
                pass

        all_picture_set = set(all_picture_list)
        self.download_picture(all_picture_list=all_picture_set, prefix=keyword, item=item)

    @staticmethod
    def download_picture(all_picture_list, prefix, item):
        path = "../Dateset/" + prefix
        if not os.path.exists(path):
            os.makedirs(path)
        for index, pic_url in enumerate(all_picture_list):
            string = '{}/{}00000{}.jpg'.format(prefix, str(item), str(index + 1))
            try:
                request.urlretrieve(pic_url, string)
            except (SSLError, ConnectionError, ConnectTimeout):
                pass


if __name__ == "__main__":
    keywords = ['金融柜台', '金融贷款', '贷款账单', '信用卡', '东莞银行',
                '金融投诉', '金融订单', '金融员工', '柜员机', '打砸抢钱',
                '分裂国家', '恐怖主义', '极端宗教主义', '涉政场景', '',
                '情趣用品', '暴恐旗帜', '暴恐标识', '暴恐图集', '燃烧爆炸',
                '黑社会', '恐怖袭击', '血腥场面', '国民党', '共产党',
                '国旗国徽', '政治人物', '军装', '恶搞漫画', '反动人物',
                '枪支刀具', '血腥暴乱', '卡通动漫', '帅哥', '美女',
                '山峰', '河流', '建筑', '树木', '草地', '订单',
                '街道', '车辆', '衣服', '商务人士', '男女明星']
    CrawlerBaiduPicture(keywords)
