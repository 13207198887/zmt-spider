import json
import urllib
from urllib import request
import re
from bs4 import BeautifulSoup
import os

from utils import translate, db


def spider_tc():
    '''爬取techcrunch.com站点'''

    tc_url = "https://techcrunch.com/wp-json/tc/v1/magazine?page=1&_embed=true&_envelope=true&categories=449557028"
    header = {
        "referer": "https://techcrunch.com/mobile/",
        "upgrade-insecure-requests": 1,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36"
    }
    req = urllib.request.Request(tc_url, headers=header)
    res = urllib.request.urlopen(req).read()
    js_result = json.loads(res)
    for article in js_result['body']:
        link = article['guid']['rendered']
        if db.exist_article(link):
            continue
        article_id  = article['id']
        title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '',translate.TranslateByGoogle(article['title']['rendered']))
        content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', article['content']['rendered'])) 
        get_cover_req = urllib.request.Request(link, headers=header)
        get_cover_res = urllib.request.urlopen(get_cover_req).read().decode('utf-8')
        cover_link = re.findall(r'<img src="(.*?)" class="article__featured-image" />', get_cover_res)[0]
        if not cover_link:
            article_id = "test"
        else:            
            download_cover(cover_link, article_id)
        if not content:
            print("该链接没有内容：%s" % link)
        else:
            db.add_article(link, article_id, title, content)
            print(link)


def spider_reuters():
    '''爬取euters.com站点'''

    reuters_url = 'https://www.reuters.com/news/archive/technologyNews'
    header = {
        "referer": "https://www.google.com.hk/",
        "user-agent": "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"
    }
    req = urllib.request.Request(reuters_url, headers=header)
    res = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    hrefs = soup.select("div .story-content a")
    link_list = []
    for href in hrefs:
        link_list.append(href['href'])
    #对link列表进行更新判断
    #intersection交集
    #union并集
    #difference差集
    # if reuters_link:
    #     list_difference = list(set(link_list).difference(set(reuters_link)))
    #     if list_difference:
    #         # list_intersection = list(set(reuters_link).intersection(set(link_list)))
    #         # reuters_link = list_difference + list_intersection
    #         reuters_link = list_difference
    #     else:
    #         return None
    # else:
    #     reuters_link = link_list
    for link in link_list:
        if db.exist_article(link):
            continue
        link = "https://www.reuters.com"+link
        conten_req = urllib.request.Request(link, headers=header)
        content_res = urllib.request.urlopen(conten_req).read().decode('utf-8')
        en_title = re.findall(r'<h1 class="headline_2zdFM">(.*?)</h1>', content_res)[0]
        en_content = re.findall(r'<div class="body_1gnLA">(.*?)<div class="container_28wm1">', content_res)[0]
        img_src = re.findall(r'<div class="container_1Z7A0" style="background-image:none"><img src="(.*?)".*?>', content_res)
        if not img_src:
            #没有封面的话直接用本地预留的test.png
            article_id = "test"
        else:
            img = img_src[0].split('amp;')
            img.pop()
            img_url = "http:"+''.join(img)+"w=1280"
            article_id = link.split('-').pop()
            download_cover(img_url, article_id)
        title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '', translate.TranslateByGoogle(en_title))
        content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', en_content)) 
        if not content:
            print("该链接没有内容：%s" % link)
        else:
            db.add_article(link, article_id, title, content)
            print(link)

def spider_techradar():
    '''爬取techradar.com站点'''

    techradar_url = 'https://www.techradar.com/news/archive'
    header = {
        "referer": "https://www.google.com.hk/",
        "user-agent": "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50"
    }
    req = urllib.request.Request(techradar_url, headers=header)
    res = urllib.request.urlopen(req).read().decode('utf-8')
    day_data = res.split('<li class="list-title date-heading">')[1]
    soup = BeautifulSoup(day_data, 'html.parser')
    hrefs = soup.select("li .day-article a")
    link_list = []
    for href in hrefs:
        link_list.append(href['href'])
    for link in link_list:
        if db.exist_article(link):
            continue
        try:
            conten_req = urllib.request.Request(link, headers=header)
            content_res = urllib.request.urlopen(conten_req).read().decode('utf-8')
            en_title = re.findall(r'<h1 itemprop="name headline">(.*?)</h1>', content_res, re.I|re.S|re.M)[0]
            soup = BeautifulSoup(content_res, 'html.parser')
            en_content = soup.find_all("div", {"id": "article-body"})[0]
            en_content = BeautifulSoup(str(en_content), 'html.parser').get_text()
            img_url = re.findall(r'<img .*? data-original-mos="(.*?)" .*?>', content_res)[0]
            if not img_url:
                article_id = "test"
            else:
                article_id = (img_url.split('/')[-1]).split('.')[0]
            title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '', translate.TranslateByGoogle(en_title), re.I|re.S|re.M)
            content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', str(en_content), re.I|re.S|re.M))
        except Exception as e:
            print('='*20)
            print("抓取失败：%s" % link)
            print("错误信息：%s" % e )
            print('='*20)
            continue
        if not content:
            print("该链接没有内容：%s" % link)
        else:
            db.add_article(link, article_id, title, content)
            print(link)




def download_cover(url, article_id):
    '''下载封面图'''
    res = urllib.request.urlopen(url).read()
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    with open(save_path, 'wb') as f:
        f.write(res)
