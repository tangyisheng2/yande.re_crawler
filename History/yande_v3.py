__author__ = 'Eason'
# -*- coding: utf-8 -*-

import urllib
from io import BytesIO

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


def get_link(url):
    r = requests.get(url, headers)  # 爬取图片
    soup = BeautifulSoup(r.text, features="lxml")
    url_list = soup.find_all(class_="directlink largeimg")
    return url_list


def main():
    url = input('URL：')
    print("Working in progress:")
    url_list = get_link(url)
    count = 0
    for seq in url_list:
        response = requests.get(seq.attrs['href'])  # Download image directly
        # response = requests.get(seq.attrs['href'], proxies=proxies)  # Download image via proxy
        image = Image.open(BytesIO(response.content))
        filename = str.split(seq.attrs['href'], '/')[-1]  # Correct filename
        raw_name = urllib.parse.unquote(filename)
        image.save("./download/" + raw_name)
        print("Saved", count + 1, 'image(s)')
        count = count + 1
    print("Done")


if __name__ == '__main__':
    main()
