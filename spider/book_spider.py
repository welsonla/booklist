# -*- encoding=utf-8 -*-
import math
import time

import requests
from bs4 import BeautifulSoup
import re
import xlwt
from requests import request,get,post
from db import DBManager
from db import Book
from datetime import timedelta

class BookSpider:
    data_source = [
        # {
        #     "url":"https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4",
        #     "category":"小说"
        #  },
        # {
        #     "url":"https://book.douban.com/tag/%E6%96%87%E5%AD%A6",
        #     "category":"文学"
        #  },
        # {
        #     "url":"https://book.douban.com/tag/%E7%BB%8F%E5%85%B8",
        #     "category":"经典"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%8E%8B%E5%B0%8F%E6%B3%A2",
        #     "category":"王小波"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%B1%B3%E5%85%B0%C2%B7%E6%98%86%E5%BE%B7%E6%8B%89",
        #     "category":"米兰昆德拉"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E6%9D%91%E4%B8%8A%E6%98%A5%E6%A0%91",
        #     "category":"村上春树"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E4%B8%AD%E5%9B%BD%E6%96%87%E5%AD%A6",
        #     "category":"中国文学",
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E5%8F%A4%E9%BE%99",
        #     "category":"古龙"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E5%8E%86%E5%8F%B2",
        #     "category":"历史"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%88%B1%E6%83%85",
        #     "category":"爱情"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E6%8A%95%E8%B5%84",
        #     "category":"投资"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%BC%96%E7%A8%8B",
        #     "category":"编程"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C",
        #     "category":"神经网络"
        # },
        # {
        #   "url":"https://book.douban.com/tag/web",
        #   "category":"Web"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E5%93%B2%E5%AD%A6",
        #     "category":"哲学"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E5%BF%83%E7%90%86%E5%AD%A6",
        #     "category":"心理学"
        # },
        # {
        #     "url": "https://book.douban.com/tag/%E6%B8%B8%E8%AE%B0",
        #     "category": "游记"
        # },
        {
            "url":"https://book.douban.com/tag/%E6%91%84%E5%BD%B1",
            "category":"摄影"
        },
        # {
        #     "url":"https://book.douban.com/tag/%E7%AE%97%E6%B3%95",
        #     "category":"算法"
        # },
        # {
        #     "url":"https://book.douban.com/tag/%E7%A8%8B%E5%BA%8F",
        #     "category":"程序"
        # }
        # "https://book.douban.com/tag/%E7%BB%8F%E5%85%B8",  # 经典
        # "https://book.douban.com/tag/%E7%8E%8B%E5%B0%8F%E6%B3%A2",  # 王小波
        # "https://book.douban.com/tag/%E7%B1%B3%E5%85%B0%C2%B7%E6%98%86%E5%BE%B7%E6%8B%89",  # 米兰昆德拉
        # "https://book.douban.com/tag/%E6%9D%91%E4%B8%8A%E6%98%A5%E6%A0%91",  # 村上春树
        # "https://book.douban.com/tag/%E4%B8%AD%E5%9B%BD%E6%96%87%E5%AD%A6",  # 中国文学
        # "https://book.douban.com/tag/%E5%8F%A4%E9%BE%99",  # 古龙
        # "https://book.douban.com/tag/%E5%8E%86%E5%8F%B2",  # 历史
        # "https://book.douban.com/tag/%E7%88%B1%E6%83%85",  # 爱情
        # "https://book.douban.com/tag/%E6%8A%95%E8%B5%84",  # 投资
        # "https://book.douban.com/tag/%E7%BC%96%E7%A8%8B",  # 编程
        # "https://book.douban.com/tag/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C",  # 神经网络
        # "https://book.douban.com/tag/%E7%AE%97%E6%B3%95",  # 算法
        # "https://book.douban.com/tag/%E7%A8%8B%E5%BA%8F",  # 程序
    ]

    def __init__(self):
        print("BookSpider.init")
        self.manager = DBManager()
        self.start()

    def start(self):
        print("start")
        # self.manager.check('https://book.douban.com/subject/35695541/111')
        for dict in self.data_source:
            for i in range(10):
                print(f"正在抓取{dict['category']}第{i}页数据")
                # 获取页面html
                url = f"{dict['url']}?start={i * 20}&type=T"
                html = self.get_html(url)
                # 解析页面DOM元素
                self.parse_dom(html, category=dict['category'])
                print(html)

                # 防止抓取过于频繁
                time.sleep(5)


    def get_html(self, url):
        print(f"get_html:{url}")

        # 关闭https证书验证，警告
        requests.packages.urllib3.disable_warnings()

        head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        # 获取页面元素，并忽略ssl验证
        html = requests.get(url, headers=head, verify=False)
        print(f"html.StatusCode:{html.status_code}")
        return html.text

    def parse_dom(self, content, category = '小说'):
        soup = BeautifulSoup(content, "html.parser")

        index = 0
        for item in soup.find_all('li', class_='subject-item'):
            data = []
            dom = str(item)
            print(f"index:-------{index}")
            print(f"dom:--------{dom}")
            subject_url_patten = re.compile('<a class="nbg" href="(.*)" onclick=.*')
            cover_url_patten = re.compile('<img class="" src="(.*)" width="90"/>')
            rating_patten = re.compile('<span class="rating_nums">(.*)</span>')
            reader_patten = re.compile('\((\d{1,})人评价\)')
            title_patten = re.compile('title="(.*)"')
            author_patten = re.compile('<div class="pub">[\s\n]+(.*)[\s\n]+<\/div>')
            # auhor_patten = re.compile('<div class="pub">[\s\n]+ (.*) \/ (.*) \/ (.*) \/ (.*)(元|\(元\))[\s\n]+<\/div>')
            desc_patten = re.compile("<p>([\S\s\n]+.*)<\/p>")
            price_patten = re.compile('纸质版 (.*)元')

            print("开始解析")

            url = re.findall(subject_url_patten, dom)[0]
            cover_url = re.findall(cover_url_patten, dom)[0]
            rating = re.findall(rating_patten, dom)
            author_rslt = re.findall(author_patten, dom)
            title = re.findall(title_patten, dom) #!= '' ? re.findall(title_patten, dom)[0] : ""
            desc = re.findall(desc_patten, dom)
            price_str = re.findall(price_patten, dom)
            readers = re.findall(reader_patten, dom)

            if len(title) > 0:
                title = title[0]
            else:
                title = ""

            publish_date = ""
            auhor_name = ""
            publisher = ""
            price = 0

            print(author_rslt)

            if len(author_rslt) > 0:
                content = author_rslt[0]
                #  刘慈欣 / 重庆出版社 / 2010-11 / 38.00元
                item_array = str(content).strip().split('/')

                if len(item_array) > 0:
                    # print(f"查找作者{str(item_array[0]).rfind('出版社')}")
                    if str(item_array[0]).rfind('出版社') == -1:
                        auhor_name = item_array[0]
                        print(f"作者是:{item_array[0]}")

                # 出版社
                publisher_patten = re.compile('\/\s?(.*出版社)\s?')
                publisher_list = re.findall(publisher_patten, content)
                if len(publisher_list) > 0:
                    publisher = publisher_list[0]
                # 出版时间
                data_patten = re.compile("\s?(\d{4}.*)\s?\/")
                publish_date_list = re.findall(data_patten, content)
                if len(publish_date_list) > 0:
                    publish_date = publish_date_list[0]

                # 价格
                price_patten = re.compile('\/\s*(\d{1,}\.?\d{1,}?)元\s?')
                price_list = re.findall(price_patten, content)
                if len(price_list) > 0:
                    price = price_list[0]  # str(price_list[0]).replace("元", "").replace("(元)", "")
                print(f"{content} --- {publisher} --- {publish_date} ---- {price}")
            else:
                print("author null")

            # 列表有时候会缺失价格
            # if len(price) == 0:
            #     # if len(auhor) >= 4:
            #     #     price = float(str(auhor[3]).replace("元",""))
            #     # else:
            #         price = 0
            # else:
            #     price = price[0]

            # 评论人数少的图书会不显示评分
            if len(rating) == 0 or rating[0] == '':
                rating = 0
            else:
                rating = rating[0]

            # 缺少简介的情况
            if len(desc) == 0:
                desc = ""
            else:
                desc = re.findall(desc_patten, dom)[0]

            if len(readers) == 0:
                readers = 0
            else:
                readers = readers[0]

            print(f"url:{url}, ----- cover:{cover_url} --- {auhor_name}  ---- {readers}--- {rating} --- {title} ---- {desc} --- {price}")

            book = Book(name=title,
                        price=float(price),
                        author=auhor_name,
                        publisher=publisher,
                        publish_date=publish_date,
                        rating_count=readers,
                        rating=rating,
                        desc=desc,
                        cover_url=cover_url,
                        douban_url=url,
                        category=category)
            self.manager.insert_book(book)

            index+=1

