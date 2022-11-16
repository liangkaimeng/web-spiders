#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 0016 19:11
# @Author  : LKM

import os
import re
import time
import warnings
import requests
from requests.exceptions import SSLError, ConnectionError, ConnectTimeout

warnings.filterwarnings("ignore")


class SougouImageCrawler:
    """ 采集搜狗图片数据：https://pic.sogou.com/napi/pc/ """

    def __init__(self, path):
        """ 实例化 """
        self.path = path
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": "IPLOC=CN4419; SUV=00542E241B2C18876374BE784BFC2952; wuid=1668595320672; SNUID=25BA8FB9A3A64F3682A0A05AA32D2C1C; search_tip=1668595147347; ABTEST=1|1668595828|v1; FUV=0a3f821957227c8563333662c3485bc3"
        }

    def request_url(self, page_num, keyword):
        """ 请求链接，返回数据JSON """
        url = "https://pic.sogou.com/napi/pc/searchList?mode=1&start={}&xml_len=48&query={}".format(page_num, keyword)
        session = requests.session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=10))

        response = None
        try:
            response = session.request("GET", url=url, headers=self.headers, verify=False, timeout=30)
        except (SSLError, ConnectionError, ConnectTimeout):
            pass

        if response:
            response = response.json()

        return response

    def upload_image_local_path(self, json_files):
        """ 解析图片，保存图片到本地 """
        global keyword
        if not json_files:
            pass
        else:
            save_file_path = self.path + "搜狗图片数据集/" + keyword + "/"
            if not os.path.exists(save_file_path):
                os.makedirs(save_file_path)

            content = json_files["data"]["items"]
            for item in content:
                img_url = item["picUrl"]
                img_name = re.sub(r"[+|\-|/|*|_]", "", item["name"].split(".")[0])
                if len(img_name) < 8:
                    img_name = re.sub("[.]", "", str(time.time()))

                session = requests.session()
                session.mount('http://', requests.adapters.HTTPAdapter(max_retries=10))
                try:
                    img_content = session.request("GET", url=img_url, headers=self.headers, timeout=30).content
                    with open(save_file_path + img_name + ".jpg", "wb") as f:
                        f.write(img_content)
                except (SSLError, ConnectionError, ConnectTimeout):
                    pass


if __name__ == "__main__":
    page = 1
    keyword = "恐怖袭击"
    path = "D:/图片数据集/"
    cls = SougouImageCrawler(path=path)
    res = cls.request_url(page_num=page, keyword=keyword)
    cls.upload_image_local_path(res)
