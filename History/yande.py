__author__ = 'Eason'
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import urllib

url = 'https://yande.re/post/show/499312'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

r = requests.get(url, headers)

soup = BeautifulSoup(r.text)
print(soup)
list = soup.find_all(id='highres')
src = list[0].attrs['href']
response = requests.get(src)
image = Image.open(BytesIO(response.content))
filename = str.split(src, '/')[-1]
raw_name = urllib.parse.unquote(filename)
image.save(raw_name)
