__author__ = 'Eason'
# -*- coding: utf-8 -*-
import os
import urllib
from io import BytesIO
from sys import argv

import requests
from PIL import Image
from bs4 import BeautifulSoup

# Config
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}


def get_tag(url):
    params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    tag = params['tags'][0]
    return tag


def check_tag_dir(tag):
    try:
        print("Checking download dictionary...")
        os.makedirs('./download', False)
    except FileExistsError:
        print("Success")
        try:
            print("Creating folder using tag...")
            os.makedirs(f'{"./download/"}{tag}', False)
        except FileExistsError:
            print("Folder already exist...Start downloading...")
        path = f'{r"./download/"}{tag}{r"/"}'
        return path


def get_link(url):
    r = requests.get(url, headers)  # 爬取图片
    soup = BeautifulSoup(r.text, features="lxml")
    url_list = soup.find_all(class_="directlink largeimg")
    return url_list


def main():
    if len(argv) == 2:  # 判断是否有传参
        url = argv[1]
    else:
        url = input('URL：')

    print("Working in progress:")
    url = url.strip()  # 去除URL中前后空格防止出错
    url_list = get_link(url)
    tag = get_tag(url)  # 检查文件夹是否存在
    path = check_tag_dir(tag)
    count = 0
    total = url_list.__len__()
    for seq in url_list:
        response = requests.get(seq.attrs['href'])  # Download image directly
        # response = requests.get(seq.attrs['href'], proxies=proxies)  # Download image via proxy
        image = Image.open(BytesIO(response.content))
        filename = str.split(seq.attrs['href'], '/')[-1]  # Correct filename
        raw_name = urllib.parse.unquote(filename)
        image.save(path + raw_name)
        count = count + 1
        process_percentage = '{:.2%}'.format(count / total)
        print("Downloading", process_percentage, ":", "Saved", count, 'image(s),', "Total", total, 'image(s) on page')

    print("Done")


if __name__ == '__main__':
    main()
