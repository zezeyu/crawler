# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

import pymysql.cursors

#请求URL并把结果用UTF-8编码
resp = urlopen("http://www.chinalaw.gov.cn/art/2018/3/12/art_11_207556.html").read().decode("utf-8")

#使用BeautifulSoup去解析
soup = BeautifulSoup(resp, "html.parser")

#网站title
title = soup.title.get_text()

#获取所有p标签
p_list = soup.findAll("p")

for p_i in p_list:
    text = p_i.string
    # print(str(text))
    rec = re.search(r"(第.+?条)\s\s(.*[^\n])", str(text))
    if rec:
        print(rec.group(1))  # 第几条
        print(rec.group(2))  # 对应的内容
        # 改成你自己的数据库
        connection = pymysql.connect(host='xx.xx.xx.xx', user='hz', password='yao', db='crawler', charset='utf8mb4', )
        try:
            with connection.cursor() as cursor:
                sql = "insert into `news`(`title`,`content`) values(%s,%s)"

                cursor.execute(sql, (rec.group(1), rec.group(2)))
                connection.commit()
        finally:
            connection.close()

