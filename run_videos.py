from utils import db
from utils.Crawl_video import Tiktok

import sqlite3

def make_db_table(sql):
    '''创建数据库表'''
    conn = db.init_videoDB()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()

def init_table():
    '''初始化数据库表'''

    make_db_table(
        '''create table if not exists videos (
        download_link text
    )''')

    #===============
    #do more
    #===============

def start_download():
    '''开启视频下载'''
    tiktok = Tiktok()
    tiktok.favorite_download()


print("初始化数据库")
init_table()

print('='*30+"--START--"+'='*30)

# while True:
#     start_download()
start_download()