# -*- coding: utf-8 -*-
# Author: lkm
# date: 2022/11/17 11:22

import os
import warnings
import requests
from urllib.parse import *
from requests.exceptions import SSLError, ConnectionError, ConnectTimeout

warnings.filterwarnings("ignore")


class RequestURL:
    """ 发送访问请求，返回请求结果，对返回结果进行解析 """
    def __init__(self, path):
        self.path = path
        self.url = "https://so.toutiao.com/search?"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
            "Cookie": "msToken=KqGRTq14LOFyzuimd7asNbqd0uZY7DgXgyq70yrn6lRKeAJ91YSRVdJChnaue81jjjvnr-UqfHBwlJBsjjhMjKVqCluwwG7zcADyb3cFHw4s; tt_webid=7166432939261134367; _tea_utm_cache_4916=undefined; _S_DPR=1.25; _S_IPAD=0; MONITOR_WEB_ID=7166432939261134367; ttwid=1%7C6mtaRB-MQ9ZNaBlBFLn5IP3dZ7Jg-v8Mm_0RWrlBD6U%7C1668568822%7Cb97b77146bd9549a7bc80e7c1b7ff53370b003e781d8c51f856b53955b343cd8; __ac_nonce=06374804c0004c5ba62fe; __ac_signature=_02B4Z6wo00f01qoaqUgAAIDBGutFg04JteaqO63AAMn-87; __ac_referer=https://so.toutiao.com/search?dvpf=pc&source=input&keyword=%E6%81%90%E6%80%96%E5%88%86%E5%AD%90; _S_WIN_WH=1536_720"
        }

    def request_url(self, _keyword, search_id, pageNum):
        """ 发送请求，返回请求内容json """
        params = {
            "dvpf": "pc",
            "source": "search_subtab_switch",
            "keyword": _keyword,
            "pd": "atlas",
            "action_type": "search_subtab_switch",
            "page_num": pageNum,
            "search_id": search_id,
            "from": "gallery",
            "cur_tab_title": "gallery",
            "rawJSON": 1
        }  # 定义参数
        url = self.url + urlencode(params)  # 拼接链接
        session = requests.session()  # 创建会话
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=10))  # 请求失败则尝试10次

        response = None  # 定义返回内容为None
        try:
            response = session.request("GET", url=url, headers=self.headers, verify=False, timeout=30)  # 发送请求
        except (SSLError, ConnectionError, ConnectTimeout):
            pass

        if response:
            response = response.json()  # 转换为json

        return response

    def extract_json_info(self, json_info):
        """ 解析json内容，保存图片到本地路径 """
        global keyword
        if not json_info:
            pass
        else:
            save_file_path = self.path + "今日头条图片数据集/" + keyword + "/"
            if not os.path.exists(save_file_path):  # 判断文件夹是否存在，不存在则创建
                os.makedirs(save_file_path)

            contents = json_info.get('rawData').get('data')  # 获取请求内容
            for content in contents:
                img_url = content.get("img_url")

                session = requests.session()
                session.mount('https://', requests.adapters.HTTPAdapter(max_retries=10))
                try:
                    img_content = session.request("GET", url=img_url, headers=self.headers, timeout=30).content
                    with open(save_file_path + str(abs(int(contents.get("id")))) + ".jpeg", "wb") as f:
                        f.write(img_content)
                except (SSLError, ConnectionError, ConnectTimeout):
                    pass


class CrawlerRun(RequestURL):
    """ 执行爬虫 """
    def __init__(self, path):
        super().__init__(path=path)
        self.run()

    def run(self):
        grip_params = {
            "page_num": range(21),
            "keywords": {
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
                "赌博": "20221116180050010212046101164BBD50"
            }
        }
        for word in grip_params["keywords"].keys():
            for page in grip_params["page_num"]:
                response = self.request_url(_keyword=word, search_id=grip_params["keywords"][word], pageNum=page)
                self.extract_json_info(json_info=response)


if __name__ == "__main__":
    filepath = "D:/liangkaimeng/图片数据集/"
    cls = CrawlerRun(path=filepath)
