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


class RunNetworkSpider(SougouImageCrawler):
    def __init__(self, _path, _keyword, _page):
        super(RunNetworkSpider, self).__init__(path=path)
        self.path = _path
        self.keyword = _keyword
        self.page = _page
        self.run()

    def run(self):
        res = self.request_url(page_num=self.page, keyword=self.keyword)
        self.upload_image_local_path(res)


if __name__ == "__main__":
    params = {
        "page_num": [48 * i for i in range(1, 26)],
        "keyword": {
            "恐怖分子": "202211161416450102121921510F59F753",
            "恐怖袭击": "2022111616572901015003909441A91451",
            "恐怖头目": "20221116165826010212192159404CD485",
            "警察部队": "202211161706090102121851650553D180",
            "大型军事武器": "2022111617065501015104402823AA23BE",
            "枪械": "202211161708000102121830430E523C54",
            "刀具": "202211161708430102121830431F4E8448",
            "武装人员": "202211161709190102121831442C4C5F5A",
            "血腥": "202211161711010101500390944D9A4305",
            "人类尸体": "202211161711570102121871695157F6C2",
            "动物尸体": "202211161712370102121831440D533DEB",
            "爆炸": "202211161721280102121871690D54ADB6",
            "火灾": "20221116172213010212172034514E1D9B",
            "火灾爆炸": "202211161722370101501350300496D7E0",
            "暴乱": "20221116172311010212192136104FE4B3",
            "中国国旗": "202211161737020102121920453D5866AB",
            "中国地图": "20221116173802010212183144214D4238",
            "国徽": "2022111617405701015013703547944352",
            "党旗": "20221116174131010212187169124CED82",
            "党徽": "202211161741570101500390945FBFD37C",
            "军旗": "202211161742290101501370350AA44B01",
            "警徽": "2022111617443001015013614422AB248A",
            "敏感物品": "202211161759470101500390940EA16A7C",
            "宗教": "202211161745560102121672070D54CC42",
            "道教服饰": "202211161746550101500390945FBFDDFC",
            "佛教服饰": "2022111617480101021216609658570AAD",
            "领导人": "20221116174847010150139012169A536D",
            "人民币": "202211161751180102120222265B561E72",
            "二维码": "202211161751530101501350300B9E9320",
            "条形码": "202211161752210101501350304D99A4CE",
            "小程序码": "202211161752560101500200493BA4B277",
            "吸烟": "20221116175333010212192136064C952E",
            "吸烟卡通": "20221116175424010212192051455801A1",
            "纹身": "2022111617553501015013703510902D38",
            "竖中指": "202211161756050101501350305999DCDE",
            "钱币": "202211161756580101501361442C9319A2",
            "脏器": "2022111617573301021219402558529A23",
            "恶心动物": "2022111617585401021218304323560BBF",
            "赌博": "20221116180050010212046101164BBD50",
            "广告": "20221116180050010212046101164BBD50",
            "宣传栏": "20221116180050010212046101164BBD50",
            "广告牌": "20221116180050010212046101164BBD50",
            "金融订单": "20221116180050010212046101164BBD50",
            "订单": "20221116180050010212046101164BBD50",
            "信用卡账单": "20221116180050010212046101164BBD50",
            "银行柜台": "20221116180050010212046101164BBD50",
            "取款机": "20221116180050010212046101164BBD50"
        }
    }
    path = "D:/图片数据集/"
    keyword = "恐怖袭击"
    for keyword in params["keyword"].keys():
        for index, page_num in enumerate(params["page_num"]):
            print("正在采集【{}】，第{}页".format(keyword, index+1))
            RunNetworkSpider(_path=path, _keyword=keyword, _page=page_num)
