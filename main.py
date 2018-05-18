from Publish import dayu, qie, baijia
from utils.Crawl_article import spider_tc, spider_reuters, spider_techradar
from utils import db

import yaml
import sqlite3
import os
from selenium import webdriver
import threading

def make_db_table(sql):
    '''创建数据库表'''
    conn = db.init_db()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()

def init_table():
    '''初始化数据库表'''
    make_db_table(
        '''create table if not exists articles (
        link text,
        article_id text,
        title text,
        content text
    )''')

    make_db_table(
        '''create table if not exists dayu (
        link text
    )''')

    make_db_table(
        '''create table if not exists qie (
        link text
    )''')

    make_db_table(
        '''create table if not exists baijia (
        link text
    )''')


def init_driver():
    '''初始化浏览器'''
    #===========================Chrome=================
    #进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    # 更换头部
    '''登陆时将请求头设置成手机代理防止被检测出来,登录请求的URL也用手机web版登录然后跳转回正常页面'''
    options.add_argument('user-agent: "Mozilla/5.0 (Android 6.0.1; Mo…43.0) Gecko/43.0 Firefox/43.0"')
    #不显示前台界面
    #options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    #driver = webdriver.Firefox()
    driver.maximize_window()
    return driver

def get_user(stage):
    '''读取账号信息
    param: stage->平台名称
    '''
    f = open(os.getcwd()+"\\user.yml")  
    values = yaml.load(f) 
    usr = values[stage]['usr']
    pwd = values[stage]['pwd']
    return usr, pwd

def start_spider():
    '''多线程开启爬虫'''
    tc = threading.Thread(target=spider_tc)
    reuters = threading.Thread(target=spider_reuters)
    techradar = threading.Thread(target=spider_techradar)
    tc.start()
    reuters.start()
    techradar.start()
    # spider_tc()
    # spider_reuters()
    # spider_techradar()


init_table()

driver = init_driver()

dayu_usr, dayu_pwd = get_user("dayu") 
baijia_usr, baijia_pwd = get_user("baijia")
qie_usr, qie_pwd = get_user("qie")


while True:
    start_spider()
    articles = db.get_articles()
    for article in articles:
        link, article_id, title, content = article

        if not db.whether_published("dayu", link):
            try:
                dayu.run(dayu_usr, dayu_pwd, driver, article_id, title, content)
            except:
                pass
            else:
                db.published_article("dayu", link)

        if not db.whether_published("qie", link):
            try:
                qie.run(qie_usr, qie_pwd, driver, article_id, title, content)              
            except:
                pass
            else:
                db.published_article("qie", link)

        if not db.whether_published("baijia", link):
            try:
                baijia.run(baijia_usr, baijia_pwd, driver, article_id, title, content)  
            except:
                pass 
            else:
                db.published_article("baijia", link)  


    



'''
TODO: 多进程爬取文章并发布,判断浏览器是否已开启，已开启的话则跳过新建一个浏览器进程节省开销
特别是 循环发布的时候

优化: 直接把所有要发布的文章集合到一个列表中，然后以列表的形式传参给平台[dayu.py],循环发布，每发布完一篇就重进写文章的页面中
'''