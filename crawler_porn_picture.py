#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/4 0004 19:52
# @Author  : LKM

import re
import warnings
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError, ConnectionError, ConnectTimeout

warnings.filterwarnings("ignore")


class PictureAutoCollect:

    def __init__(self, url: str):
        self.url = url
        self.draw_html()

    def draw_html(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
        }
        file_path = r"D:/Project/ViolationPatternRecognition/Dataset/sexual-behaviour/"

        for item in range(1, 53):
            for page in range(1, 501):
                page_address = self.url.format(item, page)
                try:
                    response = requests.get(url=page_address, headers=headers)
                    response.encoding = 'gbk'
                    tree_text = etree.HTML(response.text)

                    for index in range(30):
                        try:
                            img_src = tree_text.xpath('/html/body//div/div/div/ul/li/div/a/div/img/@src')[index]
                            extract_name = re.sub('/', '', re.findall(r"\d/(.+?).jpg", img_src)[0])
                            img_path = file_path + extract_name + ".jpg"

                            print(img_src, "\t\t\t\t", extract_name)
                            s = requests.session()
                            s.mount('https://', HTTPAdapter(max_retries=3))
                            try:
                                img_content = s.request("GET", url=img_src, headers=headers, verify=False, timeout=30).content
                                with open(img_path, "wb") as f:
                                    f.write(img_content)
                            except SSLError:
                                pass
                            except ConnectionError:
                                pass
                            except ConnectTimeout:
                                pass
                        except IndexError:
                            pass
                except SSLError:
                    pass
                except ConnectionError:
                    pass
                except ConnectTimeout:
                    pass


if __name__ == "__main__":
    _url = r"http://jrsb--0901196161.01-19.sepc--0912.gn1yg2fyt.com:8123/vodtype/{}-{}.html"
    PictureAutoCollect(_url)
