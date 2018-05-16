import json
import urllib
from urllib import request
import re
from bs4 import BeautifulSoup
import os

from utils import translate


tc_link = ''
def spider_tc():
    '''爬取techcrunch.com站点'''

    global tc_link
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
    if tc_link == link:
        return None, None, None
    
    tc_link = link
    article_id  = article['id']
    title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '',translate.TranslateByGoogle(article['title']['rendered']))
    content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', article['content']['rendered'])) 
    get_cover_req = urllib.request.Request(link, headers=header)
    get_cover_res = urllib.request.urlopen(get_cover_req).read().decode('utf-8')
    cover_link = re.findall(r'<img src="(.*?)" class="article__featured-image" />', get_cover_res)[0]
    download_cover(cover_link, article_id)
    return article_id, title, content


reuters_link = None
def spider_reuters():
    '''爬取euters.com站点'''

    global reuters_link
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
    if reuters_link:
        list_difference = list(set(link_list).difference(set(reuters_link)))
        if list_difference:
            # list_intersection = list(set(reuters_link).intersection(set(link_list)))
            # reuters_link = list_difference + list_intersection
            reuters_link = list_difference
        else:
            return None
    else:
        reuters_link = link_list
    data_list = []
    for link in reuters_link:
        data_body = {}
        link = "https://www.reuters.com"+link
        conten_req = urllib.request.Request(link, headers=header)
        content_res = urllib.request.urlopen(conten_req).read().decode('utf-8')
        en_title = re.findall(r'<h1 class="headline_2zdFM">(.*?)</h1>', content_res)[0]
        en_content = re.findall(r'<div class="body_1gnLA">(.*?)<div class="container_28wm1">', content_res)[0]
        img_src = re.findall(r'<div class="container_1Z7A0" style="background-image:none"><img src="(.*?)".*?>', content_res)[0]
        img = img_src.split('amp;')
        img.pop()
        img_url = "http:"+''.join(img)+"w=1280"
        article_id = link.split('-').pop()
        download_cover(img_url, article_id)
        title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '', translate.TranslateByGoogle(en_title))
        content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', en_content)) 
        data_body['article_id'] = article_id
        data_body['title'] = title
        data_body['content'] = content
        data_list.append(data_body)
    reuters_link = link_list
    return data_list


techradar_link = None
def spider_techradar():
    '''爬取techradar.com站点'''

    global techradar_link
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
    #对link列表进行更新判断
    #intersection交集
    #union并集
    #difference差集
    if techradar_link:
        list_difference = list(set(link_list).difference(set(techradar_link)))
        if list_difference:
            # list_intersection = list(set(techradar_link).intersection(set(link_list)))
            # techradar_link = list_difference + list_intersection
            techradar_link = list_difference
        else:
            return None
    else:
        techradar_link = link_list
    data_list = []
    for link in techradar_link:
        data_body = {}
        conten_req = urllib.request.Request(link, headers=header)
        content_res = urllib.request.urlopen(conten_req).read().decode('utf-8')
        en_title = re.findall(r'<h1 itemprop="name headline">(.*?)</h1>', content_res)[0]
        img_url = re.findall(r'<img .*? data-original-mos="(.*?)" .*?>', content_res)[0]
        soup = BeautifulSoup(content_res, 'html.parser')
        en_content = soup.find("div", {"id": "article-body"})
        article_id = (img_url.split('/')[-1]).split('.')[0]
        download_cover(img_url, article_id)
        title = re.sub(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', '', translate.TranslateByGoogle(en_title))
        content = translate.TranslateByGoogle(re.sub(r'</?\w+[^>]*>', '', en_content)) 
        data_body['article_id'] = article_id
        data_body['title'] = title
        data_body['content'] = content
        data_list.append(data_body)
    techradar_link = link_list
    return data_list




def download_cover(url, article_id):
    '''下载封面图'''
    res = urllib.request.urlopen(url).read()
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    with open(save_path, 'wb') as f:
        f.write(res)
