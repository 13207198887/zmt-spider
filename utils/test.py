import json
import urllib
from urllib import request
import re
from bs4 import BeautifulSoup
import os

import translate

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
    print(link_list)
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
            print("没有最新的")
            return None
    else:
        techradar_link = link_list
    data_list = []
    for link in techradar_link:
        data_body = {}
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
        data_body['article_id'] = article_id
        data_body['title'] = title
        data_body['content'] = content
        data_list.append(data_body)
        print(data_body)
    techradar_link = link_list
    #return data_list




def download_cover(url, article_id):
    '''下载封面图'''
    res = urllib.request.urlopen(url).read()
    save_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'\\cover\\'+str(article_id)+'.png'
    with open(save_path, 'wb') as f:
        f.write(res)

while True:
    spider_techradar()