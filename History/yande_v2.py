__author__ = 'Eason'
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import urllib

# Config
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def main():
    url = input('请输入要爬取的URL：')
    print("正在爬取")
    r = requests.get(url, headers)  # 爬取图片
    soup = BeautifulSoup(r.text, features="lxml")
    list = soup.find_all(id='highres')
    src = list[0].attrs['href']  # 获取图片地址

    response = requests.get(src)  # 下载图片
    image = Image.open(BytesIO(response.content))
    filename = str.split(src, '/')[-1]  # 修正图片文件名
    raw_name = urllib.parse.unquote(filename)
    image.save(raw_name)
    print("Done")


if __name__ == '__main__':
    main()
