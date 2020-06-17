# coding : utf-8

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os


os.makedirs('output', exist_ok=True)
page_encoding = 'gb18030'
file_encoding = 'utf-8'

pool = {'http://cs.ahu.edu.cn/2018/0323/c11202a163167/page.htm'}


def category_extract(soup, link):
    try:
        title = soup.title.string
        a = soup.find_all("a")
        img = soup.find_all("img")
        text = soup.get_text()
        dn = "output/"
        os.makedirs(dn, exist_ok=True)
        with open(dn + "link.txt", "w", encoding=file_encoding) as f:  # encoding should be chosen properly
            f.write(link)
        with open(dn + "href.txt", "w", encoding=file_encoding) as f:
            for i in a:
                try:
                    f.write(i['href']+'\n')
                except Exception as e:
                    pass
        with open(dn + "img.txt", "w", encoding=file_encoding) as f:
            for i in img:
                try:
                    f.write(i['src']+'\n')
                except Exception as e:
                    pass
        with open(dn + "title.txt", "w", encoding=file_encoding) as f:
            f.write(title)
        with open(dn + "text.txt", "w", encoding=file_encoding) as f:
            f.write(text)
    except Exception as e:
        print(e)


for url in pool:
    try:
        v = []
        par = urlparse(url)
        Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                          'Referer': par[0] + '://' + par[1],
                          'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
                          'Host': par[1]}
        r = requests.get(url, headers=Default_Header, timeout=10).content
        soup = BeautifulSoup(r, 'html.parser', from_encoding=page_encoding)  # encoding should be chosen properly
        filt = ['script', 'noscript', 'style']
        for ff in filt:
            for i in soup.find_all(ff):
                i.decompose()
        category_extract(soup, url)
        title = soup.title.string
        a = soup.find_all("a")
        img = soup.find_all("img")
        text = soup.get_text()
        print(title)
        print(a)
        print(img)
        print(text)

    except Exception as e:
        print(e)

