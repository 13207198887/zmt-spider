import json
import urllib
from urllib import request
import re
from utils import translate
import os

from Publish import dayu

new_link = ''

def spider_tc():
    global new_link
    tc_url = "https://techcrunch.com/wp-json/tc/v1/magazine?page=1&_embed=true&_envelope=true&categories=449557028"
    header = {
        "referer": "https://techcrunch.com/mobile/",
        "upgrade-insecure-requests": 1,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36"
    }
    req = urllib.request.Request(tc_url, headers=header)
    res = urllib.request.urlopen(req).read()
    js_result = json.loads(res)
    #for article in js_result['body']:
    #只爬取最新的一篇文章
    article = js_result['body'][0]
    link = article['guid']['rendered']
    if new_link == link:
        return None, None, None
    
    new_link = link
    article_id  = article['id']
    print(article_id)
    title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '',translate.TranslateByGoogle(article['title']['rendered']))
    content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', article['content']['rendered'])) 
    get_cover_req = urllib.request.Request(link, headers=header)
    get_cover_res = urllib.request.urlopen(get_cover_req).read().decode('utf-8')
    cover_link = re.findall(r'<img src="(.*?)" class="article__featured-image" />', get_cover_res)[0]
    download_cover(cover_link, article_id)
    print(link)
    return article_id, title, content

def download_cover(url, article_id):
    '''下载封面图'''
    res = urllib.request.urlopen(url).read()
    save_path = os.getcwd()+'\\cover\\'+ str(article_id) +'.png'
    with open(save_path, 'wb') as f:
        f.write(res)


while True:
    article_id, title, content = spider_tc()
    if title and content:
        dayu.run(article_id, title, content)